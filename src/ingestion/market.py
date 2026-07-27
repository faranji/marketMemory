"""Daily TUPRS.IS and XU100.IS price collection for the initial MVP."""
from datetime import date
import pandas as pd

def download_daily_prices(symbols:list[str],start_date:date,end_date:date)->pd.DataFrame:
    # TODO: yfinance.download(auto_adjust=False), inspect columns, flatten MultiIndex, one row per symbol/date.
    # Validate duplicate symbol/date, adjusted_close>0, and missing business dates.
    # Save local raw file before Supabase upload.
    raise NotImplementedError
