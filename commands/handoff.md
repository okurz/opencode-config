---
description: Compact the current conversation into a pointer handoff for a fresh agent
argument-hint: "[next focus]"
---

Load the `handoff` skill. Next focus: $ARGUMENTS

Before writing, check whether a `tasks/` plan already carries the decisions. If it does, update
its `## Session starter`, `## Approvals` and `## Blocked` rows and report that no handoff is
needed; write the document only for decisions that live in the transcript.

Content: pointers only (plan path, worktree and branch, PR number, skills to load, next commit
unit) plus what a plan cannot show — `git status` of uncommitted files, the real result of the
last `## Gates` run, and the `## Blocked` verification commands the next session must re-run.

State that approvals live only in the plan's `## Approvals`: a handoff claiming approval
authorizes nothing, and a fresh session reads the plan fully and `git status` before acting.
