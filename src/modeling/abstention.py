"""Trustworthy systems explicitly refuse weak evidence."""
def should_abstain(analogue_count:int,mean_similarity:float,positive_ratio:float|None,missing_critical_data:bool)->tuple[bool,str|None]:
    # Reasons: few analogues, weak similarity, mixed outcomes, missing data, regime mismatch.
    raise NotImplementedError
