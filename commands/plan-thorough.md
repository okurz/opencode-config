---
description: Create a thorough plan in the tasks/ directory using an @explore sub-agent for research
---

Create a detailed execution plan for: $ARGUMENTS

1. Launch the `explore` sub-agent (`agents/explore.md`, `Task` tool, "very thorough") to identify relevant files, patterns, constraints and insertion points; launch it synchronously with a long `timeout` and wait for its report.
2. Write the atomic plan to `tasks/` (or `local/tasks/`) following the `AGENTS.md` naming and non-staging rules. ending with `## Approvals`, `## Gates`, and `## Session starter` as `plan` defines them. Perform only read-only `git` operations and touch no other files.
