from __future__ import annotations

import argparse
from datetime import datetime, timezone
from typing import Any

from _common import (
    batch,
    create_ingestion_run,
    deterministic_uuid,
    finish_ingestion_run,
    get_backend_client,
    iter_json_files,
    json_hash,
    load_json,
)


def extract_items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []

    for key in ("prices", "bars", "data", "values", "results"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]

    return [payload]


def first_value(item: dict[str, Any], names: tuple[str, ...]) -> Any:
    for name in names:
        if item.get(name) is not None:
            return item[name]
    return None


def normalise_timestamp(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc).isoformat()
    return str(value)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Load raw market-price JSON into Supabase."
    )
    parser.add_argument("--path", required=True)
    parser.add_argument("--provider", required=True)
    parser.add_argument("--ticker", default=None)
    parser.add_argument("--interval", default="1d")
    parser.add_argument("--batch-size", type=int, default=500)
    args = parser.parse_args()

    client = get_backend_client()
    run_id = create_ingestion_run(
        client, "market", args.provider, args.path
    )

    seen = inserted = failed = 0
    rows: list[dict[str, Any]] = []

    try:
        for file_path in iter_json_files(args.path):
            payload = load_json(file_path)
            for item in extract_items(payload):
                seen += 1
                ticker = args.ticker or first_value(
                    item, ("ticker", "symbol", "asset")
                )
                observed_at = normalise_timestamp(
                    first_value(
                        item,
                        ("observed_at", "timestamp", "date", "session_date"),
                    )
                )
                if not ticker or not observed_at:
                    failed += 1
                    continue

                payload_hash = json_hash(item)
                record_key = (
                    f"raw-market:{args.provider}:{ticker}:"
                    f"{args.interval}:{observed_at}:{payload_hash}"
                )
                rows.append(
                    {
                        "id": deterministic_uuid(record_key),
                        "ingestion_run_id": run_id,
                        "provider": args.provider,
                        "ticker": str(ticker),
                        "interval": args.interval,
                        "observed_at": observed_at,
                        "payload": item,
                        "payload_hash": payload_hash,
                        "processing_status": "pending",
                    }
                )

        for group in batch(rows, args.batch_size):
            try:
                (
                    client.table("raw_market_bars")
                    .upsert(
                        group,
                        on_conflict=(
                            "provider,ticker,interval,observed_at,payload_hash"
                        ),
                        ignore_duplicates=True,
                    )
                    .execute()
                )
                inserted += len(group)
                print(f"Inserted/upserted: {inserted}/{seen}")
            except Exception as exc:
                failed += len(group)
                print(f"Batch failed: {exc}")

        finish_ingestion_run(
            client,
            run_id,
            status="completed" if failed == 0 else "partial",
            records_seen=seen,
            records_inserted=inserted,
            records_failed=failed,
        )
    except Exception as exc:
        finish_ingestion_run(
            client,
            run_id,
            status="failed",
            records_seen=seen,
            records_inserted=inserted,
            records_failed=max(failed, seen - inserted),
            error_message=str(exc),
        )
        raise


if __name__ == "__main__":
    main()
