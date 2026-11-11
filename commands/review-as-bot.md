---
description: Review a GitHub pull request as a designated review bot using review-assistant token (defaults to next reviewable open PR)
---

Review a GitHub pull request as the configured review bot (`$ARGUMENTS` can be a PR number, URL, or empty).

1. **Bot CLI Helper**:
   Use `gh-as-bot` (wraps `gh` with the bot's credentials). It automatically selects:
   - `~/.config/review-assistant/write.env` (fine-grained PAT) for `os-autoinst/*` repositories.
   - `~/.config/review-assistant/write-classic-public_repo.env` (classic PAT with `public_repo` scope) for non-`os-autoinst` repositories (e.g. `openSUSE/*`).
   Verify bot identity if needed:
   ```sh
   gh-as-bot api user --jq .login
   ```

2. **Select Target PR**:
   - If `$ARGUMENTS` provides a PR number or URL, target that PR.
   - If `$ARGUMENTS` is empty, find the first open PR in the current repository that is not draft and still needs review from the bot:
     ```sh
     gh-as-bot pr list --state open --json number,title,isDraft,reviews --limit 20
     ```
     Pick the highest-priority candidate (e.g. oldest unreviewed non-draft PR or ready Dependabot bump).

3. **Inspect & Triage**:
   - Inspect PR details and diff: `gh-as-bot pr view <PR> --json title,body,author,headRefName` and `gh-as-bot pr diff <PR>`.
   - Inspect check runs: `gh-as-bot pr checks <PR>`.
   - Load domain/testing skills matching the project (e.g. `openqa`, `perl-dev`, `python-dev`, `testing`, `code-review`).

4. **Assess Quality**:
   - Verify alignment with project conventions, commit style (Conventional Commits, 50/80 rule), and test coverage requirements.
   - For dependency updates: check for breaking changes, dropped assets, or failing test suites.
   - Determine verdict: `APPROVE`, `COMMENT`, or `REQUEST_CHANGES`.

5. **Draft & Submit**:
   - Formulate a concise, pragmatic review summary.
   - Unless instructed to post directly, adhere to the write gate: present the target PR number, title, draft review verdict, and comment body to the user for approval before submitting.
   - Once approved, submit via:
     ```sh
     gh-as-bot pr review <PR> --<verdict> --body "<comment>"
     ```
