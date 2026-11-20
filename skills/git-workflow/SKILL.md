---
name: git-workflow
description: Use when committing verified work, amending, squashing, rebasing, resolving git merge conflicts, writing commit messages, or opening stacked/follow-up PRs.
---

# Git workflow

## Commit discipline

- **Atomic & Verified**: One conceptual change per commit; commit unrelated changes sequentially; split a diff that spans several modules by concept, never by line count. Pass all lint, typecheck, and test checks before committing (avoid commit-then-amend cycles). Verify exit code 0 AND inspect the final 20 lines of test output for coverage/threshold failures. If near-term polish is likely, ask whether to commit now or wait.
- **Message Format**: Hard-wrap body at 50/80 columns with physical newlines and commit via `git commit -F - <<'EOF'`.
  Ceilings only, never floors; never pad a body to match diff size and never shrink a diff to fit a budget. The body
  delivers what the diff cannot, so obviousness decides its shape, not diff size; never merge sections or drop their
  separators to save lines:
  (1) self-evident change (typo in a comment, formatting, rename, version or dependency bump, wording-only
  `docs`/`chore`): subject only;
  (2) reason not evident from the diff, no runtime behavior change (e.g. `refactor`): one sentence, no labels;
  (3) runtime behavior change: `Motivation:` required, plus `Design Choices:` for a non-obvious constraint and
  `Benefits:` for a user-visible effect, each ≤2 sentences;
  (4) one-line change to a default, flag, timeout, permission or generated-file exclusion (overrides 3): the line
  does not cap the explanation; one sentence each for `Motivation:`, `Design Choices:` and `Benefits:`, included only
  as far as the reason needs them, because `git blame` shows only the change and such a line can still have wide impact.
  Sections, when present, follow the order `Motivation:`, `Design Choices:`, `Benefits:`, `How to test:` (only when the
  project gate is not the test suite), then `Related issue: <ticket_URL>` as the final paragraph when applicable.
  Separate sections with exactly one blank line; a label-free body needs none. Prose ceiling: ≤10 lines, excluding
  labels, blank separators and the trailer. Never restate the CI log, the ticket prose or the diff.
- **Accuracy & Linting**: Describe only the final diff (never local drafts or avoided mistakes) and do not call the target repo "upstream". Run project commit linters (e.g. `make test-gitlint`) after committing/amending and fix failures via `git commit --amend -F - <<'EOF'`.

## Stacked & follow-up PRs

- **Branch & Title**: stack follow-up commits on the base PR's branch in a derived branch with suffix `_N` (e.g. `feature/145_…_2`); title `PART N: <subject> - After #<base PR>`.
- **Body**: lead with an `After:` bullet list of every base PR number (e.g. `After:\n* #8107`) so GitHub renders each base PR's title and status inline; keep the body shorter than the base PR's.
- **Draft While Stacked**: open with `--draft` until all blocking bases are merged and their gates are satisfied, so merge-activated automation (mergify rules, CI deploys) cannot fire prematurely.

## Rebase & conflict resolution

- **Staged Changes in Rebase**: During `git rebase`, `Changes to be committed:` in `git status` are the _local commit's_ changes being replayed, NOT the existing state of `origin/master` (`HEAD`).
- **Conflict Sides in Rebase**: `<<<<<<< HEAD` is the upstream target (rebased-onto state); the block after `=======` is the commit being replayed. Resolve so the replayed commit's intent survives, merging upstream's refactors of the same region (shared anchors, `extends`, `variables`) into it; take upstream alone only when it supersedes the change. Never leave conflict markers in the resolution.
- **Rerere Is Not Trusted Automatically**: `git rerere status`/`git rerere diff` listing a file is not a resolution; only `git status` reporting "all conflicts fixed: run git rebase --continue" is. Review the recorded resolution before continuing — stale entries exist. `git add` re-records the manual resolution; prune the cache with `git rerere gc`.
- **Syntax-Check Before `--continue`**: Run the repo's own check for the conflicted file type (`make check`/`lint`, gitlint; GitLab CI YAML needs a loader that registers the `!reference` tag) so a structurally merged resolution is verified as parseable.
- **Verify Upstream Before `--skip`**: Never run `git rebase --skip` without verifying via `git show origin/master:<path>` or `git log` that the identical change is already in the upstream target branch.
