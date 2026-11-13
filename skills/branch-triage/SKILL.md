---
name: branch-triage
description: Use when auditing or triaging local branches and open pull requests to identify fastest merge candidates, unblocking reviews, or ready-to-open PRs.
---

# Branch and PR Triage Workflow

Systematic read-only evaluation to identify branches ready for a PR, PRs closest to merge today, and stale or diverged branches.

## 1. Fast State Inventory (Read-Only)

Gather local branch status and upstream PR state without modifying working trees:

1. **Local branch inventory & worktree scoping**:
   - Worktree scoping: check sibling directories (`../<name>`) and branch naming tags (e.g. `oqa$N`). Scope the audit to branches created from or active in this working copy; attribute others to their respective home worktree rather than classifying them as orphan PRs.
   - Distance from upstream: `git rev-list --count origin/<main>..<branch>`
   - Merge base status: `git merge-base --is-ancestor <branch> origin/<main>`
   - Cherry-pick status: `git cherry -v origin/<main> <branch>` to detect commits already picked upstream.
   - Commit intent: identify `WIP`, `fixup!`, `squash!`, or multi-part suffixes (`_1`, `_2`).

2. **Map local branches to PRs**:
   - Query PRs by author/head using `gh pr list --state open --json number,title,headRefName,isDraft,mergeStateStatus,reviewDecision,updatedAt`.
   - Separate branches with an open PR from independent local branches.

3. **Check local tip vs. remote PR head**:
   - Compare `git rev-parse <branch>` with PR `headRefOid`.
   - When fork remote == PR head != local, compare commit messages (`git log -1 --format=%s`) and timestamps: identical message with newer local commit indicates an unpushed local rebase (propose `git push --force-with-lease`); if PR is newer or message differs, local tip is stale (propose `git reset --hard <fork>/<branch>`).
   - Check if difference is a clean rebase or content drift via patch comparison:
     `git diff origin/<main>...<branch>` vs. `git diff <base>...<headRefOid>`.

## 2. Check Auto-Merge and CI Gates

Before ranking, inspect repository-specific merge requirements:

- Inspect `.mergify.yml` or branch protection rules (e.g. required approvals count, required check names, minimum check count `#check-success >= N`, forbidden labels like `acceptance-tests-needed` or `not-ready`, bypass labels like `merge-fast`).
- Tally PR checks (`gh pr checks <num>`): distinguish genuine test/linter failures vs. transient infrastructure glitches or outdated base packaging errors (e.g. OBS build failures caused by an old base commit missing recent spec/packaging fixes) that resolve on clean rebase.
- Focus on actionable code/test fixes (review feedback to address, test adjustments, packaging rebase) over administrative force-merge bypass labels (e.g. `merge-fast`).

## 3. Candidate Categorization

Categorize findings into four tiers:

- **Tier 1: Ready to merge today (Zero or minimal code friction)**:
  - Required approvals met (or needs 1 more approval / label).
  - 0 unresolved review threads / 0 changes requested.
  - CI checks green or only blocked by clean rebase push.
  - Action: rebase push with lease, remove blocking label, or ping for final approval.

- **Tier 2: Quick-fix unblocks (Low friction)**:
  - 1 minor reviewer request (e.g. nitpick, small test helper refactor).
  - Passing CI once pushed.

- **Tier 3: Best candidates to open new PRs from**:
  - Independent branches with clean commit history (Conventional Commits, 50/80 rule).
  - Tests included and passing.
  - Not blocked by unmerged parent features.

- **Tier 4: Stale, duplicate, or blocked (Prune / Do not touch)**:
  - Blocked by unmerged parent branches in a stacked PR chain.
  - Competing POCs or experiments without tests.
  - PRs with core architectural objections or failing test suites.
  - Already merged upstream (empty diff or identical patch-id).

## 4. Safety Constraints

- Perform **only read-only** operations during triage (`git`, `gh`).
- Never force-push, close PRs, change labels, or delete branches without explicit user confirmation per target.
