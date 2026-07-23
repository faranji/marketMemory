from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go


def build_prediction_chart(
    prices: pd.DataFrame,
    predictions: pd.DataFrame,
) -> go.Figure:
    fig = go.Figure()

    if prices.empty or predictions.empty:
        fig.update_layout(template="plotly_dark", height=500, title="No chart data")
        return fig

    history = prices.sort_values("date").copy()
    last_date = pd.Timestamp(history["date"].iloc[-1])
    last_price = float(history["close"].iloc[-1])

    fig.add_trace(
        go.Scatter(
            x=history["date"],
            y=history["close"],
            mode="lines",
            name="Historical price",
            line={"width": 2},
        )
    )

    days = (
        predictions["Horizon"]
        .str.replace("D", "", regex=False)
        .astype(int)
        .to_numpy()
    )
    future_dates = [
        last_date + pd.tseries.offsets.BDay(int(day))
        for day in days
    ]

    expected = predictions["Expected abnormal return (%)"].to_numpy(float)
    lower = predictions["Lower bound (%)"].to_numpy(float)
    upper = predictions["Upper bound (%)"].to_numpy(float)

    x_future = [last_date] + future_dates
    median_prices = np.r_[last_price, last_price * (1 + expected / 100)]
    lower_prices = np.r_[last_price, last_price * (1 + lower / 100)]
    upper_prices = np.r_[last_price, last_price * (1 + upper / 100)]

    fig.add_trace(
        go.Scatter(
            x=x_future,
            y=upper_prices,
            mode="lines",
            line={"width": 0},
            hoverinfo="skip",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_future,
            y=lower_prices,
            mode="lines",
            line={"width": 0},
            fill="tonexty",
            fillcolor="rgba(66,211,146,0.16)",
            name="Historical analogue range",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_future,
            y=median_prices,
            mode="lines+markers",
            name="Median projected path",
            line={"width": 2, "dash": "dash"},
        )
    )

    fig.add_vline(
        x=last_date.timestamp() * 1000,
        line_dash="dot",
        annotation_text="News event",
    )

    fig.update_layout(
        template="plotly_dark",
        height=510,
        title="Historical Price and Multi-Horizon Analogue Range",
        xaxis_title=None,
        yaxis_title="Price / modelled path",
        hovermode="x unified",
        legend={"orientation": "h", "y": 1.08},
        margin={"l": 10, "r": 10, "t": 50, "b": 10},
    )
    return fig


def build_analogue_paths_chart(analogues: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    if analogues.empty:
        fig.update_layout(
            template="plotly_dark",
            height=420,
            title="No analogue data",
        )
        return fig

    horizons = [0, 1, 5, 20]
    for _, row in analogues.head(12).iterrows():
        values = [
            0.0,
            float(row["1D abnormal return (%)"]),
            float(row["5D abnormal return (%)"]),
            float(row["20D abnormal return (%)"]),
        ]
        fig.add_trace(
            go.Scatter(
                x=horizons,
                y=values,
                mode="lines",
                opacity=0.28,
                showlegend=False,
                hovertemplate=(
                    f'{row["Historical event"]}<br>'
                    "Day %{x}: %{y:.2f}%<extra></extra>"
                ),
            )
        )

    median = [
        0.0,
        analogues["1D abnormal return (%)"].median(),
        analogues["5D abnormal return (%)"].median(),
        analogues["20D abnormal return (%)"].median(),
    ]
    fig.add_trace(
        go.Scatter(
            x=horizons,
            y=median,
            mode="lines+markers",
            name="Median analogue response",
            line={"width": 4},
        )
    )
    fig.add_hline(y=0, line_dash="dot")
    fig.update_layout(
        template="plotly_dark",
        height=430,
        title="How Similar Historical Events Evolved",
        xaxis_title="Trading day after event",
        yaxis_title="Abnormal return (%)",
        margin={"l": 10, "r": 10, "t": 50, "b": 10},
    )
    return fig
