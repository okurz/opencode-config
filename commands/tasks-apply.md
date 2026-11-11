---
description: Execute approved tasks/ plan file moves safely (plain mv, no git staging, no deletion)
agent: build
---

Execute the file moves the user approved from a `tasks-status` audit. Work in the tasks dir (`tasks/`, fall back to `local/tasks/`).

STRICT RULES (from AGENTS.md, non-negotiable):

- `tasks/` is a git submodule. Use plain `mv` only. NEVER run `git add`, `git commit`, `git rm`, `git mv`, `rm`, or any deletion in `tasks/`.
- Moves are within `tasks/` (root -> `completed/`, `review/`, `wip/`). Moving is allowed; deleting is not.
- Content merges of duplicate plans require deleting one file, which is forbidden. Skip them; report them for manual handling.
- Keep `Readme.md` and `not_done/` untouched unless the user explicitly asks.

PROCEDURE:

1. Take the approved source -> target list from the audit, or from $ARGUMENTS.
2. Verify each source file exists and the target directory exists (`completed/`, `review/`, `wip/`).
3. `mv` each file into its target directory, batching moves per target.
4. Do not stage. Plain `mv` of a tracked file leaves an unstaged `D` in `git status` and the copy untracked in the new location; that is expected. Tell the user to stage themselves if they want.
5. Report: files moved per target, resulting counts per location, duplicate-prefix collisions that auto-resolved (one member moved out of root), and content duplicates left in root for manual handling.

User Context: $ARGUMENTS
