from __future__ import annotations

import argparse
from datetime import datetime, timezone
from typing import Any

from _common import batch, deterministic_uuid, get_backend_client


def first_value(item: dict[str, Any], names: tuple[str, ...]) -> Any:
    for name in names:
        if item.get(name) is not None:
            return item[name]
    return None


def as_float(value: Any) -> float | None:
    if value in (None, "", "null"):
        return None
    return float(value)


def normalise_timestamp(value: Any) -> str:
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc).isoformat()
    text = str(value)
    if len(text) == 10:
        return f"{text}T00:00:00+00:00"
    return text


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Promote generic raw market bars into market_prices."
    )
    parser.add_argument("--provider", required=True)
    parser.add_argument("--limit", type=int, default=5000)
    parser.add_argument("--batch-size", type=int, default=500)
    args = parser.parse_args()

    client = get_backend_client()
    raw_response = (
        client.table("raw_market_bars")
        .select("id,ticker,interval,observed_at,payload")
        .eq("provider", args.provider)
        .eq("processing_status", "pending")
        .limit(args.limit)
        .execute()
    )
    asset_response = client.table("assets").select("id,ticker").execute()
    asset_ids = {
        str(row["ticker"]): str(row["id"])
        for row in asset_response.data
    }

    rows: list[dict[str, Any]] = []
    promoted_raw_ids: list[str] = []

    for raw in raw_response.data:
        item = raw["payload"]
        ticker = str(raw["ticker"])
        asset_id = asset_ids.get(ticker)
        if not asset_id:
            continue

        observed_at = normalise_timestamp(raw["observed_at"])
        close_value = first_value(item, ("adjusted_close", "adj_close", "close"))
        if close_value is None:
            continue

        row_id = deterministic_uuid(
            f"market-price:{asset_id}:{args.provider}:"
            f"{raw['interval']}:{observed_at}"
        )
        rows.append(
            {
                "id": row_id,
                "raw_market_bar_id": raw["id"],
                "asset_id": asset_id,
                "provider": args.provider,
                "interval": raw["interval"],
                "observed_at": observed_at,
                "open": as_float(first_value(item, ("open", "Open"))),
                "high": as_float(first_value(item, ("high", "High"))),
                "low": as_float(first_value(item, ("low", "Low"))),
                "close": as_float(first_value(item, ("close", "Close"))),
                "adjusted_close": as_float(close_value),
                "volume": as_float(first_value(item, ("volume", "Volume"))),
                "is_complete": True,
            }
        )
        promoted_raw_ids.append(str(raw["id"]))

    for group in batch(rows, args.batch_size):
        (
            client.table("market_prices")
            .upsert(
                group,
                on_conflict="asset_id,provider,interval,observed_at",
            )
            .execute()
        )

    for raw_id in promoted_raw_ids:
        (
            client.table("raw_market_bars")
            .update({"processing_status": "promoted"})
            .eq("id", raw_id)
            .execute()
        )

    print(f"Promoted {len(rows)} clean market-price rows.")


if __name__ == "__main__":
    main()
