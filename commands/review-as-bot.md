---
description: Review a pull or merge request (GitHub or GitLab) as the configured review bot (defaults to next reviewable open PR/MR)
---

Review a pull or merge request as the configured review bot (`$ARGUMENTS` can be a PR/MR number, URL, or empty).

1. **Host & Tool Detection**:
   Detect hosting forge from `$ARGUMENTS` URL or from `git remote get-url origin`:
   - **GitHub**: use `gh-as-bot` (wraps `gh` with credentials from `~/.config/review-assistant/write*.env`).
     Verify bot identity: `gh-as-bot api user --jq .login`.
   - **GitLab**: use `glab-as-bot` (wraps `glab` with credentials from `~/.config/review-assistant/<host-slug>.env`).
     Load the `gitlab-review` skill.
     Verify bot identity: `glab-as-bot api user | jq -r '.username + " (" + .name + ")"'`.

2. **Select Target PR/MR**:
   - If `$ARGUMENTS` provides a number or URL, target that PR/MR.
   - If `$ARGUMENTS` is empty, find the highest-priority open candidate in the current repository that is not draft, not authored by the bot/reviewer identity, and still needs review:
     - **GitHub**:
       ```sh
       gh-as-bot pr list --state open --json number,title,isDraft,reviews --limit 20
       ```
     - **GitLab**:
       ```sh
       glab-as-bot api "projects/<owner>%2F<repo>/merge_requests?state=opened&order_by=created_at&sort=asc&per_page=100" \
         | jq -r '.[] | select(.draft==false) | [.iid, .created_at[0:10], .author.username, .title, (.reviewers|length), (.detailed_merge_status // "n/a")] | @tsv'
       ```

3. **Inspect & Triage**:
   - Inspect details and diff:
     - GitHub: `gh-as-bot pr view <PR> --json title,body,author,headRefName` and `gh-as-bot pr diff <PR>`.
     - GitLab: `glab-as-bot mr view <MR>` and `glab-as-bot mr diff <MR>`. Check mergeability with `git merge-tree`.
   - Inspect check runs / CI pipelines:
     - GitHub: `gh-as-bot pr checks <PR>`.
     - GitLab: pipeline status from `glab-as-bot api "projects/<owner>%2F<repo>/merge_requests/<MR>"`.
   - Load domain/testing skills matching the project (e.g. `openqa`, `perl-dev`, `python-dev`, `testing`, `code-review`).

4. **Assess Quality**:
   - Verify alignment with project conventions, commit style (Conventional Commits, 50/80 rule), and test coverage requirements.
   - For dependency updates: check for breaking changes, dropped assets, or failing test suites.
   - Determine verdict: `APPROVE`, `COMMENT`, or `REQUEST_CHANGES`.

5. **Draft & Submit**:
   - Formulate a concise, pragmatic review summary.
   - Unless instructed to post directly, adhere to the write gate: present the target number, forge, active reviewer identity, draft review verdict, and comment body to the user for approval before submitting.
   - Once approved:
     - **GitHub**:
       ```sh
       gh-as-bot pr review <PR> --<verdict> --body "<comment>"
       ```
     - **GitLab**:
       Write body to file, then comment and optionally approve:
       ```sh
       glab-as-bot mr note create <MR> -m "$(cat /tmp/mr-reviews/<MR>.body)"
       # If verdict is APPROVE:
       glab-as-bot mr approve <MR>
       ```
