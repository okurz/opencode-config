---
description: Create a plan in the tasks/ directory without triggering any remove or add Git actions
---

Create a detailed execution plan for: $ARGUMENTS

Resolve the plans directory with `git plans-dir` (the primary checkout's `tasks/`, so a worktree never gets its own copy) and write the plan there (or to `local/tasks/`), broken into atomic, independently committable tasks following the `AGENTS.md` naming and non-staging rules. Perform only read-only `git` operations and modify no other files.

End the plan with four sections: `## Approvals` (each decision, who approved it, the date), `## Gates` (the exact verification command for each commit), `## Blocked` (each unit gated on an external event: the condition, the read-only command that verifies it, the date recorded, and `unmet`/`met`; omit the section when nothing is gated), and `## Session starter` (the exact prompt for the next session: the plan file, the skills to load, the commit unit, and the actions that need confirmation).
