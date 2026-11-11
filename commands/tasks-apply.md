---
description: Execute approved tasks/ plan file moves safely (plain mv, no git staging, no deletion)
agent: build
---

Execute approved `tasks/` (or `local/tasks/`) file moves from a `tasks-status` audit or `$ARGUMENTS`, strictly obeying the `AGENTS.md` `tasks/` constraints (plain `mv` only; never stage, commit, or delete; skip content duplicates that would require deletion; leave `Readme.md` and `not_done/` untouched unless asked).

1. Verify each source file and target directory (`completed/`, `review/`, `wip/`) exist, then batch plain `mv` per target.
2. Leave any resulting `git status` changes unstaged (tell the user to stage inside the submodule themselves if desired).
3. Report files moved per target, resulting counts per location, auto-resolved prefix collisions, and content duplicates left in root for manual handling.
