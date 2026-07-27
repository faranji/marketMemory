"""Separate USDTRY and Brent collectors. Each produces date/value before any join."""
from datetime import date
import pandas as pd

def download_usdtry(start_date:date,end_date:date)->pd.DataFrame:
    # TODO: read EVDS_API_KEY, save raw response, normalize observed_date/value/provider/series_code.
    raise NotImplementedError

def download_brent(start_date:date,end_date:date)->pd.DataFrame:
    # TODO: read EIA_API_KEY, save raw response, normalize observed_date/value/provider/series_code.
    raise NotImplementedError
