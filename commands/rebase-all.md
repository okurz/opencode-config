---
description: Rebase all local branches onto origin/master/main, handling conflicts automatically
---

Rebase all local branches onto upstream (`origin/master` or `origin/main`):

1. Load and follow the `git-workflow` skill. Precondition: clean tree (stash if `git status --short` is dirty), then record the starting branch (`git rev-parse --abbrev-ref HEAD`) and the original tips (`git for-each-ref --format='%(refname:short) %(objectname:short)' refs/heads`) so a bad resolution can be recovered.
2. Fetch upstream only (`git fetch origin`; `git remote update` aborts the chain when any fork remote is unreachable), then run `git rebase-all-branches` (rebases branches not matching `no_rebase-*`; exits on conflict). Check the exit code without a pipe — `cmd | tail` reports `tail`'s status and hides a conflict. Re-running the script continues an in-progress rebase.
3. On conflict, `git status` is the only gate:
   - "all conflicts fixed: run git rebase --continue" means `git rerere` resolved it; review `git rerere diff` before continuing, a recorded resolution can be stale and may contain conflict markers.
   - Otherwise `Read` the conflicted files and resolve per the `git-workflow` conflict rules, then `git add <files>` — this re-records the resolution and overwrites the stale entry (prune the cache with `git rerere gc`).
4. Validate the resolved file with the repo's own check (`make check`/`lint`, gitlint; for `.gitlab-ci.yml` parse YAML with a loader registering the `!reference` tag) before continuing.
5. Run `GIT_EDITOR=true git rebase --continue` (or `--skip` only after verifying upstream state per `git-workflow`), then re-run `git rebase-all-branches` until every branch reports "Skipping … (already up to date)".
6. Verify with `git branch -vv` plus ahead/behind counts for every non-`no_rebase` branch (`git rev-list --count $b..origin/master` must be 0; `git branch -vv` reports them only for tracking branches). Report commits the rebase dropped as already upstream, list branches ending at ahead 0 (candidates for `git delete-no-content-branches` — ask, never delete silently), switch back to the recorded starting branch, and do not push: history was rewritten, so publishing needs `git push --force-with-lease <fork> <branch>` on request.
