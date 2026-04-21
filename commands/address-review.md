---
description: Fetch GitHub PR review comments and set up a plan to address them
---

Address review comments for the PR, reviewer, or specific comment URL: $ARGUMENTS

Follow these steps:
1. Parse the input. If it is a URL containing `#discussion_r(\d+)`, extract the comment ID.
2. If a comment ID is found:
   - Use `gh api repos/:owner/:repo/pulls/comments/:id` to fetch only that comment.
3. Otherwise:
   - Use `gh pr view` and `gh api` to retrieve review comments for the specified PR.
   - If a specific reviewer is mentioned, filter for their comments.
4. Critically evaluate the reviewer's comments. Do not blindly implement them. If a comment is ambiguous, seems incorrect, or requires architectural decisions, pause and ask the user for clarification or confirmation before proceeding.
5. Use the `todowrite` tool to list all suggestions.
6. For each point:
   - Identify the affected code.
   - Implement the change using `edit` or `write`.
   - Run relevant tests and linting.
7. Once all points are addressed, create `git commit --fixup <commit_hash>` for the relevant original commits.
8. Verify everything passes with `make tidy` or equivalent project standards.
