from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    openai_model: str
    slack_bot_token: str
    slack_channel_id: str
    lookback_days: int
    max_per_source: int
    top_k: int


def get_settings() -> Settings:
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-5"),
        slack_bot_token=os.getenv("SLACK_BOT_TOKEN", ""),
        slack_channel_id=os.getenv("SLACK_CHANNEL_ID", ""),
        lookback_days=int(os.getenv("NEWS_LOOKBACK_DAYS", "7")),
        max_per_source=int(os.getenv("NEWS_MAX_PER_SOURCE", "12")),
        top_k=int(os.getenv("NEWS_TOP_K", "5")),
    )
