---
description: Plan, implement, and review using specialized sub-agents
---

Execute the following request using a multi-agent workflow: $ARGUMENTS

Roles: $ARGUMENTS may contain `architect=<agent>`, `builder=<agent>`, and `fixer=<agent>`; remove these tokens from the request. Defaults: `architect=pro-architect`, `builder=flash-builder`, `fixer=precision-fixer`. Launch each role's sub-agent by its resolved name. If a name is not an available subagent, stop and report it.

STRICT RULES:

1. **Planning:** First, use the `Task` tool to launch the architect sub-agent to research the codebase, identify relevant files and patterns, and design the architecture. Wait for it to finish. Based on its output, create a detailed markdown plan in the 'tasks/' directory.
2. **Implementation & Testing:** Second, use the `Task` tool to launch the builder sub-agent to implement the solution and corresponding tests as defined in the plan. Wait for it to finish.
3. **Review & Fix-up:** Third, use the `Task` tool to launch the fixer sub-agent to review the changes, fix any bugs, ensure strict compliance with linting, and verify maximum test coverage. Wait for it to finish.
4. **Coordination:** You (the main agent) must coordinate these sub-agents sequentially. Update the plan document in the 'tasks/' directory with the progress and results of each phase.
5. Do NOT stage (git add) or commit the plan file.
6. Only perform safe file operations and read-only 'git' operations on the plan document yourself (the subagents can edit the code).
