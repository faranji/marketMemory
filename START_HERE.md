# Start Here

## Preserve locally

Keep these existing files and values:

```text
.env
.streamlit/config.toml
.streamlit/secrets.toml
```

Do not commit `.env` or `.streamlit/secrets.toml`. Do not reuse an old `config.py` that contains plaintext credentials.

## Build order

```text
KAP probe
→ one detail
→ five-detail pilot
→ raw Supabase
→ clean events
→ event categories
→ TUPRS/XU100
→ USD/TRY + Brent
→ BIST session alignment
→ pre-event features
→ 1D/3D/5D labels
→ embeddings
→ historical retrieval
→ confidence/abstention
→ evaluation
→ Streamlit
→ optional YouTube/X ablation
```

Never scrape the full history before the five-record pilot is correct.
