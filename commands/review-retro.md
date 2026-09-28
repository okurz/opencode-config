---
description: Periodic retrospective over reviewer feedback on own PRs to promote, merge or prune review rules
---

Run a review retrospective. Arguments (optional): repos and time window, e.g.
`os-autoinst/openQA 30d`. Default: repos in the log, last 30 days. $ARGUMENTS

1. Fetch own PRs in the window: `gh pr list --repo <repo> --author @me --state all --json number,title,state,additions,deletions,reviewDecision,createdAt`.
   Report: PR count, open vs merged, median size, PRs > 300 changed lines, PRs with `CHANGES_REQUESTED`.
2. For each PR fetch reviewer comments (inline and review bodies) from others,
   excluding bots: `gh api repos/<repo>/pulls/<n>/comments` and `gh pr view <n> --json reviews`.
   Use `gh` with at most 4 parallel calls. Process data in code; print only summaries.
3. Compare with `~/.config/opencode/review-learnings.md`. Classify comments not
   yet logged (same categories as in the log) and propose log lines.
4. Group all log entries by class. Propose:
   - Promotions: classes with >= 2 entries (or security) not yet promoted,
     with the most automatic target (linter > repo `AGENTS.md` > global
     `AGENTS.md`/skill > `review-checklist.md`).
   - Pruning: checklist/rule entries with no recurrence in 90 days or now
     enforced by a linter.
   - Pre-push gaps: comments matching an existing checklist item, i.e. the
     pre-push review missed them. Suggest sharper wording.
5. PAUSE AND WAIT for approval. Then apply global changes directly; prepare
   repo changes on separate branches as atomic commits. Never push.
