---
name: colgrep
description: Use when searching code, locating where behaviors or features are implemented, exploring unfamiliar repositories, or running semantic/hybrid code search with colgrep.
---

# Semantic Code Search & Localization

`colgrep` provides local semantic code search (NextPlaid/LateOn-Code-edge) and agent-driven code localization (`colgrep-agent-2B`).

## Workflows

- **Behavior & Feature Localization (`colgrep --agent`)**:
  Use for open-ended questions when symbol names are unknown:
  ```bash
  colgrep --agent "where are sessions expired after logout"
  colgrep --agent "how is authentication delegated" ./src
  ```
  The local 2B agent queries the index, inspects candidates, and returns targeted locations with enclosing function code. Use the returned snippet directly to avoid opening redundant files.
  *Execution:* Runs locally (5–25s). Never run in background mode; wait for synchronous completion.

- **Hybrid Semantic + Pattern Search (`colgrep -e`)**:
  Combines literal/regex filtering with semantic ranking:
  ```bash
  colgrep -e "Result<" "error handling"
  colgrep -e "async fn" --include="*.rs" "worker dispatch"
  ```

- **Broad Semantic Exploration**:
  ```bash
  colgrep "database connection pool" -k 10
  colgrep -l "authentication"          # matching files only (prevents context flooding)
  ```

- **Exact Identifier Lookups**:
  For known, exact symbol or regex matches (e.g. `grep "ExactSymbol"`), prefer native `grep` / `rg` for millisecond response.

## Filtering & Scoping

- Path scoping: `colgrep "<query>" ./src/api`
- File patterns: `--include="*.{ts,tsx}"`, `--exclude="*_test.go"`
- Context lines: `-n 10`

## Repository Indexing

Index is stored locally (`~/.local/share/colgrep/`) and updates automatically on file changes.
Initialize manually on a new repo with `/colgrep-init` or `colgrep init`.
