---
description: Perform a critical review of all commits in the branch based on origin/HEAD, using a reviewer sub-agent by default
---

Perform a critical review of all commits in `origin/HEAD..HEAD`.

Parse and strip optional `reviewer=<agent>` from `$ARGUMENTS` (default `general`; `main` runs in the main session).

1. Unless `reviewer=main`, launch the reviewer sub-agent via `Task` (do not run `git` or analyze in the main session) with prompt:
   `Read ~/.config/opencode/review-protocol.md and follow it strictly for all commits in origin/HEAD..HEAD (git log --reverse -p origin/HEAD..HEAD). Read-only: do not modify files. Context: $ARGUMENTS`
2. Report the findings directly to the user.
