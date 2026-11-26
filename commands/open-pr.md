---
description: Push the current ticket branch, open a PR, and link it in the progress ticket
---

Open a PR for the current ticket branch: $ARGUMENTS

Parse optional `remote=<name>` (default `okurz`) and `base=<branch>` (default the branch `origin/HEAD` points to) from `$ARGUMENTS`.

1. **Preflight**: Confirm `git status` is clean and `git log --oneline origin/HEAD..HEAD` contains only the ticket commits; rebase or change the base if it includes an unrelated unmerged branch.
2. **Push**: Push the branch to `remote` and confirm the fork tip matches local `HEAD`.
3. **PR**: Load the `pr` skill for the body shape, but follow the repo's own PR layout (`AGENTS.md`, PR template, project skill). Create the PR against `base` with `gh pr create` and report the URL.
4. **Ticket**: Load the `redmine` skill. Append only the PR URL as a note to the progress ticket and set it to Feedback (or the project's review status). Show the exact note and status first unless the user already requested both.
5. **Follow up**: Continue in the same session with `/pr-watch <number>` unless the user asked to stop at creation (`skill: pr-followup`).
