---
description: Start a new ticket by fetching info, planning, branching, and executing with sub-agents
---

Start a new task for ticket ID or URL: $ARGUMENTS

Roles: parse and strip optional `architect=<agent>` (default `pro-architect`), `builder=<agent>` (default `flash-builder`), and `fixer=<agent>` (default `precision-fixer`) from `$ARGUMENTS`. Stop and report if any resolved sub-agent does not exist.

1. **Fetch Ticket**: If the ticket references GitHub (`github.com`, `gh*`, or issue number), run `gh issue view <ticket>`; otherwise run `redmine-fetcher <ticket>`.
2. **Plan & Branch**: Run `architect` via `Task` to research and design the solution. Determine `<task_name>` (`<NNN>_<ticket_id>_<snake_case_desc>`, e.g. `062_poo12345_fix_foo` or `gh717`) per `AGENTS.md`, switch to/create branch `feature/<task_name>`, and save the plan to `tasks/<task_name>.md` (or `local/tasks/`).
3. **Implement & Fix**: Sequentially run `builder` (implement code + tests) and `fixer` (review, fix bugs, pass linters, verify coverage) via `Task`, updating `tasks/<task_name>.md` after each phase.
4. **Commit**: Load and follow the `testing` and `git-workflow` skills to verify and commit the changes (never stage `tasks/` or push).
