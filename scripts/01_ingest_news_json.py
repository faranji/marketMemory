from __future__ import annotations

import argparse
from pathlib import Path
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
    """Flatten common news JSON envelopes without deleting the raw payload."""
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]

    if not isinstance(payload, dict):
        return []

    for key in ("feed", "articles", "results", "data", "items"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]

    return [payload]


def guess_external_id(item: dict[str, Any]) -> str | None:
    for key in ("id", "article_id", "external_id", "uuid", "url"):
        value = item.get(key)
        if value:
            return str(value)
    return None


def guess_url(item: dict[str, Any]) -> str | None:
    for key in ("url", "webUrl", "web_url", "canonical_url"):
        value = item.get(key)
        if value:
            return str(value)
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Load raw news JSON into Supabase."
    )
    parser.add_argument("--path", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--batch-size", type=int, default=250)
    args = parser.parse_args()

    client = get_backend_client()
    run_id = create_ingestion_run(
        client, "news", args.source, args.path
    )

    seen = inserted = failed = 0
    rows: list[dict[str, Any]] = []

    try:
        for file_path in iter_json_files(args.path):
            payload = load_json(file_path)
            for item in extract_items(payload):
                seen += 1
                payload_hash = json_hash(item)
                rows.append(
                    {
                        "id": deterministic_uuid(
                            f"raw-news:{args.source}:{payload_hash}"
                        ),
                        "ingestion_run_id": run_id,
                        "source_name": args.source,
                        "external_id": guess_external_id(item),
                        "source_url": guess_url(item),
                        "payload": item,
                        "payload_hash": payload_hash,
                        "processing_status": "pending",
                    }
                )

        for group in batch(rows, args.batch_size):
            try:
                (
                    client.table("raw_news_items")
                    .upsert(
                        group,
                        on_conflict="source_name,payload_hash",
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
