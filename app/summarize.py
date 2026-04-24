from __future__ import annotations

import json
import re

from google import genai

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
- Prefer items relevant to AI, speech, voice, STT, TTS, AICC, callbots, chatbots, contact centers.
- Treat GeekNews as a high-priority curated source for discovering important AI and developer news.
- It is fine if categories are imbalanced.
- Do not let a single source dominate the list when other credible sources are available.
- Prefer source diversity. Unless the candidate pool is extremely narrow, cap each source at 2 selected items.
- Summary lines must be in Korean.
- Each summary line should be one concise sentence.
- Summaries must describe only the article's contents.
- Do not add interpretation, implications, recommendations, or commentary beyond the article itself.
- Do not include markdown code fences.
- Keep titles and URLs exactly as provided.
- Scores must be integers from 0 to 100.
"""

RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "items": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "title": {"type": "STRING"},
                    "url": {"type": "STRING"},
                    "category": {
                        "type": "STRING",
                        "enum": ["AI 전반", "STT·TTS", "AICC"],
                    },
                    "score": {"type": "INTEGER"},
                    "summary_lines": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"},
                        "minItems": 3,
                        "maxItems": 3,
                    },
                },
                "required": ["title", "url", "category", "score", "summary_lines"],
            },
        }
    },
    "required": ["items"],
}


def create_weekly_brief(
    client: genai.Client,
    model: str,
    articles: list[Article],
    start_date: str,
    end_date: str,
    top_k: int,
    source_counts: dict[str, int],
    collection_lookback_days: int,
) -> WeeklyBrief:
    payload = [
        {
            "title": article.title,
            "url": article.url,
            "source_name": article.source_name,
            "source_kind": article.source_kind,
            "source_priority": article.source_priority,
            "category_hint": article.category_hint,
            "published_at": article.published_at,
        }
        for article in articles
    ]

    prompt = (
        f"Review these candidate articles for the week {start_date} to {end_date}. "
        f"Select the top {top_k} items.\n"
        f"Candidate source counts: {json.dumps(source_counts, ensure_ascii=False)}\n"
        f"Collection lookback days actually used: {collection_lookback_days}\n\n"
        f"Candidates:\n{json.dumps(payload, ensure_ascii=False)}"
    )

    response = client.models.generate_content(
        model=model,
        contents=f"{SYSTEM_PROMPT}\n\n{prompt}",
        config={
            "temperature": 0.2,
            "response_mime_type": "application/json",
            "response_schema": RESPONSE_SCHEMA,
        },
    )

    response_text = (response.text or "").strip()
    parsed = parse_response_json(response_text)
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

    return WeeklyBrief(
        start_date=start_date,
        end_date=end_date,
        items=items,
        source_counts=source_counts,
        collection_lookback_days=collection_lookback_days,
    )


def find_source_name(url: str, articles: list[Article]) -> str:
    for article in articles:
        if article.url == url:
            return article.source_name
    return ""


def parse_response_json(response_text: str) -> dict:
    if not response_text:
        raise ValueError("Gemini returned an empty response")

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass

    cleaned = response_text.strip()
    cleaned = re.sub(r"^```json\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    if match:
        return json.loads(match.group(0))

    raise ValueError(f"Gemini returned non-JSON output: {response_text[:500]}")
