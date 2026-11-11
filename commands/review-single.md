---
description: Perform a critical review of the last commit, using a reviewer sub-agent by default
---

Perform a critical review of the last commit (`HEAD`).

Parse and strip optional `reviewer=<agent>` from `$ARGUMENTS` (default `general`; `main` runs in the main session).

1. Unless `reviewer=main`, launch the reviewer sub-agent via `Task` (do not run `git` or analyze in the main session) with prompt:
   `Read ~/.config/opencode/review-protocol.md and follow it strictly for the last commit only (git log -p -1). Read-only: do not modify files. Context: $ARGUMENTS`
2. Report the findings directly to the user.
