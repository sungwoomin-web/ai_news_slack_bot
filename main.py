from __future__ import annotations

import argparse
from datetime import date, timedelta
from pathlib import Path

from google import genai

from app.collect import collect_articles, source_counts
from app.config import get_settings
from app.post_slack import post_message
from app.render import render_weekly_message
from app.storage import save_json
from app.summarize import create_weekly_brief


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Weekly AI news Slack bot")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate the briefing without posting to Slack",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = get_settings()

    if not settings.google_cloud_project:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT is required")

    if not args.dry_run and (not settings.slack_bot_token or not settings.slack_channel_id):
        raise RuntimeError("SLACK_BOT_TOKEN and SLACK_CHANNEL_ID are required unless --dry-run is used")

    today = date.today()
    start_date = (today - timedelta(days=settings.lookback_days)).isoformat()
    end_date = today.isoformat()

    articles = collect_articles(
        lookback_days=settings.lookback_days,
        max_per_source=settings.max_per_source,
    )
    article_source_counts = source_counts(articles)
    collection_lookback_days = settings.lookback_days
    if articles:
        oldest_date = min(article.published_at for article in articles)
        collection_lookback_days = max(
            settings.lookback_days,
            (today - date.fromisoformat(oldest_date)).days,
        )

    client = genai.Client(
        vertexai=True,
        project=settings.google_cloud_project,
        location=settings.vertex_region,
    )
    brief = create_weekly_brief(
        client=client,
        model=settings.gemini_model,
        articles=articles,
        start_date=start_date,
        end_date=end_date,
        top_k=settings.top_k,
        source_counts=article_source_counts,
        collection_lookback_days=collection_lookback_days,
    )

    message = render_weekly_message(brief)

    artifacts_dir = Path("data")
    save_json(artifacts_dir / "articles.json", {"articles": [article.to_dict() for article in articles]})
    save_json(
        artifacts_dir / "source_stats.json",
        {
            "requested_lookback_days": settings.lookback_days,
            "actual_collection_lookback_days": collection_lookback_days,
            "source_counts": article_source_counts,
        },
    )
    save_json(artifacts_dir / "weekly_brief.json", brief.to_dict())
    (artifacts_dir / "weekly_message.txt").write_text(message + "\n", encoding="utf-8")

    if args.dry_run:
        print(message)
        return

    post_message(
        token=settings.slack_bot_token,
        channel_id=settings.slack_channel_id,
        text=message,
    )
    print("Posted weekly briefing to Slack.")


if __name__ == "__main__":
    main()
