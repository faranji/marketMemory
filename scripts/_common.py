from __future__ import annotations

import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()


def get_backend_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SECRET_KEY")
    if not url or not key:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_SECRET_KEY must be set in .env."
        )
    return create_client(url, key)


def deterministic_uuid(value: str) -> str:
    """Return the same UUID whenever the same logical record is processed."""
    return str(uuid.uuid5(uuid.NAMESPACE_URL, value))


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def json_hash(payload: Any) -> str:
    stable = json.dumps(
        payload,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
        default=str,
    )
    return hashlib.sha256(stable.encode("utf-8")).hexdigest()


def iter_json_files(path: str) -> Iterable[Path]:
    target = Path(path)
    if target.is_file() and target.suffix.lower() == ".json":
        yield target
        return
    if target.is_dir():
        yield from sorted(target.rglob("*.json"))
        return
    raise FileNotFoundError(f"No JSON file or directory found at: {target}")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def batch(items: list[dict[str, Any]], size: int) -> Iterable[list[dict[str, Any]]]:
    for start in range(0, len(items), size):
        yield items[start:start + size]


def create_ingestion_run(
    client: Client,
    source_type: str,
    source_name: str,
    input_path: str,
) -> str:
    response = (
        client.table("ingestion_runs")
        .insert(
            {
                "source_type": source_type,
                "source_name": source_name,
                "status": "running",
                "input_path": input_path,
            }
        )
        .execute()
    )
    return str(response.data[0]["id"])


def finish_ingestion_run(
    client: Client,
    run_id: str,
    *,
    status: str,
    records_seen: int,
    records_inserted: int,
    records_failed: int,
    error_message: str | None = None,
) -> None:
    (
        client.table("ingestion_runs")
        .update(
            {
                "status": status,
                "finished_at": utc_now_iso(),
                "records_seen": records_seen,
                "records_inserted": records_inserted,
                "records_failed": records_failed,
                "error_message": error_message,
            }
        )
        .eq("id", run_id)
        .execute()
    )
