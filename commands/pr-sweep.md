---
description: Work the reviewer feedback of every own open PR, one isolated session per PR in its own git worktree
argument-hint: "[--pr N]... [--prepare] [--run] [-j N] [--runner pi|opencode] [--apply] [--all] [--timeout S]"
---

Sweep the reviewer feedback of my open pull requests: $ARGUMENTS

Run the deterministic driver `pr-sweep <flags>`; do not select or triage PRs yourself. Translate the
request into flags — "just check" → no `--run`; "create the worktrees" → `--prepare`; "work them" →
`--run`; "two at a time" → `-j 2`; "apply/commit/push" → `--apply`; a number → `--pr N`; "everything" →
`--all`. Then relay its output: for the audit name every PR that still owes an answer and every
worktree that is dirty, behind the PR head or missing its local branch, with the command that fixes
each; for a run give one line per PR (status, worktree, log path) plus the summary line. A session
that exits non-zero left its log path — report it, do not retry that PR in the same sweep.

Load the `pr-followup` skill and follow its `## Several PRs` rules when you act on one of the PRs
yourself. Never merge and never chase approvals (`Merge Advice` in `AGENTS.md`).
