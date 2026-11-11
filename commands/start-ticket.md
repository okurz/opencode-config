---
description: Start a new ticket by fetching info, planning, branching, and executing
---

Start a new task for ticket ID or URL: $ARGUMENTS

1. **Fetch Ticket**: If `$ARGUMENTS` references GitHub (`github.com`, `gh*`, or issue number), run `gh issue view $ARGUMENTS`; otherwise run `redmine-fetcher $ARGUMENTS`.
2. **Plan & Branch**: Determine `<task_name>` (`<NNN>_<ticket_id>_<snake_case_desc>`, e.g. `062_poo12345_fix_foo` or `gh717`) per `AGENTS.md`, switch to/create branch `feature/<task_name>`, and save the execution plan to `tasks/<task_name>.md` (or `local/tasks/`).
3. **Execute & Commit**: Implement the plan, verify with tests and project checks, and commit following the `testing` and `git-workflow` skills (never stage `tasks/` or push).
