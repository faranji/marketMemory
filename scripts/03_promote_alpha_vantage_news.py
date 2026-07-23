from __future__ import annotations

import argparse
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from _common import batch, deterministic_uuid, get_backend_client


def parse_alpha_vantage_time(value: str) -> str:
    parsed = datetime.strptime(value, "%Y%m%dT%H%M%S")
    return parsed.replace(tzinfo=timezone.utc).isoformat()


def canonicalise_url(value: str | None) -> str | None:
    if not value:
        return None
    parts = urlsplit(value)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def choose_primary_ticker(payload: dict[str, Any]) -> str | None:
    sentiments = payload.get("ticker_sentiment") or []
    if not isinstance(sentiments, list) or not sentiments:
        return None

    ranked = sorted(
        sentiments,
        key=lambda row: float(row.get("relevance_score") or 0),
        reverse=True,
    )
    return ranked[0].get("ticker")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Promote Alpha Vantage raw news into clean tables."
    )
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--batch-size", type=int, default=200)
    args = parser.parse_args()

    client = get_backend_client()
    response = (
        client.table("raw_news_items")
        .select("id,payload")
        .eq("source_name", "alpha_vantage")
        .eq("processing_status", "pending")
        .limit(args.limit)
        .execute()
    )

    assets_response = (
        client.table("assets")
        .select("id,ticker")
        .execute()
    )
    asset_ids = {
        row["ticker"]: str(row["id"])
        for row in assets_response.data
    }

    article_rows = []
    raw_ids = []
    relation_rows = []
    for raw in response.data:
        payload = raw["payload"]
        title = payload.get("title")
        published = payload.get("time_published")
        url = canonicalise_url(payload.get("url"))
        if not title or not published or not url:
            continue

        primary_ticker = choose_primary_ticker(payload)
        article_id = deterministic_uuid(f"article:{url}")
        article_rows.append(
            {
                "id": article_id,
                "raw_news_item_id": raw["id"],
                "source_name": payload.get("source") or "alpha_vantage",
                "external_id": payload.get("url"),
                "title": title,
                "summary": payload.get("summary") or "",
                "published_at": parse_alpha_vantage_time(published),
                "url": payload.get("url"),
                "canonical_url": url,
                "primary_asset_id": asset_ids.get(primary_ticker),
                "topic": (
                    (payload.get("topics") or [{}])[0].get("topic")
                    if isinstance(payload.get("topics"), list)
                    else None
                ),
                "language": "en",
                "article_type": "news",
                "leakage_status": "not_reviewed",
                "is_active": True,
            }
        )
        raw_ids.append(raw["id"])
        if primary_ticker and asset_ids.get(primary_ticker):
            relation_rows.append(
                {
                    "article_id": article_id,
                    "asset_id": asset_ids[primary_ticker],
                    "relevance_source": "provider",
                    "relevance_score": 1.0,
                    "is_primary": True,
                }
            )

    for group in batch(article_rows, args.batch_size):
        (
            client.table("news_articles")
            .upsert(
                group,
                on_conflict="canonical_url",
            )
            .execute()
        )

    for group in batch(relation_rows, args.batch_size):
        (
            client.table("article_assets")
            .upsert(group, on_conflict="article_id,asset_id")
            .execute()
        )

    for raw_id in raw_ids:
        (
            client.table("raw_news_items")
            .update({"processing_status": "promoted"})
            .eq("id", raw_id)
            .execute()
        )

    print(f"Promoted {len(article_rows)} clean news rows.")


if __name__ == "__main__":
    main()
