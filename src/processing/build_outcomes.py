"""Future 1D/3D/5D values are labels and never retrieval inputs."""
import pandas as pd
def build_event_outcomes(events:pd.DataFrame,asset_prices:pd.DataFrame,benchmark_prices:pd.DataFrame)->pd.DataFrame:
    # reference close = immediately before effective session.
    # asset_return = horizon/reference - 1; abnormal = asset - benchmark.
    # TODO: count trading sessions, handle missing future data, flag corporate actions.
    raise NotImplementedError
