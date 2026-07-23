# 📈 Market Memory 

Market Memory is a regime-aware and explainable machine learning (Decision-Support) system that predicts the short and medium-term impacts of financial news on stock prices. This project aims to predict the Cumulative Abnormal Return (CAR) at 1, 3, 5, 10, and 20 trading days following a news event.

By design, instead of providing strict buy/sell (investment) advice, it offers data-backed insights by semantically finding similar past events.

## ✨ Key Features

* **Multi-Horizon Prediction:** Modeling the impact of news across 1, 3, 5, 10, and 20-day trading horizons (CAR).
* **Semantic Memory:** Comparing incoming news with past financial news (analogues) using TF-IDF and SBERT (Sentence-BERT) to find the nearest K-neighbors (KNN).
* **Market Regime Awareness:** Incorporating the overall market state into the analysis using metrics like the VIX (fear) level, SPY momentum, and stock volatility (volume z-score)[cite: 1].
* **Hybrid ML Architecture:** Utilizing Logistic Regression (baseline) for fundamental analysis and XGBoost algorithms for final classification/regression predictions[cite: 1].
* **Explainability and Calibration:** Validating the model's prediction probabilities with calibration curves (Brier score) and presenting them to the user[cite: 1].
* **Interactive Terminal:** A user-friendly interface developed with Streamlit, displaying the news feed, CAR trajectory, and neighbor distributions[cite: 1].

## 🛠️ Technologies and Data Sources

* **Languages & Frameworks:** Python, Scikit-Learn, XGBoost, Streamlit, Pandas[cite: 1].
* **NLP (Natural Language Processing):** SBERT (Semantic Similarity), FinBERT (Financial Sentiment Analysis)[cite: 1].
* **Data Sources:** 
  * News Feed: Alpha Vantage API[cite: 1].
  * Market Data (OHLCV): Yahoo Finance[cite: 1].


## Supabase sırası

1. Yeni bir Supabase projesi aç.
2. `sql/schema.sql` çalıştır.
3. `sql/seed_assets.sql` çalıştır.
4. `.env.example` → `.env` kopyala; backend secret key ekle.
5. JSON dosyalarını `data/raw/news` ve `data/raw/market` altına koy.
6. Ham ingestion scriptlerini çalıştır.
7. Temizleme, etiket, embedding ve model scriptlerini sırayla geliştir.
8. `.streamlit/secrets.toml.example` → `.streamlit/secrets.toml` kopyala.
9. Publishable key ekle ve `USE_MOCK_DATA=false` yap.
