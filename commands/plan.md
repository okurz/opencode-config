---
description: Create a plan in the tasks/ directory without triggering any remove or add Git actions
---

Create a detailed execution plan for: $ARGUMENTS

Write the plan to `tasks/` (or `local/tasks/`) broken into atomic, independently committable tasks following the `AGENTS.md` naming and non-staging rules. Perform only read-only `git` operations and modify no other files.

End the plan with three sections: `## Approvals` (each decision, who approved it, the date), `## Gates` (the exact verification command for each commit), and `## Session starter` (the exact prompt for the next session: the plan file, the skills to load, the commit unit, and the actions that need confirmation).
