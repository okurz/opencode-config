---
description: Read-only audit of local branches vs open PRs — merge readiness, stale local tips, and the work needed per PR
agent: plan
---

Audit local branches against open PRs. Context: $ARGUMENTS

1. Run `git fetch --all --prune` first — tracking counts in `git branch -vv` are stale without it. Identify upstream vs fork remotes from `git remote -v`.
2. Derive the base repo from `git remote get-url origin` (owner/repo), then gather in one `ctx_batch_execute` (gh concurrency ≤ 4): local branch tips (`git branch -v`) and open PRs via
   `gh pr list --repo <owner>/<repo> --state open --json number,title,headRefName,headRefOid,headRepositoryOwner,baseRefName,mergeable,mergeStateStatus,reviewDecision,isDraft,updatedAt,url --limit 100`
   Use only fields gh accepts (`headRefOwner` is NOT valid; the owner field is `headRepositoryOwner`).
3. Match PRs to branches by exact `headRefName`, then fetch authoritative PR heads: `git fetch origin pull/<N>/head:pr-<N>` (fork refs can be stale; the PR ref is ground truth).
4. Derive per branch in `ctx_execute` (never read raw git output into context):
   - `git rev-parse --short <branch> <fork>/<branch> pr-<N>` — fork remote == PR head means the PR was already updated from another machine and the local tip is stale.
   - `git rev-list --count` in both directions; large counts on rebased branches are master commits, not real divergence — confirm same-tip with `git log -1 --format=%s`.
   - `git merge-base --is-ancestor X Y && echo yes || echo no` — exit code 1 is the normal "no" answer; never let it abort the script.
   - Unmerged work: `git log --oneline origin/master..<branch>`; 0 commits means fully merged → branch deletion candidate.
5. For PRs not ready, collect blockers with `gh pr view <N> --json statusCheckRollup --jq '.statusCheckRollup | map("\(.name // .context) | \(.state // .status // "?")")'` (`state` is null for status contexts) and `gh pr view <N> --json reviews --jq '.reviews[] | select(.state=="CHANGES_REQUESTED") | (.comments // [])[] | "\(.path): \(.body[0:400])"'` (`comments` is null on many reviews; guard with `// []`).
6. State semantics: `DIRTY` = merge conflicts (rebase required); `UNSTABLE` = required checks not `SUCCESS`, and `COMPLETED` from workflow_dispatch runs counts as neutral — check the rollup before treating it as a real failure; `CLEAN` + `APPROVED` = merge-ready. Draft PRs additionally need a review request and ready mark.
7. Output one table: `branch | PR | review | merge state | local↔PR head | next step`, plus rows for open PRs without a local branch and local branches without a PR. Give the exact sync command (`git reset --hard <fork>/<branch>`) for stale branches. Read-only: propose, never mutate.
