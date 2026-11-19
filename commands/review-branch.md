---
description: Perform a critical review of all commits in the branch based on origin/HEAD, using a reviewer sub-agent by default
---

Perform a critical review of all commits in `origin/HEAD..HEAD`.

Parse and strip optional `model=<fuzzy>` and `reviewer=<agent>` from `$ARGUMENTS`:
- If `reviewer=main`, run in the main session.
- If `model=<fuzzy>` is given: fuzzy-match against configured reviewer subagents or models in `~/.config/opencode/opencode.jsonc` (e.g. `hydrogen` -> `hydrogen-reviewer`, `deepseek` -> `deepseek-reviewer`).
- Otherwise use `reviewer=<agent>` if specified, defaulting to `general`.

1. Unless `reviewer=main`, launch the resolved reviewer sub-agent via `Task` (do not run `git` or analyze in the main session) with prompt:
   `Read ~/.config/opencode/review-protocol.md and follow it strictly for all commits in origin/HEAD..HEAD (git log --reverse -p origin/HEAD..HEAD). Read-only: do not modify files. Context: $ARGUMENTS`
2. Report the findings directly to the user.
