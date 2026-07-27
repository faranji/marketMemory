"""Create one inspectable analysis snapshot without mutating source tables."""
import pandas as pd
def build_analysis_dataset(events:pd.DataFrame,features:pd.DataFrame,outcomes:pd.DataFrame)->pd.DataFrame:
    # TODO: one row per event/asset, preserve times, features, labels and version.
    raise NotImplementedError
