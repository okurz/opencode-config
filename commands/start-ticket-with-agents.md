---
description: Start a new ticket by fetching info, planning, branching, and executing with sub-agents
---

Start a new task based on the ticket ID or URL: $ARGUMENTS

Roles: $ARGUMENTS may contain `architect=<agent>`, `builder=<agent>`, and `fixer=<agent>`; remove these tokens before using the ticket ID or URL. Defaults: `architect=pro-architect`, `builder=flash-builder`, `fixer=precision-fixer`. Launch each role's sub-agent by its resolved name. If a name is not an available subagent, stop and report it.

STRICT RULES:

1. **Ticket Fetching:** Run the correct fetching command based on the provided ticket ID or URL:
   - If the ticket ID or URL contains `github.com`, starts with `gh`, or is a GitHub issue ID/number, run `gh issue view <ticket>` directly to fetch the issue details.
   - Otherwise, run `redmine-fetcher <ticket>` directly to fetch Redmine ticket data (the command is on $PATH).
2. **Architecture & Planning:** Use the `Task` tool to launch the architect sub-agent to analyze the ticket requirements, research the codebase, identify relevant files, and design the architecture. Wait for it to finish.
3. Determine the next free task number by taking the maximum of (a) the 3-digit prefixes of all local git branches, (b) the 3-digit prefixes of all files in `local/tasks/` (or `tasks/`), and (c) any listed task numbers in `tasks/todo.md`. Increment this maximum by one, formatted with leading zeros (e.g., if the highest is 061, use 062). If no numbers are found, start with 001.
4. Extract the ticket ID (e.g., `poo12345` for Redmine or `gh717` for GitHub) and a concise, snake_case description (3-4 words) from the ticket.
5. Formulate the task name: `<number>_<ticket_id>_<description>` (e.g., 062_poo12345_fix_foo).
6. Create and switch to a new git branch named `feature/<task_name>` (if the branch already exists, switch to it; otherwise create it, e.g., using `git checkout -b` or `git checkout` if it already exists).
7. SAVE the execution plan derived from the architect sub-agent into `tasks/<task_name>.md`.
8. **Implementation:** Use the `Task` tool to launch the builder sub-agent to implement the solution and tests as defined in the plan. Wait for it to finish.
9. **Review & Fix-up:** Use the `Task` tool to launch the fixer sub-agent to review the changes, fix any bugs, ensure strict compliance with linting, and verify maximum test coverage. Wait for it to finish.
10. Update the plan document in `tasks/<task_name>.md` with the progress and results of each phase. You (the main agent) must coordinate the sub-agents sequentially.
11. After the sub-agents finish implementation and verification, COMMIT the changes yourself. Follow the "Commit Discipline" and "Test Discipline" from AGENTS.md.
12. Do NOT push the branch or commits to the remote repository.
