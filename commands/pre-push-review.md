---
description: Mandatory pre-push review of the current branch against the global review checklist, using a reviewer sub-agent by default
---

Perform a pre-push review of the current branch against the global review checklist.

Reviewer: if $ARGUMENTS contains `reviewer=<agent>`, use that agent as the reviewer; remove the token from the context. Default: `general`. `reviewer=main` performs the review in the main session.

STRICT RULES:
1. If the reviewer is not `main`, you MUST use the `Task` tool to launch the reviewer sub-agent to perform this review. Do NOT perform the review in the main session.
2. Provide the reviewer with the following prompt:
   "Read `~/.config/opencode/review-protocol.md` and follow it strictly for the current branch. You are acting as reviewer only: do not apply fixes. Additional context: $ARGUMENTS"
3. Report the reviewer's findings directly to the user.
