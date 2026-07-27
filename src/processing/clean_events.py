"""raw_source_items → market_events. No embeddings or return labels here."""

def html_to_text(html:str)->str:
    # TODO: BeautifulSoup; remove script/style/nav noise; preserve meaningful tables; collapse whitespace.
    raise NotImplementedError

def promote_raw_kap_record(raw_record:dict)->dict:
    # Required: title, summary, body, published_at, URL, revision flags, review/leakage status.
    # Category may remain empty until classification.
    raise NotImplementedError
