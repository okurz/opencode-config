---
description: Rebase all local branches onto origin/master/main, handling conflicts automatically
---

Rebase all local branches onto upstream (`origin/master` or `origin/main`):

1. Load the `git-workflow` skill. Run `git remote update && git rebase-all-branches` (rebases branches not matching `no_rebase-*`; exits on conflict).
2. On conflict, check `git status`:
   - If `git rerere` already staged the resolution ("all conflicts fixed: run git rebase --continue"), proceed to step 3.
   - Otherwise `Read` conflicted files, resolve via `Edit` (prefer `HEAD` unless upstream is clearly better), and `git add <files>`.
3. Run `GIT_EDITOR=true git rebase --continue` (or `--skip` only after verifying upstream state per `git-workflow`), then re-run `git rebase-all-branches` until all branches finish.
4. Verify with `git branch -vv`.
