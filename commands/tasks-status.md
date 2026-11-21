---
description: Read-only audit of plan state in tasks/ cross-checked against git branches
agent: plan
---

Read-only audit of plans in `tasks/` (or `local/tasks/`) using the `AGENTS.md` layout semantics (root = active; `wip/`, `review/`, `completed/` = report filename/counts only; `todo.md` = backlog). Context: $ARGUMENTS

1. List plans per location (flag 0-byte/empty files); evaluate steps 2–3 ONLY for active plans in `tasks/` root.
2. Parse `NNN_<ticket>_<description>.md` and extract progress signals (`[x]` vs `[ ]`, Progress/Results/Status/DONE/WIP sections, `## Blocked` rows).
3. Cross-check active plans against read-only git state (`git branch -a`, `git log`, `git ls-files`, `git merge-base --is-ancestor`):
   - Match branches by exact `feature/NNN_` prefix (NOT substring, as ticket IDs like `poo203217` embed numbers; mark slug-token matches as approximate).
   - Check whether each branch is MERGED into `HEAD` and whether plan acceptance artifacts exist in `git ls-files`.
   - Run each `## Blocked` verification command read-only (`gh`, `git merge-base`) and report the gate as `met`/`unmet`.
4. Output a table of active plans (`task+ticket | mtime | plan status | blocked gate | branch state + head | verdict`), one count line per subdir, and flag inconsistencies (done in root, duplicate `NNN` prefixes, empty files, unmerged follow-up branches, gate marked `met` in the plan while the verification command says otherwise).
5. Propose `source -> target` moves (noting prefix collisions that auto-resolve vs. content duplicates requiring manual merge due to the no-delete rule). Do NOT move/edit anything; run `/tasks-apply` only after user approval.
