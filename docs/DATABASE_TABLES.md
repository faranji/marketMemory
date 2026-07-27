# Supabase Table Map

| Table | Purpose |
|---|---|
| ingestion_runs | one import execution |
| raw_source_items | immutable raw source records |
| assets / aliases / sectors | reference data |
| event_categories | event taxonomy |
| trading_sessions | BIST calendar |
| market_events | cleaned KAP events |
| event_assets | event-company mapping |
| market_prices | TUPRS/XU100 daily prices |
| macro_series / observations | Brent and USDTRY |
| event_features | pre-event context |
| event_outcomes | 1D/3D/5D future labels |
| model_versions / event_embeddings | NLP versions and vectors |
| analysis_runs / horizons / historical_analogues | presented analyses |
| social_signals | future YouTube/X aggregates |
| data_quality_checks | validation records |
