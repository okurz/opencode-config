---
description: Watch an open PR for review feedback or CI changes and apply approved fixes until nothing is actionable
argument-hint: "[PR number, URL or branch] [--interval N] [--cycles N] [--auto]"
---

Follow up on an open pull request: $ARGUMENTS

Load the `pr-followup` skill and follow it. Resolve the target from `$ARGUMENTS` (number, URL, or the
current branch's PR via `gh pr view --json number,state,url`); default interval 120 s, default 20 cycles.

1. **Read**: Fetch the PR state and the handled-id cache, and list only actionable items since then. Report a merged or closed PR and stop.
2. **Wait**: If nothing is actionable, wait one interval inside a single `bash` call with an explicit `timeout`, then re-read. Report one line per cycle.
3. **Propose**: On an actionable event, evaluate it with the `code-review` skill and present the fix set, prevention findings and draft replies; pause for approval unless `--auto` was passed.
4. **Apply**: Verify (repo tests, lint, coverage), commit, push, reply, update the cache, and continue with step 1 while cycles and blockers remain.
5. **Report**: End with the PR URL, the cycles consumed and the single remaining blocker or "nothing to do". Name the resume command when the session stops short.
