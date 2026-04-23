from __future__ import annotations

from app.models import WeeklyBrief


def render_weekly_message(brief: WeeklyBrief) -> str:
    lines = [
        f"[주간 AI 브리핑] {brief.start_date} ~ {brief.end_date}",
        "",
        "이번 주에는 AICC와 음성 AI 운영 관점에서 참고할 만한 업데이트를 중심으로 Top 5를 정리했습니다.",
        "",
    ]

    for index, item in enumerate(brief.items, start=1):
        lines.append(f"{index}. <{item.url}|{item.title}>")
        for summary_line in item.summary_lines[:3]:
            lines.append(f"- {summary_line}")
        lines.append("")

    return "\n".join(lines).strip()
