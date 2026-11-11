---
description: Rebase all local branches onto origin/master/main, handling conflicts automatically
---

Rebase all local branches onto their upstream target using git:

1. First run: `git remote update` to fetch all remotes
2. Then run: `git rebase-all-branches`
3. This loops through branches NOT matching 'no_rebase-\*' and rebases onto origin/master (or origin/main). If a conflict occurs, the loop WILL STOP and exit.

If conflicts occur:

1. Run `git status` to identify conflicting files and check the rerere status.
2. If `git status` says "all conflicts fixed: run git rebase --continue", `git rerere` has automatically resolved and staged the conflict. Skip to step 5.
3. Otherwise, examine conflicting files using the Read tool.
4. Resolve conflicts by editing - prefer HEAD changes unless incoming is clearly better.
5. Run: `git add <conflicted-files>` (if you had to manually resolve files)
6. Continue the current rebase with: `GIT_EDITOR=true git rebase --continue`
7. CRITICAL: Because `git rebase-all-branches` stops and exits when a conflict occurs, you MUST run `git rebase-all-branches` again to resume rebasing the remaining branches.
8. Repeat this entire conflict resolution process until `git rebase-all-branches` completes successfully without stopping.

To skip a problematic branch: `GIT_EDITOR=true git rebase --skip`

After all branches are rebased, verify with: `git branch -vv`
