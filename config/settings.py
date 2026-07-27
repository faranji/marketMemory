"""Central non-secret settings. Keep API keys/passwords in .env only."""
from dataclasses import dataclass
from pathlib import Path
import os

PROJECT_ROOT=Path(__file__).resolve().parents[1]
DATA_DIR=PROJECT_ROOT/'data'
RAW_DIR=DATA_DIR/'raw'
INTERIM_DIR=DATA_DIR/'interim'
PROCESSED_DIR=DATA_DIR/'processed'
EXPORT_DIR=DATA_DIR/'exports'

@dataclass(frozen=True)
class AssetSettings:
    ticker:str='TUPRS'
    provider_symbol:str='TUPRS.IS'
    benchmark_ticker:str='XU100'
    benchmark_provider_symbol:str='XU100.IS'
    timezone:str='Europe/Istanbul'

@dataclass(frozen=True)
class ScrapingSettings:
    target_ticker:str=os.getenv('KAP_TARGET_TICKER','TUPRS')
    max_workers:int=int(os.getenv('KAP_MAX_WORKERS','3'))
    test_limit:int=int(os.getenv('KAP_TEST_LIMIT','5'))
    page_timeout_ms:int=60000

@dataclass(frozen=True)
class AnalysisSettings:
    horizons:tuple[int,...]=(1,3,5)
    candidate_count:int=20
    selected_analogue_count:int=8
    minimum_analogue_count:int=5
    embedding_dimension:int=384

ASSET=AssetSettings();SCRAPING=ScrapingSettings();ANALYSIS=AnalysisSettings()
