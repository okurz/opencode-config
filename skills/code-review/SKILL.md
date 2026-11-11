---
name: code-review
description: Use when addressing GitHub PR or code-review comments, reviewer feedback, fixup commits, or running pre-push reviews.
---

# Code review management

- **Evaluate & Get Approval First**: Check original commit messages and design context before accepting reviewer suggestions. Track all items via `todowrite` and ALWAYS present an evaluation + implementation plan for user approval BEFORE editing code or committing.
- **Fetch Feedback**: Use `gh` to fetch PR review comments; for `#discussion_r(\d+)` URLs, fetch only `gh api repos/:owner/:repo/pulls/comments/:id`.
- **Verify-Implement-Verify & Fixup**: Reproduce/verify the issue, apply the fix, re-run tests/lint, and commit with `git commit --fixup <commit_hash>` unless rebase/new commit is requested.
- **No Force Push**: Never force-push unless the user explicitly confirms it is safe.
- **Pre-Push & Checklist**: Check `~/.config/opencode/review-checklist.md` before coding; run `/pre-push-review` before pushing or opening a PR and resolve all `blocker`/`should-fix` items.
- **Learn & Scratch**: Log comments in `~/.config/opencode/review-learnings.md` (promote recurring classes per `/address-review`). Put temporary files only in `/tmp/opencode`.
