"""KAP source layer: discover links and preserve raw detail pages; do not classify meaning here."""
from pathlib import Path

def discover_disclosure_links(year:int,ticker:str='TUPRS')->list[dict]:
    # TODO: Playwright visible browser → save HTML/screenshot → inspect selectors → dedupe URL/ID.
    # Expected: external_id, source_url, row_text.
    raise NotImplementedError

def fetch_disclosure_detail(source_url:str,output_directory:Path)->dict:
    # TODO: rendered HTML + visible text + publisher + timestamp + subject/summary + revision flags + attachments + hash.
    # Keep raw source; final event category belongs to processing.
    raise NotImplementedError
