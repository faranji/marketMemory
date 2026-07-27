# Implementation Guide

Every stage follows the same learning format.

## 1. KAP discovery
**Objective:** obtain a stable list of detail URLs.
**Why:** the list page is discovery metadata, not sufficient NLP text.
**Input:** one selected TUPRS year.
**Output:** deduplicated URL CSV plus screenshot/HTML.
**Test:** every URL opens one detail page; no duplicate disclosure IDs.

## 2. Detail scraping
**Objective:** preserve complete source evidence.
**Input:** verified detail URLs.
**Output:** raw HTML, visible text, metadata JSONL.
**Test:** timestamp, publisher, title, source URL and revision flags exist.

## 3. Raw database upload
**Objective:** make collection idempotent.
**Input:** local JSONL.
**Output:** raw_source_items and ingestion_runs.
**Test:** rerunning the same file does not create a duplicate.

## 4. Clean-event promotion
**Objective:** create provider-independent events.
**Input:** pending raw records.
**Output:** market_events and event_assets.
**Test:** source traceability remains; body text is readable.

## 5. Event classification
**Objective:** create a trustworthy event taxonomy.
**Input:** reviewed clean events.
**Output:** category, method, confidence and review flag.
**Test:** uncertain events abstain instead of receiving forced labels.

## 6. Market and macro sources
**Objective:** create comparable daily series.
**Input:** yfinance, EVDS and EIA raw responses.
**Output:** market_prices and macro_observations.
**Test:** units, dates, duplicates and missing values are documented.

## 7. Session alignment
**Objective:** determine the first full session that can reflect an event.
**Input:** publication timestamp plus trading_sessions.
**Output:** publication_session and effective_session_date.
**Test:** before-open, in-session, Friday-after-close, weekend and holiday examples.

## 8. Pre-event features
**Objective:** describe the known market context without leakage.
**Input:** clean event, prior prices and prior macro values.
**Output:** lagged returns, volatility, relative volume and regimes.
**Test:** changing the event-day close cannot change a pre-event feature.

## 9. Future labels
**Objective:** measure historical outcomes.
**Input:** effective session and future trading prices.
**Output:** TUPRS, XU100 and abnormal returns for 1D/3D/5D.
**Test:** horizons count sessions, not calendar days.

## 10. NLP representation
**Objective:** represent Turkish disclosures consistently.
**Input:** title, summary, cleaned body and category.
**Output:** text representation and embedding vector.
**Test:** dimensions match schema and model version is stored.

## 11. Historical retrieval
**Objective:** find comparable earlier events.
**Input:** query embedding, earlier events and pre-event context.
**Output:** ranked analogues and human-readable reasons.
**Test:** no candidate is later than the query; labels do not affect selection.

## 12. Confidence and abstention
**Objective:** communicate evidence strength.
**Input:** analogue count, similarity, outcome consistency, completeness and regime match.
**Output:** confidence label and abstention reason.
**Test:** weak or missing evidence produces insufficient evidence.

## 13. Evaluation
**Objective:** demonstrate that the system works beyond attractive examples.
**Input:** chronological train/validation/test periods.
**Output:** retrieval relevance, calibration, baseline metrics, coverage and errors.
**Test:** no temporal overlap or revision leakage.

## 14. Streamlit
**Objective:** present evidence, not trigger the data pipeline.
**Input:** reviewed/completed Supabase rows.
**Output:** Overview, Event Analysis, Analogues and Methodology pages.
**Test:** source, uncertainty, missing data and disclaimer are visible.

## 15. Social extension
**Objective:** measure whether attention/sentiment adds value.
**Input:** timestamped authorised YouTube/X data.
**Output:** daily pre-event social features.
**Test:** ablation A/B/C on identical chronological splits.
