"""Build only information available before the event/effective session."""
import pandas as pd
def build_pre_event_features(events:pd.DataFrame,prices:pd.DataFrame,macro:pd.DataFrame)->pd.DataFrame:
    # TODO: pre-return 5D/20D, benchmark 20D, Brent/USDTRY 20D, vol20D, relative volume20D, regime.
    # CRITICAL: shift rolling values so the event session is not inside input data.
    raise NotImplementedError
