---
name: git-workflow
description: Use when committing, amending, squashing, rebasing, resolving git merge conflicts, or writing commit messages. Covers atomic commits, commit-message format/heredocs, and rebase/conflict safety.
---

# Git workflow

## Commit discipline

- **Atomic Commits**: Each commit MUST focus on a single conceptual change or task. Do not mix unrelated changes, such as bug fixes, logging improvements, and new features, into a single commit. If multiple unrelated changes are needed, implement and commit them sequentially.
- Do not commit until all verification steps (lint, typecheck, tests) have passed. Fix issues first, then commit once — avoid commit-then-amend cycles.
- CRITICAL: Do not just read the top of the test output. You MUST verify the command exit code is 0 and read the final 20 lines of the output for strict threshold failures (like coverage drops) that might occur even if all individual tests pass.
- When a commit may need near-term follow-up changes (e.g. test consolidation, style fixes), ask the user whether to commit now or wait until changes are fully polished.
- ALL fix and feat commits MUST include a multi-line commit message. The body MUST contain the headings: Motivation, Design Choices, and Benefits. Be concise: write only 1-2 short sentences under each heading.
- Commit message format: 50/80 rule. You MUST explicitly insert physical newlines to hard-wrap the body text at 80 characters.
- To execute multi-line commits reliably without temporary files or interactive editors, ALWAYS use a bash heredoc via standard input: `git commit -F - <<EOF`.
- After creating or amending a commit, run any project-specific commit linters (e.g. `make test-gitlint`). If the linter fails, use `git commit --amend -F - <<EOF` to fix the message.
- If work is based on a ticket, reference the ticket in the commit message at the bottom in a separate line in the format `Related issue: <ticket_URL>`
- **Accuracy over History**: Commit messages must strictly describe the final diff. Do not describe hypothetical prior states, avoided mistakes, or local drafts as if they were removed in the current commit.
- **Terminology**: Avoid referring to the target repository as "upstream" in commit messages intended for that repository.

## Rebase & conflict resolution

- **Do Not Misinterpret Staged Changes during Rebase**: During `git rebase`, any files listed under `Changes to be committed:` as `typechange`, `modified`, or `new file` in the output of `git status` represent the changes introduced by the _local branch's commit_ currently being applied. Do NOT misinterpret these as representing the existing state of `origin/master` (HEAD).
- **Double-Check Upstream State Before Skipping**: Before skipping any conflicting commit or branch with `git rebase --skip`, you MUST explicitly inspect the file status and history on the upstream target branch (e.g. `origin/master` or `origin/main`) using commands like `git show origin/master:<path>` or `git log`. Never assume a change is redundant or already merged without verifying that the identical change actually exists on the upstream target.
