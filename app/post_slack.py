from __future__ import annotations

from slack_sdk import WebClient


def post_message(token: str, channel_id: str, text: str) -> None:
    client = WebClient(token=token)
    client.chat_postMessage(
        channel=channel_id,
        text=text,
        mrkdwn=True,
        unfurl_links=False,
        unfurl_media=False,
    )
