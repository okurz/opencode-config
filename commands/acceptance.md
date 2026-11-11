---
description: Run a plan's acceptance steps on a remote machine, re-verifying dated facts first
argument-hint: "<plan-file>"
---

Read `AGENTS.md`, `$1`, and `git status`. Load the `git-workflow` and `testing` skills.
Re-verify every dated fact in the plan before acting (versions, release feed contents, driver, disk, service state) with read-only commands: facts go stale within hours, so the plan's numbers are a starting hypothesis, not the current state.
Ask for confirmation before the first `ssh` write, service change, install, or reboot on the remote machine, then run the plan's acceptance steps in order, each with its check.
Report each step's real output, the log path the plan asked to record, and every plan fact that turned out to be stale.
