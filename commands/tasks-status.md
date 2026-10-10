---
description: Read-only audit of plan state in tasks/ cross-checked against git branches
agent: plan
---

Audit the state of all plans without changing any file. Work in the tasks dir (`tasks/`, fall back to `local/tasks/`) of the current project.

DIRECTORY SEMANTICS (authoritative, do not re-derive):
- `tasks/` root = ACTIVE plans: work not finished yet, these are the only plans to evaluate in depth.
- `tasks/wip/` = work in progress: implementation started, follow-up branches may be unmerged.
- `tasks/review/` = implementation done, awaiting user review before `completed/`.
- `tasks/completed/` = finished and archived; never audit their content, only count them.
- `tasks/todo.md` = backlog; numbers absent from plan files mean done and archived.
- Naming: `NNN_<ticket>_<description>.md` maps to branches `feature/NNN_*`.

PROTOCOL:
1. List plans per location; note empty or 0-byte plan files.
2. Evaluate steps 3-4 ONLY for plans in the `tasks/` root (active ones). For `wip/`, `review/`, `completed/` just report location and filename.
3. For each active plan, derive the 3-digit task number and ticket id from the filename (`NNN_<ticket>_<description>.md`).
4. Extract progress signals from the active plan body: checkbox counts (`[x]` vs `[ ]`), and any "Progress"/"Results"/"Status"/"DONE"/"WIP" sections.
5. Cross-check active plans with git (read-only only: `git branch -a`, `git log`, `git ls-files`, `git merge-base --is-ancestor`):
   - Find local and remote branches whose name contains the task number or the plan's slug.
   - Classify each branch as MERGED into HEAD or UNMERGED via `git merge-base --is-ancestor`.
   - For acceptance criteria named in the plan (files to create/remove/migrate), check presence in `git ls-files` / current tree.
6. Output one table row per active plan: task+ticket | last mtime | plan-internal status | branch state (merged/unmerged, branch head commit) | verdict; then one summary line per archived location (count only).
7. Flag inconsistencies for active plans explicitly: verifiably done but not in `completed/`; duplicate task-number prefixes; empty plan files; unmerged follow-up refactor branches for an otherwise-done task.
8. End with a short list of suggested file moves (source -> target) but DO NOT move or edit anything; ask the user before any change.

STRICT RULES: no file writes, no git state changes, no remote operations. Only read-only inspection.

User Context: $ARGUMENTS
