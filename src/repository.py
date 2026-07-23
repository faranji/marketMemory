from __future__ import annotations

from datetime import datetime

import pandas as pd

from src.db import get_supabase_client
from src.mock_data import (
    get_mock_analogues,
    get_mock_article_assets,
    get_mock_articles,
    get_mock_assets,
    get_mock_predictions,
    get_mock_prices,
)
from src.models import Asset, NewsArticle


class MarketMemoryRepository:
    """Streamlit reads only through this repository."""

    def __init__(self) -> None:
        self.client = get_supabase_client()

    @property
    def mode(self) -> str:
        return "SUPABASE" if self.client is not None else "MOCK"

    def list_assets(self) -> list[Asset]:
        if self.client is None:
            return get_mock_assets()

        response = (
            self.client.table("assets")
            .select("id,ticker,asset_name,asset_class,benchmark_asset_id")
            .eq("is_active", True)
            .order("ticker")
            .execute()
        )
        return [
            Asset(
                id=str(row["id"]),
                ticker=row["ticker"],
                asset_name=row["asset_name"],
                asset_class=row["asset_class"],
                benchmark_asset_id=(
                    str(row["benchmark_asset_id"])
                    if row.get("benchmark_asset_id")
                    else None
                ),
            )
            for row in response.data
        ]

    def _asset_map(self) -> dict[str, Asset]:
        return {asset.id: asset for asset in self.list_assets()}

    def list_articles(self, limit: int = 50) -> list[NewsArticle]:
        if self.client is None:
            return get_mock_articles()

        asset_map = self._asset_map()
        response = (
            self.client.table("news_articles")
            .select(
                "id,title,summary,source_name,published_at,canonical_url,"
                "primary_asset_id,topic,leakage_status"
            )
            .eq("is_active", True)
            .order("published_at", desc=True)
            .limit(limit)
            .execute()
        )

        articles: list[NewsArticle] = []
        for row in response.data:
            primary_id = str(row["primary_asset_id"]) if row.get("primary_asset_id") else None
            ticker = asset_map[primary_id].ticker if primary_id in asset_map else "UNASSIGNED"
            articles.append(
                NewsArticle(
                    id=str(row["id"]),
                    title=row["title"],
                    summary=row.get("summary") or "",
                    source=row.get("source_name") or "Unknown",
                    published_at=datetime.fromisoformat(
                        row["published_at"].replace("Z", "+00:00")
                    ),
                    url=row.get("canonical_url") or "",
                    primary_asset_id=primary_id,
                    ticker=ticker,
                    topic=row.get("topic") or "Unclassified",
                    leakage_status=row.get("leakage_status") or "not_reviewed",
                )
            )
        return articles

    def list_assets_for_article(self, article_id: str) -> list[Asset]:
        if self.client is None:
            return get_mock_article_assets(article_id)

        all_assets = self._asset_map()
        response = (
            self.client.table("article_assets")
            .select("asset_id,is_primary,relevance_score")
            .eq("article_id", article_id)
            .order("is_primary", desc=True)
            .order("relevance_score", desc=True)
            .execute()
        )
        return [
            all_assets[str(row["asset_id"])]
            for row in response.data
            if str(row["asset_id"]) in all_assets
        ]

    def _latest_prediction_run_id(
        self,
        article_id: str,
        asset_id: str,
    ) -> str | None:
        response = (
            self.client.table("prediction_runs")
            .select("id")
            .eq("query_article_id", article_id)
            .eq("asset_id", asset_id)
            .eq("status", "completed")
            .order("generated_at", desc=True)
            .limit(1)
            .execute()
        )
        if not response.data:
            return None
        return str(response.data[0]["id"])

    def get_predictions(
        self,
        article_id: str,
        asset_id: str,
    ) -> pd.DataFrame:
        if self.client is None:
            return get_mock_predictions(article_id)

        run_id = self._latest_prediction_run_id(article_id, asset_id)
        if not run_id:
            return pd.DataFrame()

        response = (
            self.client.table("prediction_horizons")
            .select(
                "horizon_days,direction,probability_up,probability_neutral,"
                "probability_down,expected_abnormal_return,lower_bound,upper_bound"
            )
            .eq("prediction_run_id", run_id)
            .order("horizon_days")
            .execute()
        )

        rows = []
        for row in response.data:
            probabilities = {
                "UP": float(row["probability_up"]),
                "NEUTRAL": float(row["probability_neutral"]),
                "DOWN": float(row["probability_down"]),
            }
            direction = row["direction"]
            rows.append(
                {
                    "Horizon": f'{row["horizon_days"]}D',
                    "Direction": direction,
                    "Probability": probabilities[direction],
                    "Probability UP": probabilities["UP"],
                    "Probability NEUTRAL": probabilities["NEUTRAL"],
                    "Probability DOWN": probabilities["DOWN"],
                    "Expected abnormal return (%)": float(
                        row["expected_abnormal_return"]
                    ),
                    "Lower bound (%)": float(row["lower_bound"]),
                    "Upper bound (%)": float(row["upper_bound"]),
                }
            )
        return pd.DataFrame(rows)

    def get_analogues(
        self,
        article_id: str,
        asset_id: str,
        limit: int = 20,
    ) -> pd.DataFrame:
        if self.client is None:
            return get_mock_analogues(article_id).head(limit)

        run_id = self._latest_prediction_run_id(article_id, asset_id)
        if not run_id:
            return pd.DataFrame()

        response = (
            self.client.table("historical_analogues")
            .select(
                "rank,historical_title,historical_published_at,text_similarity,"
                "regime_similarity,combined_similarity,abnormal_return_1d,"
                "abnormal_return_5d,abnormal_return_20d,impact_shape,source_url"
            )
            .eq("prediction_run_id", run_id)
            .order("rank")
            .limit(limit)
            .execute()
        )

        return pd.DataFrame(
            [
                {
                    "Rank": int(row["rank"]),
                    "Date": row["historical_published_at"][:10],
                    "Historical event": row["historical_title"],
                    "Text similarity": float(row["text_similarity"]),
                    "Regime similarity": float(row["regime_similarity"]),
                    "Combined similarity": float(row["combined_similarity"]),
                    "1D abnormal return (%)": float(row["abnormal_return_1d"]),
                    "5D abnormal return (%)": float(row["abnormal_return_5d"]),
                    "20D abnormal return (%)": float(row["abnormal_return_20d"]),
                    "Impact shape": row.get("impact_shape") or "unknown",
                    "URL": row.get("source_url") or "",
                }
                for row in response.data
            ]
        )

    def get_price_history(
        self,
        asset_id: str,
        ticker: str,
        limit: int = 50,
    ) -> pd.DataFrame:
        if self.client is None:
            return get_mock_prices(ticker)

        response = (
            self.client.table("market_prices")
            .select("observed_at,adjusted_close")
            .eq("asset_id", asset_id)
            .eq("interval", "1d")
            .order("observed_at", desc=True)
            .limit(limit)
            .execute()
        )
        frame = pd.DataFrame(response.data)
        if frame.empty:
            return frame
        frame = frame.rename(
            columns={"observed_at": "date", "adjusted_close": "close"}
        )
        frame["date"] = pd.to_datetime(frame["date"])
        return frame.sort_values("date")

    def get_quality_summary(self) -> dict[str, int]:
        articles = self.list_articles(limit=500)
        return {
            "article_count": len(articles),
            "missing_summaries": sum(not item.summary.strip() for item in articles),
            "unreviewed_leakage": sum(
                item.leakage_status == "not_reviewed" for item in articles
            ),
            "ticker_count": len({item.ticker for item in articles}),
        }
