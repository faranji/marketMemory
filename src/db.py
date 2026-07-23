from __future__ import annotations

import streamlit as st
from supabase import Client, create_client

from src.config import get_settings


@st.cache_resource(show_spinner=False)
def get_supabase_client() -> Client | None:
    settings = get_settings()

    if settings.use_mock_data:
        return None
    if not settings.supabase_url or not settings.supabase_key:
        return None

    return create_client(settings.supabase_url, settings.supabase_key)
