---
description: Push the current ticket branch, open a PR, and link it in the progress ticket
---

Open a PR for the current ticket branch: $ARGUMENTS

Parse optional `remote=<name>` (default `okurz`), `base=<branch>` (default the branch `origin/HEAD` points to) and pass `model=`/`reviewer=` through to the pre-push review.

1. **Preflight**: Confirm `git status` is clean and `git log --oneline origin/HEAD..HEAD` contains only the ticket commits. When the range stacks on an unmerged branch the user asked to stack on, keep it as a stacked PR (branch suffix `_N`, title `PART N: <subject> - After #<base>`, body leading with `After:` bullets, `--draft` until the base merges, per the `git-workflow` skill); otherwise rebase or change the base if it includes an unrelated unmerged branch.
2. **Pre-push review**: Run `/pre-push-review` over the range, passing `model=`/`reviewer=` through, and resolve every `blocker`/`should-fix` finding in code, docs and commit messages before pushing. Re-run it after the fixes and report its verdict.
3. **Push**: Push the branch to `remote` and confirm the fork tip matches local `HEAD`.
4. **PR**: Load the `pr` skill for the body shape, but follow the repo's own PR layout (`AGENTS.md`, PR template, project skill). Create the PR against `base` with `gh pr create` (`--draft` for a stack) and report the URL.
5. **Ticket**: Load the `redmine` skill. Append only the PR URL as a note to the progress ticket and set it to Feedback (or the project's review status). Show the exact note and status first unless the user already requested both.
6. **Follow up**: Continue in the same session with `/pr-watch <number>` unless the user asked to stop at creation (`skill: pr-followup`).
