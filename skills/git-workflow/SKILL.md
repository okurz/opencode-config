---
name: git-workflow
description: Use when committing verified work, amending, squashing, rebasing, resolving git merge conflicts, or writing commit messages.
---

# Git workflow

## Commit discipline

- **Atomic & Verified**: One conceptual change per commit; commit unrelated changes sequentially; split a diff that spans several modules by concept, never by line count. Pass all lint, typecheck, and test checks before committing (avoid commit-then-amend cycles). Verify exit code 0 AND inspect the final 20 lines of test output for coverage/threshold failures. If near-term polish is likely, ask whether to commit now or wait.
- **Message Format**: Hard-wrap body at 50/80 columns with physical newlines and commit via `git commit -F - <<'EOF'`. For `fix` and `feat` commits, include `Motivation`, `Design Choices`, and `Benefits` headings (1–2 short sentences each). Ceilings only, never floors: ≤10 body lines, ≤2 sentences per section; never pad a body to match diff size, never shrink a diff to skip a section. Write a section only when it carries what the diff cannot: `Motivation` for any behavior change, `Design Choices` for a non-obvious constraint, `Benefits` for a user-visible effect, `How to test` when the project gate is not the test suite. A 1-line diff of a default, flag, timeout, permission or generated-file exclusion gets the full sections, because `git blame` shows only the change. `docs`/`chore`/`style`/`refactor`/dependency bumps: subject plus at most one sentence. Never restate the CI log, the ticket prose or the diff. Append `Related issue: <ticket_URL>` on its own final line when applicable.
- **Accuracy & Linting**: Describe only the final diff (never local drafts or avoided mistakes) and do not call the target repo "upstream". Run project commit linters (e.g. `make test-gitlint`) after committing/amending and fix failures via `git commit --amend -F - <<'EOF'`.

## Rebase & conflict resolution

- **Staged Changes in Rebase**: During `git rebase`, `Changes to be committed:` in `git status` are the *local commit's* changes being replayed, NOT the existing state of `origin/master` (`HEAD`).
- **Conflict Sides in Rebase**: `<<<<<<< HEAD` is the upstream target (rebased-onto state); the block after `=======` is the commit being replayed. Resolve so the replayed commit's intent survives, merging upstream's refactors of the same region (shared anchors, `extends`, `variables`) into it; take upstream alone only when it supersedes the change. Never leave conflict markers in the resolution.
- **Rerere Is Not Trusted Automatically**: `git rerere status`/`git rerere diff` listing a file is not a resolution; only `git status` reporting "all conflicts fixed: run git rebase --continue" is. Review the recorded resolution before continuing — stale entries exist. `git add` re-records the manual resolution; prune the cache with `git rerere gc`.
- **Syntax-Check Before `--continue`**: Run the repo's own check for the conflicted file type (`make check`/`lint`, gitlint; GitLab CI YAML needs a loader that registers the `!reference` tag) so a structurally merged resolution is verified as parseable.
- **Verify Upstream Before `--skip`**: Never run `git rebase --skip` without verifying via `git show origin/master:<path>` or `git log` that the identical change is already in the upstream target branch.
