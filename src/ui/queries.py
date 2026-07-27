"""Streamlit uses read-only presentation queries; no scraping/training/writes."""
def load_overview_data(client):
    # TODO: reviewed events, latest prices, completed analyses, quality checks.
    raise NotImplementedError
def load_event_analysis(client,event_id:str):
    raise NotImplementedError
