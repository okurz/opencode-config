---
description: Rebase all local branches onto origin/master/main, handling conflicts automatically
---

Rebase all local branches onto their upstream target using git:

1. First run: `git remote update` to fetch all remotes
2. Then run: `git rebase-all-branches`
3. This loops through branches NOT matching 'no_rebase-*' and rebases onto origin/master (or origin/main)

If conflicts occur:
1. Examine conflicting files using the Read tool
2. Resolve conflicts by editing - prefer HEAD changes unless incoming is clearly better
3. Run: `git add <conflicted-files>`
4. Continue with: `GIT_EDITOR=true git rebase --continue`
5. Repeat from step 2 for remaining branches

To skip a problematic branch: `GIT_EDITOR=true git rebase --skip`

After all branches are rebased, verify with: `git branch -vv`
