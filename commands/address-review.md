---
description: Address PR/review comments and promote recurring lessons into rules or linters
---

Address review comments for the PR, reviewer, or comment URL: $ARGUMENTS

Goal: fix valid issues AND prevent recurring classes of issues. Load the `code-review` skill and follow these steps in order:

1. **Fetch**: For `#discussion_r(\d+)` URLs, run `gh api repos/:owner/:repo/pulls/comments/:id`. Otherwise fetch PR inline/review comments via `gh pr view` and `gh api` (filter by reviewer if specified).
2. **Evaluate**: Inspect `git log` and commit messages for original design context; critically evaluate each comment rather than assuming the reviewer is right.
3. **Root-Cause & Classify**: For each comment:
   - Classify: `lintable` | `repo-rule` | `global-rule` | `checklist` | `design` | `one-off`.
   - If `~/.config/opencode/review-checklist.md` already covers it, note why pre-push review missed it (too vague, skipped, or missed by model).
   - `grep` `~/.config/opencode/review-learnings.md` for prior occurrences of the same class.
4. **Prevention Proposal**: Only if the class occurred >= 2 times (including this one) or is security-related, propose the most automatic target that fits (merge/rewrite existing entries; never append for one-offs):
   1. Repo linter/fixer/test (`tidy`, `perlcritic`, `eslint`, `xt/`, markdown check).
   2. Repo `AGENTS.md` or contributing docs.
   3. Global `~/.config/opencode/AGENTS.md` or `~/.config/opencode/skills/`.
   4. `~/.config/opencode/review-checklist.md`.
5. **Plan & Pause**: Track fixes and prevention proposals in `todowrite`. Present: (a) per-comment analysis and plan (implement or push back), (b) prevention proposals + target files, (c) draft thread replies. PAUSE AND WAIT for user approval before changing anything.
6. **Implement Fixes**: For each approved fix, apply with `edit`/`write`, run tests/lint (`make tidy` or equivalent), and commit with `git commit --fixup <commit_hash>`.
7. **Apply Preventions**: Edit `~/.config/opencode/...` directly. For repo rules/linters, never mix into fixup commits—create an atomic commit (with linter tests) on a separate branch from `origin/HEAD`.
8. **Log**: Append one line per comment to `~/.config/opencode/review-learnings.md` (`date`, `repo#PR r<comment_id>`, `reviewer`, `category`, one-line lesson, `logged`/`promoted:<target>`/`rejected`) and update earlier entries when promoting. Never post GitHub replies unless explicitly asked.
