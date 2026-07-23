# JSON'dan Streamlit'e Veri Akışı

## 1. Supabase projesini oluştur

Bu proje için ayrı bir Supabase projesi kullan. SQL Editor'da sırasıyla:

1. `sql/schema.sql`
2. `sql/seed_assets.sql`

dosyalarını çalıştır.

## 2. Backend secret ayarını yap

`.env.example` dosyasını `.env` adıyla kopyala:

```env
SUPABASE_URL=https://...
SUPABASE_SECRET_KEY=sb_secret_...
```

Bu secret yalnızca VS Code/Modal gibi kontrol ettiğin backend'de bulunur.

## 3. Ham haber JSON'unu yükle

```bash
python scripts/01_ingest_news_json.py \
  --path data/raw/news \
  --source alpha_vantage
```

Script:

- JSON dosyalarını bulur.
- `feed`, `articles`, `results`, `data` veya `items` listelerini açar.
- Her haberi `raw_news_items.payload` içine dokunmadan yazar.
- Aynı JSON tekrar çalıştırıldığında hash üzerinden duplicate eklemez.
- `ingestion_runs` tablosuna yükleme raporu yazar.

## 4. Ham fiyat JSON'unu yükle

```bash
python scripts/02_ingest_market_json.py \
  --path data/raw/market \
  --provider yfinance
```

Bu aşama `raw_market_bars` tablosunu doldurur.

## 5. Ham haberi temiz tabloya geçir

Alpha Vantage kullanıyorsan:

```bash
python scripts/03_promote_alpha_vantage_news.py
```

Bu script ham payload içinden başlık, özet, zaman, kaynak ve URL alanlarını çıkarıp
`news_articles` tablosuna yazar.

Sonraki haber kaynakları için ayrı adapter yazılır. Ham tablo değişmez.

## 6. Fiyatları temizle

```bash
python scripts/04_promote_market_prices.py --provider yfinance
```

Bu modül `raw_market_bars` kayıtlarını `market_prices` tablosuna dönüştürür.
Alanlar:

- asset_id
- provider
- interval
- observed_at
- open/high/low/close
- adjusted_close
- volume

## 7. Haber–varlık ilişkilerini oluştur

Provider ticker relevance bilgisi, kural tabanı veya manuel inceleme kullanılarak
`article_assets` tablosu doldurulur.

## 8. Etiketleri hesapla

Haber zamanını fiyatlarla eşleştirip `article_asset_labels` tablosuna:

- 1/3/5/10/20 günlük getiriler
- benchmark getirileri
- abnormal return
- peak day
- reversal
- impact shape

yazılır.

## 9. Embedding ve model

- Embedding modeli `model_versions` içine eklenir.
- Vektörler `news_embeddings` içine yazılır.
- Walk-forward retrieval ve ML tahminleri çalıştırılır.
- Çıktılar `prediction_runs`, `prediction_horizons`,
  `historical_analogues` tablolarına yazılır.

## 10. Streamlit

`.streamlit/secrets.toml` içinde publishable key kullanılır:

```toml
USE_MOCK_DATA = false

[supabase]
url = "https://..."
key = "sb_publishable_..."
```

Streamlit veri üretmez; hazırlanmış sonuçları okur.
