from __future__ import annotations

import hashlib
import re
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import urlparse

import feedparser
import requests

from app.models import Article
from app.sources import SOURCES, Source


USER_AGENT = "weekly-ai-news-bot/0.1"
LOOKBACK_STEPS = (0, 7, 14)
MIN_DISTINCT_SOURCES = 3
MAX_SOURCE_SHARE = 0.6


def collect_articles(lookback_days: int, max_per_source: int) -> list[Article]:
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    best_articles: list[Article] = []
    for extra_days in LOOKBACK_STEPS:
        cutoff = datetime.now(timezone.utc) - timedelta(days=lookback_days + extra_days)
        articles: list[Article] = []

        for source in SOURCES:
            source_articles = collect_from_source(session, source, cutoff, max_per_source)
            articles.extend(source_articles)

        deduped = dedupe_articles(articles)
        best_articles = deduped
        if has_enough_diversity(deduped):
            return deduped

    return best_articles


def has_enough_diversity(articles: list[Article]) -> bool:
    if not articles:
        return False

    counts = source_counts(articles)
    distinct_sources = len(counts)
    dominant_share = max(counts.values()) / len(articles)
    return distinct_sources >= MIN_DISTINCT_SOURCES and dominant_share <= MAX_SOURCE_SHARE


def collect_from_source(
    session: requests.Session,
    source: Source,
    cutoff: datetime,
    max_per_source: int,
) -> list[Article]:
    if source.feed_url:
        items = collect_from_feed(session, source, cutoff, max_per_source)
        if items:
            return items

    return []


def collect_from_feed(
    session: requests.Session,
    source: Source,
    cutoff: datetime,
    max_per_source: int,
) -> list[Article]:
    try:
        response = session.get(source.feed_url, timeout=20)
        response.raise_for_status()
    except requests.RequestException:
        return []

    parsed = feedparser.parse(response.content)
    articles: list[Article] = []

    for entry in parsed.entries:
        published = parse_entry_datetime(entry)
        if published and published < cutoff:
            continue

        url = entry.get("link", "").strip()
        preferred_url = extract_preferred_url(entry, source, fallback_url=url)
        title = normalize_whitespace(entry.get("title", "").strip())
        if not preferred_url or not title:
            continue

        article = Article(
            title=title,
            url=preferred_url,
            source_name=source.name,
            source_kind=source.kind,
            source_priority=source.priority,
            category_hint=source.category_hint,
            published_at=(published or datetime.now(timezone.utc)).date().isoformat(),
            dedupe_key=make_dedupe_key(title, preferred_url),
        )
        articles.append(article)

        if len(articles) >= max_per_source:
            break

    return articles


def parse_entry_datetime(entry: feedparser.FeedParserDict) -> datetime | None:
    for key in ("published", "updated"):
        raw = entry.get(key)
        if not raw:
            continue
        try:
            dt = parsedate_to_datetime(raw)
            if dt.tzinfo is None:
                return dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except (TypeError, ValueError, IndexError):
            continue
    return None


def dedupe_articles(articles: list[Article]) -> list[Article]:
    seen: set[str] = set()
    unique: list[Article] = []

    ordered_articles = sorted(
        articles,
        key=lambda article: (article.source_priority, article.published_at, article.source_name),
        reverse=True,
    )

    for article in ordered_articles:
        if article.dedupe_key in seen:
            continue
        seen.add(article.dedupe_key)
        unique.append(article)

    return unique


def source_counts(articles: list[Article]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for article in articles:
        counts[article.source_name] = counts.get(article.source_name, 0) + 1
    return counts


def make_dedupe_key(title: str, url: str) -> str:
    canonical_title = re.sub(r"[^a-z0-9가-힣]+", "", title.lower())
    domainless_url = re.sub(r"^https?://", "", url.lower()).rstrip("/")
    raw = f"{canonical_title}|{domainless_url}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()


def normalize_whitespace(value: str) -> str:
    return " ".join(value.split())


def extract_preferred_url(
    entry: feedparser.FeedParserDict,
    source: Source,
    fallback_url: str,
) -> str:
    if source.name != "GeekNews":
        return fallback_url

    source_host = normalize_host(source.url)
    candidates: list[str] = []

    for link_info in entry.get("links", []):
        href = (link_info.get("href") or "").strip()
        if href:
            candidates.append(href)

    for field in ("summary", "description"):
        raw = entry.get(field, "") or ""
        candidates.extend(re.findall(r'https?://[^\s"\'<>]+', raw))

    for candidate in candidates:
        if normalize_host(candidate) != source_host:
            return candidate

    return fallback_url


def normalize_host(url: str) -> str:
    return (urlparse(url).netloc or "").lower().removeprefix("www.")
