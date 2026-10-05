---
name: code-review
description: Use when addressing GitHub PR or code-review comments, reviewer feedback, fixup commits, or pre-push review before opening a PR. Covers evaluating feedback first, gh fetch patterns, and force-push safety.
---

# Code review management

- **Evaluate Feedback First**: Do not blindly implement reviewer suggestions. First, review the original commit messages and design choices to understand the context. Evaluate whether the comment makes sense and aligns with the codebase. You MUST always formulate an implementation plan and present it to the user for approval BEFORE executing any code changes or commits, regardless of how straightforward the comment seems.
- **Fetch Feedback**: Use the `gh` tool to fetch review comments from GitHub PRs.
- **Direct Comment Targeting**: If a URL with `#discussion_r(\d+)` is provided, parse the ID and use `gh api repos/:owner/:repo/pulls/comments/:id` to fetch only that specific feedback and its context.
- **Structured Address**: Use the `todowrite` tool to explicitly list all reviewer suggestions as a checklist to ensure 100% coverage of feedback.
- **Fixup Commits**: For PRs already in review, default to using `git commit --fixup <commit_hash>` to address feedback, unless a full rebase or new commit is explicitly requested.
- **Verify-Implement-Verify**: For each suggestion, first verify the current behavior/issue, implement the fix, and then verify again with tests and linting.
- **No Force Push**: Never force push to a remote branch unless the user explicitly confirms it is safe (e.g., in a personal feature branch).
- **Pre-Push Review**: Before pushing a branch or creating a PR, run `/pre-push-review-pro` (or `/pre-push-review-precision`) and resolve all `blocker`/`should-fix` findings. Before writing new code, check `~/.config/opencode/review-checklist.md`.
- **Learn from Reviews**: Log every reviewer comment in `~/.config/opencode/review-learnings.md` and promote recurring classes to linters or rules, as described in `/address-review`.
- **Scratch Files**: Write temporary scripts only under `/tmp/opencode`, never into repository working trees.
