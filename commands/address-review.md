---
description: Fetch GitHub PR review comments and set up a plan to address them
---

Address review comments for the PR, reviewer, or specific comment URL: $ARGUMENTS

Follow these steps strictly in order:
1. Parse the input. If it is a URL containing `#discussion_r(\d+)`, extract the comment ID.
2. If a comment ID is found:
   - Use `gh api repos/:owner/:repo/pulls/comments/:id` to fetch only that comment.
3. Otherwise:
   - Use `gh pr view` and `gh api` to retrieve review comments for the specified PR.
   - If a specific reviewer is mentioned, filter for their comments.
4. Review the context. Use `bash` to check the `git log` and original commit messages to fully understand the original design choices.
5. Critically evaluate the reviewer's comments against the original design. Do not blindly assume the reviewer is correct.
6. Use the `todowrite` tool to list all suggestions as a pending checklist.
7. Formulate a detailed plan for how to address each point (e.g., implement it, or push back with a specific reply). 
8. PAUSE AND WAIT. Present your analysis and proposed plan to the user. You MUST ask for user confirmation before executing any code changes.
9. ONLY AFTER user approval, for each approved point:
   - Implement the change using `edit` or `write`.
   - Run relevant tests and linting.
10. Once all approved points are addressed, create `git commit --fixup <commit_hash>` for the relevant original commits.
11. Verify everything passes with `make tidy` or equivalent project standards.
