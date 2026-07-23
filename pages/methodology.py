from __future__ import annotations

import streamlit as st

from src.ui import inject_styles

inject_styles()

st.title("Methodology")
st.caption("MVP'nin ürettiği sayıların ne anlama geldiğini burada açıklayın.")

st.markdown(
    """
## Tahmin edilen şey

Sistem hissenin yalnızca ham fiyat değişimini değil, benchmark'a göre farkını tahmin eder:

**Abnormal return = stock return − benchmark return**

Örnek: GOOGL `%2` düşerken QQQ `%3.5` düştüyse, piyasa-düzeltilmiş sonuç
`+1.5%` olur.

## Zaman ufukları

Aynı haber için beş ayrı çıktı üretilir:

- 1 işlem günü
- 3 işlem günü
- 5 işlem günü
- 10 işlem günü
- 20 işlem günü

Uzun zaman ufukları daha fazla rakip olay içerdiğinden daha belirsizdir.

## Model hattı

1. Haber tarih ve saatini doğrula.
2. Fiyat yönünü zaten söyleyen market-recap haberlerini işaretle.
3. Başlık ve özeti embedding'e dönüştür.
4. Yalnızca haberden önce yayımlanmış benzer olayları getir.
5. Metin benzerliği ile piyasa rejimi benzerliğini birleştir.
6. Komşuların 1/3/5/10/20 günlük abnormal return dağılımını hesapla.
7. Sınıflandırma ile UP / NEUTRAL / DOWN üret.
8. Regresyon ile beklenen yüzde hareketi üret.
9. Kanıt zayıfsa tahmin vermekten kaçın.
10. Sonuçları walk-forward backtest ile değerlendir.

## MVP sınırı

Mock moddaki bütün sayılar yalnızca UI testi içindir. Gerçek model hattı sonuçları
Supabase tablolarına yazıldığında arayüz aynı veri sözleşmesini kullanır.
"""
)
