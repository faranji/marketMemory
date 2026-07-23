# Market Memory Veritabanı Sözleşmesi

Bu şema, veri gelmeden önce belirlenmelidir. Böylece scraper, fiyat indirici,
etiketleme scripti, model ve Streamlit aynı isimleri ve ilişkileri kullanır.

## Katman 1 — Ham veri

### `ingestion_runs`
Her veri yükleme çalışmasının günlüğüdür. Hangi dosya, kaynak, kaç kayıt ve hata
olduğu burada tutulur.

### `raw_news_items`
Haber API'sinden veya scraper'dan gelen JSON nesnesini değiştirmeden `payload`
alanında saklar. Ham kayıtlar elle düzeltilmez.

### `raw_market_bars`
Piyasa sağlayıcısından gelen her fiyat barının ham JSON karşılığını saklar.

## Katman 2 — Temiz referans ve içerik

### `assets`
GOOGL, TSLA, NVDA ve QQQ gibi varlıkların ana tablosudur. Bir varlığın benchmark'ı
aynı tablodaki başka bir varlığa bağlanır.

### `event_clusters`
Aynı gerçek olayı anlatan farklı haberleri tek olay grubunda toplar.

### `news_articles`
Temiz ve analiz edilebilir haber kaydıdır. Başlık, özet, kesin zaman, canonical URL,
leakage etiketi ve birincil varlık burada bulunur.

### `article_assets`
Bir haberin birden fazla varlıkla ilişkisini tutar. Bu nedenle `news_articles`
tablosuna tek bir ticker sıkıştırılmaz.

### `market_prices`
Temiz OHLCV fiyat tablosudur. Model ve Streamlit bu tablodan okur.

## Katman 3 — Öğrenme etiketleri

### `article_asset_labels`
Bir haber–varlık çifti için 1/3/5/10/20 günlük getiri, benchmark getirisi,
abnormal return, zirve günü, tersine dönüş ve etki şekli burada tutulur.

Bu tablo modelin hedef değişkenidir.

## Katman 4 — ML varlıkları

### `model_versions`
Embedding, sınıflandırma, regresyon ve hibrit modellerin sürüm ve ölçümlerini tutar.

### `news_embeddings`
Haber vektörlerini saklar. MVP için 384 boyutlu sentence-transformer varsayılmıştır.

### `model_evaluations`
Her modelin zaman bazlı test sonuçlarını saklar.

## Katman 5 — Uygulama sonuçları

### `prediction_runs`
Bir haber ve varlık için yapılan analiz çalışmasının üst kaydıdır.

### `prediction_horizons`
Aynı çalışmanın 1/3/5/10/20 günlük yön, olasılık ve yüzde tahminlerini tutar.

### `historical_analogues`
Tahminde kullanılan geçmiş olayları, sıralarını, benzerliklerini ve gerçekleşmiş
etkilerini saklar.

## Streamlit neyi okur?

- `assets`
- `news_articles`
- `article_assets`
- `market_prices`
- `model_versions`
- `prediction_runs`
- `prediction_horizons`
- `historical_analogues`

## Streamlit neyi okumaz?

- `raw_news_items`
- `raw_market_bars`
- `article_asset_labels`
- `news_embeddings`
- `model_evaluations`
- `ingestion_runs`

Bu ayrım ham ve model-içi verilerin arayüzden gereksiz yere açılmasını engeller.
