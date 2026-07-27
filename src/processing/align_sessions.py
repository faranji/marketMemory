"""Assign publication_session and effective_session_date."""
import pandas as pd
def align_events_to_sessions(events:pd.DataFrame,sessions:pd.DataFrame)->pd.DataFrame:
    # TODO: Europe/Istanbul timestamp → pre-open/in-session/post-close/non-trading → first full eligible session.
    # Test holidays and weekends; flag ambiguity.
    raise NotImplementedError
