from __future__ import annotations

import json

from anthropic import AnthropicVertex

from app.models import Article, RankedItem, WeeklyBrief


SYSTEM_PROMPT = """You are an assistant that curates a weekly AI news briefing for a Korean callbot PM team.

Return strict JSON with this schema:
{
  "items": [
    {
      "title": "string",
      "url": "string",
      "category": "AI 전반|STT·TTS|AICC",
      "score": 0,
      "summary_lines": ["line1", "line2", "line3"]
    }
  ]
}

Rules:
- Pick at most the requested top_k items.
- Prefer items relevant to AI, speech, voice, STT, TTS, AICC, callbots, contact centers.
- It is fine if categories are imbalanced.
- Summary lines must be in Korean.
- Each summary line should be one concise sentence.
- Do not include markdown code fences.
- Keep titles and URLs exactly as provided.
- Scores must be integers from 0 to 100.
"""


def create_weekly_brief(
    client: AnthropicVertex,
    model: str,
    articles: list[Article],
    start_date: str,
    end_date: str,
    top_k: int,
) -> WeeklyBrief:
    payload = [
        {
            "title": article.title,
            "url": article.url,
            "source_name": article.source_name,
            "source_kind": article.source_kind,
            "category_hint": article.category_hint,
            "published_at": article.published_at,
        }
        for article in articles
    ]

    prompt = (
        f"Review these candidate articles for the week {start_date} to {end_date}. "
        f"Select the top {top_k} items.\n\n"
        f"Candidates:\n{json.dumps(payload, ensure_ascii=False)}"
    )

    response = client.messages.create(
        model=model,
        max_tokens=2500,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    response_text = "".join(
        block.text for block in response.content if getattr(block, "type", "") == "text"
    )
    parsed = json.loads(response_text)
    items = [
        RankedItem(
            title=item["title"],
            url=item["url"],
            summary_lines=item["summary_lines"][:3],
            source_name=find_source_name(item["url"], articles),
            category=item["category"],
            score=int(item["score"]),
        )
        for item in parsed.get("items", [])
    ]

    return WeeklyBrief(start_date=start_date, end_date=end_date, items=items)


def find_source_name(url: str, articles: list[Article]) -> str:
    for article in articles:
        if article.url == url:
            return article.source_name
    return ""
