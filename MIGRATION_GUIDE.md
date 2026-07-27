# Migration Guide

A large file replacement does **not** require `git push --force`.

Use a branch:

```bash
git checkout -b refactor/market-memory-tr
git add -A
git commit -m "refactor: rebuild Market Memory for BIST event analysis"
git push -u origin refactor/market-memory-tr
```

Force push is relevant only after rewriting Git history, for example to remove committed secrets. Rotate exposed secrets first, then clean history.

Preserve local `.env`, `.streamlit/config.toml`, and `.streamlit/secrets.toml`.
