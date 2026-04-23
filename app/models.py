from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Article:
    title: str
    url: str
    source_name: str
    source_kind: str
    category_hint: str
    published_at: str
    summary: str = ""
    score: int = 0
    dedupe_key: str = ""
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RankedItem:
    title: str
    url: str
    summary_lines: list[str]
    source_name: str
    category: str
    score: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class WeeklyBrief:
    start_date: str
    end_date: str
    items: list[RankedItem] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "generated_at": self.generated_at,
            "items": [item.to_dict() for item in self.items],
        }
