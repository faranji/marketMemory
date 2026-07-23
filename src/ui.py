from __future__ import annotations

import html

import pandas as pd
import streamlit as st


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 3rem;
            max-width: 1480px;
        }
        [data-testid="stSidebar"] {
            border-right: 1px solid #202936;
        }
        .terminal-header {
            border: 1px solid #202936;
            border-radius: 14px;
            padding: 18px 20px;
            background: linear-gradient(135deg, #101722 0%, #0B1017 100%);
            margin-bottom: 14px;
        }
        .terminal-title {
            font-size: 1.75rem;
            font-weight: 800;
            letter-spacing: .02em;
        }
        .terminal-subtitle {
            color: #8E9AAA;
            margin-top: 4px;
        }
        .pill {
            display: inline-block;
            border: 1px solid #2A3948;
            border-radius: 999px;
            padding: 5px 10px;
            font-size: .76rem;
            margin-right: 6px;
            color: #B8C5D1;
        }
        .live {
            color: #53E095;
            border-color: #275B43;
            background: #10291F;
        }
        .event-card {
            border: 1px solid #202936;
            border-radius: 14px;
            padding: 20px;
            background: #10161E;
            margin-bottom: 14px;
        }
        .event-kicker {
            color: #42D392;
            font-size: .75rem;
            font-weight: 700;
            letter-spacing: .11em;
        }
        .event-title {
            font-size: 1.45rem;
            line-height: 1.25;
            font-weight: 750;
            margin: 8px 0;
        }
        .muted { color: #8E9AAA; }
        .metric-card {
            border: 1px solid #202936;
            border-radius: 12px;
            padding: 15px 16px;
            background: #111820;
            min-height: 118px;
        }
        .metric-label {
            color: #8E9AAA;
            font-size: .72rem;
            letter-spacing: .08em;
            text-transform: uppercase;
        }
        .metric-value {
            font-size: 1.55rem;
            font-weight: 800;
            margin-top: 8px;
        }
        .metric-note {
            color: #8694A3;
            font-size: .76rem;
            margin-top: 5px;
        }
        .up { color: #53E095; }
        .down { color: #FF6B75; }
        .neutral { color: #F0C75E; }
        .disclaimer {
            border: 1px solid #493F23;
            background: #201C10;
            color: #D9C68A;
            border-radius: 10px;
            padding: 11px 13px;
            font-size: .82rem;
            margin-bottom: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(mode: str) -> None:
    live_class = "live" if mode == "SUPABASE" else ""
    st.markdown(
        f"""
        <div class="terminal-header">
          <div style="display:flex;justify-content:space-between;gap:20px;align-items:center;">
            <div>
              <div class="terminal-title">MARKET MEMORY</div>
              <div class="terminal-subtitle">
                Leakage-aware, regime-aware historical news impact terminal
              </div>
            </div>
            <div style="text-align:right;">
              <span class="pill {live_class}">● {html.escape(mode)}</span>
              <span class="pill">MVP RESEARCH TERMINAL</span>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_event_card(article: object) -> None:
    timestamp = article.published_at.strftime("%d %b %Y · %H:%M UTC")
    st.markdown(
        f"""
        <div class="event-card">
          <div class="event-kicker">
            SELECTED EVENT · {html.escape(article.ticker)}
          </div>
          <div class="event-title">{html.escape(article.title)}</div>
          <div class="muted">
            {html.escape(article.source)} · {timestamp} · {html.escape(article.topic)}
          </div>
          <p style="margin-top:14px;line-height:1.55;">
            {html.escape(article.summary)}
          </p>
          <span class="pill">{html.escape(article.leakage_status)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_disclaimer() -> None:
    st.markdown(
        """
        <div class="disclaimer">
          Araştırma prototipidir. Çıktılar geçmiş benzer olaylara dayalı tahminlerdir;
          garanti veya yatırım tavsiyesi değildir. Özellikle 20 günlük sonuçlar sonraki
          rakip olaylardan güçlü biçimde etkilenebilir.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_cards(predictions: pd.DataFrame, analogue_count: int) -> None:
    if predictions.empty:
        st.warning("Bu haber ve ticker için tahmin satırı bulunamadı.")
        return

    row_5d = predictions[predictions["Horizon"] == "5D"]
    selected = row_5d.iloc[0] if not row_5d.empty else predictions.iloc[0]

    direction = str(selected["Direction"])
    css_class = {"UP": "up", "DOWN": "down"}.get(direction, "neutral")
    probability = float(selected["Probability"])
    expected = float(selected["Expected abnormal return (%)"])
    lower = float(selected["Lower bound (%)"])
    upper = float(selected["Upper bound (%)"])

    reliability = "LOW"
    if analogue_count >= 20 and probability >= 0.65:
        reliability = "HIGH"
    elif analogue_count >= 8:
        reliability = "MODERATE"

    cards = [
        ("5D DIRECTION", direction, css_class, "Market-adjusted direction"),
        ("MODEL PROBABILITY", f"{probability:.0%}", css_class, "Must be calibrated"),
        ("EXPECTED 5D RETURN", f"{expected:+.2f}%", css_class, "Versus benchmark"),
        ("EVIDENCE", reliability, "neutral", f"{analogue_count} historical events"),
    ]

    for column, card in zip(st.columns(4), cards):
        label, value, value_class, note = card
        column.markdown(
            f"""
            <div class="metric-card">
              <div class="metric-label">{label}</div>
              <div class="metric-value {value_class}">{value}</div>
              <div class="metric-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.caption(f"5D historical range: {lower:+.2f}% to {upper:+.2f}%.")


def render_horizon_table(predictions: pd.DataFrame) -> None:
    display = predictions.copy()
    display["Probability"] = display["Probability"].map(
        lambda value: f"{float(value):.0%}"
    )
    for column in [
        "Expected abnormal return (%)",
        "Lower bound (%)",
        "Upper bound (%)",
    ]:
        display[column] = display[column].map(
            lambda value: f"{float(value):+.2f}%"
        )
    st.dataframe(display, hide_index=True, use_container_width=True)
