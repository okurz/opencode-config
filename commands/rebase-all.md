---
description: Rebase all local branches onto origin/master/main, handling conflicts automatically
---

Rebase all local branches onto upstream (`origin/master` or `origin/main`):

1. Load and follow the `git-workflow` skill. Precondition: clean tree — the script refuses to run on a dirty tree, so stash first. Record the original tips (`git for-each-ref --format='%(refname:short) %(objectname:short)' refs/heads`) so a bad resolution can be recovered.
2. Fetch upstream only (`git fetch origin`; `git remote update` aborts the chain when any fork remote is unreachable), then run `git rebase-all-branches` (rebases every branch whose name does not contain `no_rebase`, skips branches already up to date, exits 1 with "Conflict on <branch>" on a conflict, and checks the starting branch back out at the end). Check the exit code without a pipe — `cmd | tail` reports `tail`'s status and hides a conflict.
3. On conflict, `git status` is the only gate:
   - "all conflicts fixed: run git rebase --continue" means `git rerere` resolved it; review `git rerere diff` before continuing, a recorded resolution can be stale and may contain conflict markers.
   - Otherwise `Read` the conflicted files and resolve per the `git-workflow` conflict rules, then `git add <files>` — this re-records the resolution and overwrites the stale entry (prune the cache with `git rerere gc`).
4. Validate the resolved file with the repo's own check (`make check`/`lint`, gitlint; for `.gitlab-ci.yml` parse YAML with a loader registering the `!reference` tag) before continuing.
5. Re-run `git rebase-all-branches`: it detects the in-progress rebase, runs `GIT_EDITOR=true git rebase --continue` (`--skip` only after verifying upstream state per `git-workflow`), then processes the remaining branches. Repeat until every branch reports "Skipping … (already up to date)".
6. Verify with `git branch -vv` plus ahead/behind counts for every non-`no_rebase` branch (`git rev-list --count $b..origin/master` must be 0; `git branch -vv` reports them only for tracking branches). Report commits the rebase dropped as already upstream, list branches ending at ahead 0 (candidates for `git delete-no-content-branches` — ask, never delete silently), and do not push: history was rewritten, so publishing needs `git push --force-with-lease <fork> <branch>` on request.
