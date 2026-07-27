"""Future official YouTube API adapter. Do not implement before the core MVP."""
def collect_youtube_mentions(query:str,published_before:str|None=None)->list[dict]:
    # Purpose: attention/community sentiment, not factual truth. Cache IDs and timestamps.
    # Leakage: only comments/videos before the analysed event may be predictors.
    raise NotImplementedError
