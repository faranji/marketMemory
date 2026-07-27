"""Trading-session contracts. Implement with Europe/Istanbul and validated BIST sessions."""
from datetime import datetime,date

def classify_publication_session(published_at:datetime)->str:
    # Return pre_open/in_session/post_close/non_trading_day/unknown.
    # TODO: read trading_sessions instead of assuming weekdays.
    raise NotImplementedError

def find_effective_session_date(published_at:datetime,valid_sessions:list[date])->date:
    # Test pre-open, in-session, Friday after close, weekend and holiday cases.
    raise NotImplementedError
