# Data Flow

```text
KAP list → detail URLs → rendered HTML/text → local cache → raw_source_items → market_events → event_assets
TUPRS/XU100 prices → market_prices
USDTRY/Brent → macro_observations
clean events + lagged context → event_features
future 1D/3D/5D prices → event_outcomes
event text → embeddings → older candidates → reranking → historical_analogues → confidence/abstention → Streamlit
```

Every stage must create an inspectable output before the next stage starts.
