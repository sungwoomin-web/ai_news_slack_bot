from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    google_cloud_project: str
    vertex_region: str
    gemini_model: str
    slack_bot_token: str
    slack_channel_id: str
    lookback_days: int
    max_per_source: int
    top_k: int


def get_settings() -> Settings:
    return Settings(
        google_cloud_project=os.getenv("GOOGLE_CLOUD_PROJECT", ""),
        vertex_region=os.getenv("VERTEX_REGION", "us-east5"),
        gemini_model=os.getenv(
            "GEMINI_MODEL",
            os.getenv("ANTHROPIC_VERTEX_MODEL", "gemini-2.5-pro"),
        ),
        slack_bot_token=os.getenv("SLACK_BOT_TOKEN", ""),
        slack_channel_id=os.getenv("SLACK_CHANNEL_ID", ""),
        lookback_days=int(os.getenv("NEWS_LOOKBACK_DAYS", "7")),
        max_per_source=int(os.getenv("NEWS_MAX_PER_SOURCE", "12")),
        top_k=int(os.getenv("NEWS_TOP_K", "5")),
    )
