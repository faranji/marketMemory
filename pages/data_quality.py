from __future__ import annotations

import streamlit as st

from src.repository import MarketMemoryRepository
from src.ui import inject_styles, render_header

inject_styles()
repo = MarketMemoryRepository()
render_header(repo.mode)

st.title("Data Quality")
st.caption("Bu ekran veri hattının eksik, bozuk veya şüpheli kayıtlarını kontrol etmek içindir.")

articles = repo.list_articles(limit=500)
summary = repo.get_quality_summary()

cols = st.columns(4)
cols[0].metric("Articles", summary["article_count"])
cols[1].metric("Missing summaries", summary["missing_summaries"])
cols[2].metric("Unreviewed leakage", summary["unreviewed_leakage"])
cols[3].metric("Available tickers", summary["ticker_count"])

st.markdown("### Required checks before model training")
st.checkbox("Publication timestamps are timezone-aware", value=False)
st.checkbox("Duplicate URLs and content hashes are grouped", value=False)
st.checkbox("Market recap headlines are excluded from predictive events", value=False)
st.checkbox("Every training event has complete future price labels", value=False)
st.checkbox("Test events retrieve only earlier historical events", value=False)

st.markdown("### Articles")
st.dataframe(
    [
        {
            "ID": item.id,
            "Ticker": item.ticker,
            "Published": item.published_at,
            "Source": item.source,
            "Topic": item.topic,
            "Leakage": item.leakage_status,
            "Title": item.title,
        }
        for item in articles
    ],
    hide_index=True,
    use_container_width=True,
)
