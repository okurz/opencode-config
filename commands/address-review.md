Address review comments for the PR, reviewer, or specific comment URL: $ARGUMENTS

Goal: fix the immediate issue AND prevent the same class of issue in future
changes. Follow these steps strictly in order:

1. Parse the input. If it is a URL containing `#discussion_r(\d+)`, extract the comment ID.
2. If a comment ID is found:
   - Use `gh api repos/:owner/:repo/pulls/comments/:id` to fetch only that comment.
3. Otherwise:
   - Use `gh pr view` and `gh api` to retrieve review comments (inline and review bodies) for the specified PR.
   - If a specific reviewer is mentioned, filter for their comments.
4. Review the context. Use `bash` to check the `git log` and original commit messages to fully understand the original design choices.
5. Critically evaluate the reviewer's comments against the original design. Do not blindly assume the reviewer is correct.
6. Root-cause analysis. For each comment:
   - Classify: `lintable` | `repo-rule` | `global-rule` | `checklist` | `design` (needed discussion before coding) | `one-off`.
   - Check whether `~/.config/opencode/review-checklist.md` already covers it. If yes, the pre-push review failed: note why (item too vague, review skipped, model missed it).
   - Grep `~/.config/opencode/review-learnings.md` for earlier occurrences of the same class.
7. Prevention proposal, only if the class occurred before (>= 2 log entries including this one) or is security-related. Pick the most automatic option that fits:
   1. Linter/fixer/test in the repo (tidy config, custom perlcritic policy, eslint rule, xt test, markdown check).
   2. Rule in the repo `AGENTS.md` or contributing docs (project-specific conventions).
   3. Rule in `~/.config/opencode/AGENTS.md` or a skill under `~/.config/opencode/skills/` (cross-project conventions).
   4. Question in `~/.config/opencode/review-checklist.md` (judgment calls a reviewer model must verify).
      Keep rule files short: merge or rewrite existing entries instead of appending. Do not propose rules for one-offs.
8. Use the `todowrite` tool to list all fixes and prevention proposals as a pending checklist.
9. PAUSE AND WAIT. Present, separately: (a) analysis and plan per comment (implement or push back with reason), (b) prevention proposals with target file, (c) draft replies for each review thread. You MUST ask for user confirmation before executing any changes.
10. ONLY AFTER user approval, for each approved fix:
    - Implement the change using `edit` or `write`.
    - Run relevant tests and linting.
11. Once all approved fixes are done, create `git commit --fixup <commit_hash>` for the relevant original commits.
12. Verify everything passes with `make tidy` or equivalent project standards.
13. Apply approved prevention proposals:
    - Global files (`~/.config/opencode/...`): edit directly.
    - Repo files (linters, `AGENTS.md`): never mix into the fixup commits. Implement on a separate branch based on `origin/HEAD` as its own atomic commit for a separate PR, with tests for any new linter rule.
14. Append one line per comment to `~/.config/opencode/review-learnings.md` (date, `repo#PR r<comment_id>`, reviewer, category, one-line lesson, status `logged`/`promoted:<target>`/`rejected`). Update status of earlier entries of the same class when promoting.
15. Do not post replies on GitHub unless the user explicitly asks.
