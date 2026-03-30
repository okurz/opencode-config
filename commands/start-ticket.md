---
description: Start a new ticket by fetching info, planning, branching, and executing
---

Start a new task based on the Redmine ticket: $ARGUMENTS

STRICT RULES:
1. Run `fetch-redmine $ARGUMENTS` to retrieve ticket information from Redmine.
2. Based on the retrieved information, create a detailed execution plan.
3. Determine the next free task number by taking the maximum of (a) the
   3-digit prefixes of all local git branches, (b) the 3-digit prefixes of
   all files in `local/tasks/` (or `tasks/`), and (c) any listed task
   numbers in `tasks/todo.md`. Increment this maximum by one, formatted with
   leading zeros (e.g., if the highest is 061, use 062). If no numbers are
   found, start with 001.
4. Extract the ticket ID (e.g., poo12345) and a concise, snake_case
   description (3-4 words) from the ticket.
5. Formulate the task name: `<number>_<ticket_id>_<description>` (e.g.,
   062_poo12345_fix_foo).
6. Create and switch to a new git branch named `feature/<task_name>`.
7. SAVE the execution plan into `tasks/<task_name>.md`.
8. IMMEDIATELY begin executing the plan.
9. After implementation and successful verification (running tests and
   project-specific checks), COMMIT the changes.
10. Follow the "Commit Discipline" and "Test Discipline" from AGENTS.md.
11. Do NOT push the branch or commits to the remote repository.
