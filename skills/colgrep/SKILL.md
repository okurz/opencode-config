---
name: colgrep
description: Use when searching code, locating where behaviors or features are implemented, exploring unfamiliar repositories, or running semantic/hybrid code search with colgrep.
---

# Semantic Code Search (`colgrep`)

- **Feature Localization (`colgrep --agent`)**: For open-ended questions when symbol names are unknown (`colgrep --agent "where are sessions expired" [./path]`). Runs synchronously in 5–25s (never run in background); returns targeted locations with enclosing function code so you can skip redundant file reads.
- **Hybrid Regex + Semantic (`colgrep -e`)**: `colgrep -e "async fn" --include="*.rs" "worker dispatch"`
- **Broad Exploration**: `colgrep "connection pool" -k 10` or file-only `colgrep -l "authentication"`.
- **Scoping & Exact Matches**: Scope via path (`./src`), `--include="*.{ts,tsx}"`, `--exclude="*_test.go"`, `-n 10`. Use native `grep`/`rg` for known exact identifiers.
- **Index**: Auto-updates in `~/.local/share/colgrep/`; initialize new repos via `/colgrep-init` or `colgrep init`.
