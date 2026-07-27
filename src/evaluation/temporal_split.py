"""Chronological train/validation/test split."""
import pandas as pd
def temporal_split(dataset:pd.DataFrame,train_end:str,validation_end:str):
    # Sort by published_at; keep revisions in same split; verify no overlap.
    raise NotImplementedError
