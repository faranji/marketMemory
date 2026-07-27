"""Prepare consistent event text for classification and embeddings."""
def build_event_text(title:str,summary:str|None,body_text:str|None,category_name:str|None)->str:
    # Suggested sections: [CATEGORY], [TITLE], [SUMMARY], [BODY].
    # Remove duplicated boilerplate but keep meaningful numbers.
    raise NotImplementedError
