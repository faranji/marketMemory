from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Asset:
    id: str
    ticker: str
    asset_name: str
    asset_class: str
    benchmark_asset_id: str | None = None


@dataclass(frozen=True)
class NewsArticle:
    id: str
    title: str
    summary: str
    source: str
    published_at: datetime
    url: str
    primary_asset_id: str | None
    ticker: str
    topic: str
    leakage_status: str
