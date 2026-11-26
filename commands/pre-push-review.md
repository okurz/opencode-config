---
description: Mandatory pre-push review of the current branch against the global review checklist, using a reviewer sub-agent by default
---

Perform a pre-push review of the current branch (`origin/HEAD..HEAD`).

Parse and strip optional `model=<fuzzy>` and `reviewer=<agent>` from `$ARGUMENTS`:
- If `reviewer=main`, run in the main session.
- If `model=<fuzzy>` is given: fuzzy-match against configured reviewer subagents or models in `~/.config/opencode/opencode.jsonc` (e.g. `hydrogen` -> `hydrogen-reviewer`, `deepseek` -> `deepseek-reviewer`).
- Otherwise use `reviewer=<agent>` if specified; with neither given, use the swift router (`model=swift`, which pi reaches as `--provider strata_router --model swift`) and fall back to `reviewer=general` when that model is unavailable.

1. Unless `reviewer=main`, launch the resolved reviewer sub-agent via `Task` (do not review in the main session) with prompt:
   `Read ~/.config/opencode/review-protocol.md and follow it strictly for origin/HEAD..HEAD. Read-only: do not apply fixes. Context: $ARGUMENTS`
2. Report the findings directly to the user.
