from __future__ import annotations

from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd

from src.models import Asset, NewsArticle


MOCK_ASSETS = [
    Asset("asset-googl", "GOOGL", "Alphabet Class A", "equity", "asset-qqq"),
    Asset("asset-tsla", "TSLA", "Tesla", "equity", "asset-qqq"),
    Asset("asset-nvda", "NVDA", "Nvidia", "equity", "asset-qqq"),
    Asset("asset-qqq", "QQQ", "Invesco QQQ Trust", "etf", None),
]


def get_mock_assets() -> list[Asset]:
    return MOCK_ASSETS


def get_mock_articles() -> list[NewsArticle]:
    base = datetime(2026, 7, 23, 9, 30, tzinfo=timezone.utc)
    return [
        NewsArticle(
            id="news-001",
            title="Alphabet expands AI infrastructure spending after cloud demand accelerates",
            summary="The company announced additional data-centre investment as enterprise demand for AI services increased.",
            source="Demo Financial News",
            published_at=base,
            url="https://example.com/news-001",
            primary_asset_id="asset-googl",
            ticker="GOOGL",
            topic="AI investment / Cloud",
            leakage_status="predictive_event",
        ),
        NewsArticle(
            id="news-002",
            title="Tesla opens lower-cost battery facility as production targets rise",
            summary="The new facility is expected to lower battery costs and expand future vehicle output.",
            source="Demo Financial News",
            published_at=base - timedelta(hours=2),
            url="https://example.com/news-002",
            primary_asset_id="asset-tsla",
            ticker="TSLA",
            topic="Manufacturing / Batteries",
            leakage_status="predictive_event",
        ),
        NewsArticle(
            id="news-003",
            title="Nvidia introduces a new enterprise inference platform",
            summary="The platform targets lower inference costs for large-scale enterprise AI workloads.",
            source="Demo Financial News",
            published_at=base - timedelta(hours=4),
            url="https://example.com/news-003",
            primary_asset_id="asset-nvda",
            ticker="NVDA",
            topic="Product launch / AI",
            leakage_status="predictive_event",
        ),
        NewsArticle(
            id="news-004",
            title="Technology shares slide as investors reassess AI spending",
            summary="Major technology stocks declined during the session amid valuation concerns.",
            source="Demo Financial News",
            published_at=base - timedelta(hours=6),
            url="https://example.com/news-004",
            primary_asset_id="asset-qqq",
            ticker="QQQ",
            topic="Market recap",
            leakage_status="market_recap",
        ),
        NewsArticle(
            id="news-005",
            title="Regulators open a competition review into a digital advertising acquisition",
            summary="The review will examine whether the transaction could reduce competition.",
            source="Demo Financial News",
            published_at=base - timedelta(hours=8),
            url="https://example.com/news-005",
            primary_asset_id="asset-googl",
            ticker="GOOGL",
            topic="Regulation / Antitrust",
            leakage_status="predictive_event",
        ),
    ]


def get_mock_article_assets(article_id: str) -> list[Asset]:
    article = next(item for item in get_mock_articles() if item.id == article_id)
    primary = next(item for item in MOCK_ASSETS if item.id == article.primary_asset_id)
    assets = [primary]
    if primary.benchmark_asset_id:
        benchmark = next(
            item for item in MOCK_ASSETS if item.id == primary.benchmark_asset_id
        )
        assets.append(benchmark)
    return assets


def get_mock_predictions(article_id: str) -> pd.DataFrame:
    paths = {
        "news-001": [0.8, 1.5, 2.1, 1.7, 0.6],
        "news-002": [0.3, 0.9, 1.4, 2.0, 1.6],
        "news-003": [1.2, 2.2, 2.8, 2.4, 1.5],
        "news-004": [-0.9, -1.2, -0.7, 0.1, 0.4],
        "news-005": [-1.0, -1.8, -2.4, -1.7, -0.8],
    }
    expected = paths.get(article_id, [0.2, 0.4, 0.5, 0.3, 0.1])
    horizons = [1, 3, 5, 10, 20]
    probabilities = [0.64, 0.68, 0.71, 0.63, 0.54]

    rows = []
    for horizon, movement, probability in zip(horizons, expected, probabilities):
        spread = 0.8 + (horizon ** 0.55) * 0.65
        direction = (
            "UP" if movement > 0.35 else
            "DOWN" if movement < -0.35 else
            "NEUTRAL"
        )
        rows.append(
            {
                "Horizon": f"{horizon}D",
                "Direction": direction,
                "Probability": probability,
                "Probability UP": probability if direction == "UP" else (1 - probability) / 2,
                "Probability NEUTRAL": probability if direction == "NEUTRAL" else (1 - probability) / 2,
                "Probability DOWN": probability if direction == "DOWN" else (1 - probability) / 2,
                "Expected abnormal return (%)": movement,
                "Lower bound (%)": movement - spread,
                "Upper bound (%)": movement + spread,
            }
        )
    return pd.DataFrame(rows)


def get_mock_analogues(article_id: str) -> pd.DataFrame:
    titles = [
        "Cloud demand leads company to expand data-centre investment",
        "Enterprise AI adoption accelerates infrastructure spending",
        "Technology group raises capital expenditure outlook",
        "New computing platform targets enterprise customers",
        "Regulatory approval supports strategic expansion",
        "Company announces new long-term cloud capacity",
        "AI services growth exceeds earlier expectations",
        "Management outlines larger infrastructure programme",
        "Digital advertising outlook improves after product changes",
        "Software company increases investment in specialised chips",
        "Enterprise demand strengthens despite macro uncertainty",
        "New AI partnership broadens distribution",
    ]
    rng = np.random.default_rng(abs(hash(article_id)) % (2**32))
    base = datetime(2025, 12, 1, tzinfo=timezone.utc)
    rows = []

    for i, title in enumerate(titles):
        base_return = rng.normal(1.0, 1.7)
        rows.append(
            {
                "Rank": i + 1,
                "Date": (base - timedelta(days=52 * i)).date(),
                "Historical event": title,
                "Text similarity": float(
                    np.clip(0.91 - i * 0.019 + rng.normal(0, 0.008), 0.65, 0.95)
                ),
                "Regime similarity": float(
                    np.clip(0.84 - i * 0.015 + rng.normal(0, 0.02), 0.55, 0.90)
                ),
                "Combined similarity": float(
                    np.clip(0.88 - i * 0.018 + rng.normal(0, 0.01), 0.60, 0.93)
                ),
                "1D abnormal return (%)": float(base_return),
                "5D abnormal return (%)": float(base_return + rng.normal(0.7, 1.2)),
                "20D abnormal return (%)": float(base_return + rng.normal(0.2, 2.6)),
                "Impact shape": rng.choice(
                    ["immediate", "gradual", "persistent", "reversal"]
                ),
                "URL": f"https://example.com/analogue-{i + 1}",
            }
        )
    return pd.DataFrame(rows)


def get_mock_prices(ticker: str) -> pd.DataFrame:
    rng = np.random.default_rng(abs(hash(ticker)) % (2**32))
    dates = pd.bdate_range(end="2026-07-22", periods=50)
    returns = rng.normal(0.0007, 0.012, len(dates))
    start = {"GOOGL": 175, "TSLA": 305, "NVDA": 152, "QQQ": 535}.get(
        ticker, 100
    )
    prices = start * np.cumprod(1 + returns)
    return pd.DataFrame({"date": dates, "close": prices})
