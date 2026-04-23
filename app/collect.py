from __future__ import annotations

import hashlib
import re
from datetime import UTC, datetime, timedelta
from email.utils import parsedate_to_datetime

import feedparser
import requests

from app.models import Article
from app.sources import SOURCES, Source


USER_AGENT = "weekly-ai-news-bot/0.1"


def collect_articles(lookback_days: int, max_per_source: int) -> list[Article]:
    cutoff = datetime.now(UTC) - timedelta(days=lookback_days)
    articles: list[Article] = []

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    for source in SOURCES:
        source_articles = collect_from_source(session, source, cutoff, max_per_source)
        articles.extend(source_articles)

    return dedupe_articles(articles)


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
        title = normalize_whitespace(entry.get("title", "").strip())
        if not url or not title:
            continue

        article = Article(
            title=title,
            url=url,
            source_name=source.name,
            source_kind=source.kind,
            category_hint=source.category_hint,
            published_at=(published or datetime.now(UTC)).date().isoformat(),
            dedupe_key=make_dedupe_key(title, url),
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
                return dt.replace(tzinfo=UTC)
            return dt.astimezone(UTC)
        except (TypeError, ValueError, IndexError):
            continue
    return None


def dedupe_articles(articles: list[Article]) -> list[Article]:
    seen: set[str] = set()
    unique: list[Article] = []

    for article in articles:
        if article.dedupe_key in seen:
            continue
        seen.add(article.dedupe_key)
        unique.append(article)

    return unique


def make_dedupe_key(title: str, url: str) -> str:
    canonical_title = re.sub(r"[^a-z0-9가-힣]+", "", title.lower())
    domainless_url = re.sub(r"^https?://", "", url.lower()).rstrip("/")
    raw = f"{canonical_title}|{domainless_url}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()


def normalize_whitespace(value: str) -> str:
    return " ".join(value.split())
