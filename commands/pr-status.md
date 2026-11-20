---
description: Read-only audit of local branches vs open PRs — merge readiness, stale local tips, and the work needed per PR
agent: plan
---

Audit local branches against open PRs. Context: $ARGUMENTS

1. Run `git fetch --all --prune` first — tracking counts in `git branch -vv` are stale without it. Identify upstream vs fork remotes from `git remote -v`.
2. Derive the base repo from `git remote get-url origin` (owner/repo). Detect working copy identity and sibling directories (e.g. `../oqa*`, worktree name, or branch tags like `oqa$N`); scope the audit to branches created from or active in this working copy, attributing sibling branches to their respective working tree rather than marking them orphan.
3. Gather in one `ctx_batch_execute` (gh concurrency ≤ 4): local branch tips (`git branch -v`) and open PRs via
   `gh pr list --repo <owner>/<repo> --state open --json number,title,headRefName,headRefOid,headRepositoryOwner,baseRefName,mergeable,mergeStateStatus,reviewDecision,isDraft,updatedAt,url --limit 100`
   Use only fields gh accepts (`headRefOwner` is NOT valid; the owner field is `headRepositoryOwner`).
4. Match in-scope PRs to branches by exact `headRefName`, then fetch authoritative PR heads: `git fetch origin pull/<N>/head:pr-<N>` (fork refs can be stale; the PR ref is ground truth).
5. Derive per branch in `ctx_execute` (never read raw git output into context):
   - `git rev-parse --short <branch> <fork>/<branch> pr-<N>` — if fork remote == PR head != local, check commit message (`git log -1 --format=%s`) and commit timestamp: if identical message and local is newer, it is an unpushed local rebase; if PR is newer or message differs, local tip is stale.
   - `git rev-list --count` in both directions; large counts on rebased branches are master commits, not real divergence.
   - `git merge-base --is-ancestor X Y && echo yes || echo no` — exit code 1 is the normal "no" answer; never let it abort the script.
   - Unmerged work: `git log --oneline origin/master..<branch>`; 0 commits means fully merged → branch deletion candidate.
6. For PRs not ready, collect blockers with `gh pr view <N> --json statusCheckRollup --jq '.statusCheckRollup | map("\(.name // .context) | \(.state // .status // "?")")'` (`state` is null for status contexts) and `gh pr view <N> --json reviews --jq '.reviews[] | select(.state=="CHANGES_REQUESTED") | (.comments // [])[] | "\(.path): \(.body[0:400])"'` (`comments` is null on many reviews; guard with `// []`).
7. State semantics: `DIRTY` = merge conflicts (rebase required); `UNSTABLE` = required checks not `SUCCESS`, and `COMPLETED` from workflow_dispatch runs counts as neutral — check the rollup before treating it as a real failure; `CLEAN` with as many approvals as `.mergify.yml` requires = finished, report "nothing to do" because the auto-merger owns the merge (a missing approval means waiting days for reviewers, never chasing them). Draft PRs additionally need a ready mark.
   - Focus on actionable code/test fixes (review feedback to address, test failures, or packaging failures resolvable by rebase). Do not prioritize PRs merely because they could be force-merged with bypass labels like `merge-fast`.
   - Distinguish genuine test/linter failures from outdated base packaging errors (e.g. OBS build failures caused by an old base commit missing recent spec fixes) or transient infrastructure glitches.
8. Output one table: `branch | PR | review | merge state | local↔PR head | next step`, plus rows for open PRs without a local branch and local branches without a PR. Give the exact sync command (`git reset --hard <fork>/<branch>` to discard, or `git push --force-with-lease <fork> <branch>` to publish local rebase). Read-only: propose, never mutate.
