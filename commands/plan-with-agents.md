---
description: Plan, implement, and review using specialized sub-agents
---

Execute using a multi-agent workflow: $ARGUMENTS

Roles: parse and strip optional `architect=<agent>` (default `pro-architect`), `builder=<agent>` (default `flash-builder`), and `fixer=<agent>` (default `precision-fixer`) from `$ARGUMENTS`. Stop and report if any resolved sub-agent does not exist.

1. **Plan**: Run `architect` via `Task` to research the codebase and design the solution. Save the resulting plan in `tasks/` per `AGENTS.md` naming/non-staging rules (main agent edits only the plan file).
2. **Implement**: Run `builder` via `Task` to implement the code and tests from the plan.
3. **Review & Fix**: Run `fixer` via `Task` to review, fix bugs, pass linters, and verify test coverage.
4. **Track**: Coordinate sequentially and update the `tasks/` plan file after each phase without staging it.
