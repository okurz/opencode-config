---
name: git-workflow
description: Use when committing verified work, amending, squashing, rebasing, resolving git merge conflicts, or writing commit messages.
---

# Git workflow

## Commit discipline

- **Atomic & Verified**: One conceptual change per commit; commit unrelated changes sequentially. Pass all lint, typecheck, and test checks before committing (avoid commit-then-amend cycles). Verify exit code 0 AND inspect the final 20 lines of test output for coverage/threshold failures. If near-term polish is likely, ask whether to commit now or wait.
- **Message Format**: Hard-wrap body at 50/80 columns with physical newlines and commit via `git commit -F - <<'EOF'`. For `fix` and `feat` commits, include `Motivation`, `Design Choices`, and `Benefits` headings (1–2 short sentences each). Append `Related issue: <ticket_URL>` on its own final line when applicable.
- **Accuracy & Linting**: Describe only the final diff (never local drafts or avoided mistakes) and do not call the target repo "upstream". Run project commit linters (e.g. `make test-gitlint`) after committing/amending and fix failures via `git commit --amend -F - <<'EOF'`.

## Rebase & conflict resolution

- **Staged Changes in Rebase**: During `git rebase`, `Changes to be committed:` in `git status` are the *local commit's* changes being replayed, NOT the existing state of `origin/master` (`HEAD`).
- **Verify Upstream Before `--skip`**: Never run `git rebase --skip` without verifying via `git show origin/master:<path>` or `git log` that the identical change is already in the upstream target branch.
