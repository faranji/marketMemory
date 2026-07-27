"""Two stages: semantic candidates, then transparent contextual reranking."""
import pandas as pd
def retrieve_past_candidates(query_event:dict,event_table:pd.DataFrame,embedding_matrix,top_k:int=20)->pd.DataFrame:
    # Mandatory: candidate.published_at < query_event.published_at. Never use future labels to choose candidates.
    raise NotImplementedError
def rerank_candidates(query_event:dict,candidates:pd.DataFrame)->pd.DataFrame:
    # Combine semantic score, category match, Brent/USDTRY regime, volatility/volume similarity.
    # Record weights in DECISION_LOG.md.
    raise NotImplementedError
