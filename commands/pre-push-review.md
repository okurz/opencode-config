---
description: Mandatory pre-push review of the current branch against the global review checklist, using a reviewer sub-agent by default
---

Perform a pre-push review of the current branch (`origin/HEAD..HEAD`).

Parse and strip optional `reviewer=<agent>` from `$ARGUMENTS` (default `general`; `main` runs in the main session).

1. Unless `reviewer=main`, launch the reviewer sub-agent via `Task` (do not review in the main session) with prompt:
   `Read ~/.config/opencode/review-protocol.md and follow it strictly for origin/HEAD..HEAD. Read-only: do not apply fixes. Context: $ARGUMENTS`
2. Report the findings directly to the user.
