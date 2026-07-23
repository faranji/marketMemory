from __future__ import annotations

import pandas as pd
import streamlit as st

from src.charts import build_analogue_paths_chart, build_prediction_chart
from src.repository import MarketMemoryRepository
from src.ui import (
    inject_styles,
    render_disclaimer,
    render_event_card,
    render_header,
    render_horizon_table,
    render_metric_cards,
)

inject_styles()
repo = MarketMemoryRepository()
articles = repo.list_articles(limit=50)

if not articles:
    st.error(
        "Haber bulunamadı. Supabase'i seed edin veya USE_MOCK_DATA=true yapın."
    )
    st.stop()

render_header(repo.mode)

with st.sidebar:
    st.markdown("## Analysis Controls")
    labels = {
        article.id: f"{article.ticker} · {article.title[:58]}"
        for article in articles
    }
    selected_id = st.selectbox(
        "Breaking news event",
        options=list(labels),
        format_func=lambda value: labels[value],
    )
    article = next(item for item in articles if item.id == selected_id)

    article_assets = repo.list_assets_for_article(article.id)
    if not article_assets:
        st.error("Bu haberle ilişkilendirilmiş varlık bulunamadı.")
        st.stop()

    asset_map = {
        asset.id: f"{asset.ticker} · {asset.asset_name}"
        for asset in article_assets
    }
    selected_asset_id = st.selectbox(
        "Target asset",
        options=list(asset_map),
        format_func=lambda value: asset_map[value],
    )
    asset = next(item for item in article_assets if item.id == selected_asset_id)

    primary_horizon = st.select_slider(
        "Primary horizon",
        options=[1, 3, 5, 10, 20],
        value=5,
        format_func=lambda value: f"{value} trading day{'s' if value > 1 else ''}",
    )
    max_analogues = st.slider("Maximum historical analogues", 5, 30, 12)
    similarity_threshold = st.slider(
        "Minimum combined similarity",
        0.50,
        0.95,
        0.70,
        0.01,
    )
    minimum_evidence = st.number_input(
        "Minimum evidence count",
        3,
        20,
        8,
        1,
    )
    st.button("Analyse selected event", type="primary", use_container_width=True)
    st.divider()
    st.caption(f"Data mode: {repo.mode}")

render_event_card(article)
render_disclaimer()

predictions = repo.get_predictions(article.id, asset.id)
analogues = repo.get_analogues(article.id, asset.id, max_analogues)

if not analogues.empty:
    analogues = analogues[
        pd.to_numeric(analogues["Combined similarity"]) >= similarity_threshold
    ].copy()

render_metric_cards(predictions, len(analogues))

if len(analogues) < minimum_evidence:
    st.warning(
        f"Yalnızca {len(analogues)} tarihsel olay eşik değerini geçti. "
        "Sistem güçlü sinyal vermemelidir."
    )

overview_tab, analogues_tab, raw_tab = st.tabs(
    ["Overview", "Historical Analogues", "Raw Outputs"]
)

with overview_tab:
    chart_col, horizon_col = st.columns([1.65, 1])
    with chart_col:
        prices = repo.get_price_history(asset.id, asset.ticker, 50)
        st.plotly_chart(
            build_prediction_chart(prices, predictions),
            use_container_width=True,
        )
    with horizon_col:
        st.markdown("#### Multi-Horizon Estimate")
        render_horizon_table(predictions)
        selected = predictions[
            predictions["Horizon"] == f"{primary_horizon}D"
        ]
        if not selected.empty:
            row = selected.iloc[0]
            st.metric(
                f"{primary_horizon}-day abnormal return",
                f'{float(row["Expected abnormal return (%)"]):+.2f}%',
            )
            st.write(
                f"Direction: **{row['Direction']}**  \n"
                f"Model probability: **{float(row['Probability']):.0%}**"
            )

with analogues_tab:
    st.plotly_chart(
        build_analogue_paths_chart(analogues),
        use_container_width=True,
    )
    if analogues.empty:
        st.info("Benzerlik eşiğini geçen tarihsel olay bulunamadı.")
    else:
        display = analogues.copy()
        for column in [
            "Text similarity",
            "Regime similarity",
            "Combined similarity",
        ]:
            display[column] = display[column].map(
                lambda value: f"{float(value):.3f}"
            )
        for column in [
            "1D abnormal return (%)",
            "5D abnormal return (%)",
            "20D abnormal return (%)",
        ]:
            display[column] = display[column].map(
                lambda value: f"{float(value):+.2f}%"
            )
        st.dataframe(
            display,
            hide_index=True,
            use_container_width=True,
            column_config={"URL": st.column_config.LinkColumn("Source")},
        )

with raw_tab:
    st.dataframe(predictions, hide_index=True, use_container_width=True)
    st.dataframe(analogues, hide_index=True, use_container_width=True)
