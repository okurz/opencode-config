---
description: Start a new ticket by fetching info, planning, branching, and executing
---

Start a new task based on the Redmine ticket: $ARGUMENTS

STRICT RULES:
1. Run `fetch-redmine $ARGUMENTS` to retrieve ticket information from Redmine.
2. Based on the retrieved information, create a detailed execution plan.
3. Determine the next free task number by listing existing files in ``tasks/`,
   entries in tasks/todo.md and named branches in the format
   "feature/$nr_$plan". Look for 3-digit prefixes (e.g., 001, 061). The next
   number should be the highest existing number plus one, formatted with
   leading zeros (e.g., 062). If no files exist, start with 001.
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
