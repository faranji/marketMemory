# 📈 Market Memory 

Market Memory is a regime-aware and explainable machine learning (Decision-Support) system that predicts the short and medium-term impacts of financial news on stock prices. This project aims to predict the Cumulative Abnormal Return (CAR) at 1, 3, 5, 10, and 20 trading days following a news event.

By design, instead of providing strict buy/sell advice, it offers data-backed insights by semantically finding similar past events.

## Key Features

* **Multi-Horizon Prediction:** Modeling the impact of news across 1, 3, 5, 10, and 20-day trading horizons (CAR).
* **Semantic Memory:** Comparing incoming news with past financial news (analogues) using TF-IDF and SBERT (Sentence-BERT) to find the nearest K-neighbors (KNN).
* **Market Regime Awareness:** Incorporating the overall market state into the analysis using metrics like the VIX (fear) level, SPY momentum, and stock volatility (volume z-score).
* **Hybrid ML Architecture:** Utilizing Logistic Regression (baseline) for fundamental analysis and XGBoost algorithms for final classification/regression predictions.
* **Explainability and Calibration:** Validating the model's prediction probabilities with calibration curves (Brier score) and presenting them to the user.
* **Interactive Terminal:** A user-friendly interface developed with Streamlit, displaying the news feed, CAR trajectory, and neighbor distributions.

## Technologies and Data Sources

* **Languages & Frameworks:** Python, Scikit-Learn, XGBoost, Streamlit, Pandas.
* **NLP (Natural Language Processing):** SBERT (Semantic Similarity), FinBERT (Financial Sentiment Analysis).
* **Data Sources:** 
  * News Feed: Alpha Vantage API.
  * Market Data (OHLCV): Yahoo Finance.
