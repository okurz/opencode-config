---
description: Execute one commit unit of an approved tasks/ plan file
argument-hint: "<plan-file> [commit unit]"
---

Read `AGENTS.md`, `$1`, `git status`, and the test precedent the plan names. Load the `git-workflow` and `testing` skills.
Implement only ${2:-commit 1} of the plan. Run the plan's `## Gates` command for that unit and report its real result.
Take every design decision from the plan's `## Approvals`; never invent a decision the plan does not record.
Stop before any remote, deploy, reboot, service start, install, or `ssh` write the plan names, and ask before one.
Never stage, commit, `rm`, or delete anything under `tasks/`; move the plan to `wip/` with plain `mv` when its code starts.
Report: the unit done, the plan sections touched, the uncommitted files, the next unit, and the plan's `## Session starter` for the next session.
