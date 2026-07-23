from __future__ import annotations

import os
from dataclasses import dataclass

import streamlit as st
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    use_mock_data: bool
    supabase_url: str | None
    supabase_key: str | None


def _to_bool(value: object, default: bool = True) -> bool:
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def get_settings() -> Settings:
    """Read Streamlit secrets first and environment variables second."""
    secret_mock = st.secrets.get("USE_MOCK_DATA", None)

    supabase_secret = st.secrets.get("supabase", {})
    secret_url = supabase_secret.get("url") if supabase_secret else None
    secret_key = supabase_secret.get("key") if supabase_secret else None

    return Settings(
        use_mock_data=_to_bool(
            secret_mock if secret_mock is not None else os.getenv("USE_MOCK_DATA"),
            default=True,
        ),
        supabase_url=secret_url or os.getenv("SUPABASE_URL"),
        supabase_key=secret_key or os.getenv("SUPABASE_KEY"),
    )
