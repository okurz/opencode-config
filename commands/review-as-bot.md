---
description: Review a pull or merge request (GitHub or GitLab) as the configured review bot (defaults to next reviewable open PR/MR)
argument-hint: "<pr|url> [--post] [--dry-run]"
---

Review a pull or merge request as the configured review bot. `$ARGUMENTS` is the target (PR/MR
number, URL, or empty) followed by optional flags.

0. **Mode**: take the first non-flag token as the target and parse the flags from the rest.
   - `--dry-run`: print the finished review body and the chosen verdict, post nothing. Use this
     when a post is not (yet) approved.
   - `--post`, or `REVIEW_BOT_POST=1`: skip the write gate in step 5 and submit immediately.
   - Neither set: interactive session, the step 5 write gate applies.
   - `--dry-run` and `--post` are GitHub-only. On GitLab keep the step 5 gate and the `glab-as-bot`
     flow below unchanged.
   - In a non-interactive run (`pi -p`) nobody answers: never ask a question, and never end the run
     without either a submitted review or a printed error plus a non-zero exit.

1. **Host & Tool Detection**:
   Detect hosting forge from the target URL or from `git remote get-url origin`:
   - **GitHub**: every GitHub call in this workflow must go through `gh-as-bot` (wraps `gh` with
     credentials from `~/.config/review-assistant/write*.env`). A bare `gh` call uses the human
     account and mis-attributes the review.
     Verify bot identity: `gh-as-bot api user --jq .login`.
   - **GitLab**: use `glab-as-bot` (wraps `glab` with credentials from `~/.config/review-assistant/<host-slug>.env`).
     Load the `gitlab-review` skill.
     Verify bot identity: `glab-as-bot api user | jq -r '.username + " (" + .name + ")"'`.

2. **Select Target PR/MR**:
   - If the target provides a number or URL, target that PR/MR.
   - If the target is empty, find the highest-priority open candidate in the current repository that is not draft, not authored by the bot/reviewer identity, and still needs review:
     - **GitHub**:
       Use `gh-pr-triage` (or `gh-as-bot pr list`):
       ```sh
       # Fast unblocking: PRs with >=1 approval, 0 changes requested, passing CI, mergeable
       gh-pr-triage --ready-to-approve
       # Or unreviewed queue:
       gh-pr-triage --unreviewed
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
   - Isolate inspection and any test run in `git worktree add --detach /tmp/review-<PR> <head-sha>`
     (remove it at the end). Never modify the working tree of the checkout the run starts in.
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
   - With `--dry-run`: print `--- DRAFT REVIEW (<forge> <target>, verdict, reviewer identity) ---`,
     the body, and `--- END DRAFT, nothing posted ---`. Post nothing, exit 0.
   - Otherwise, unless `--post`/`REVIEW_BOT_POST=1` was given, adhere to the write gate: present the
     target number, forge, active reviewer identity, draft review verdict, and comment body to the
     user for approval before submitting.
   - Submit:
     - **GitHub**:
       ```sh
       gh-as-bot pr review <PR> --<verdict> --body "<comment>"
       gh-as-bot api repos/<owner>/<repo>/pulls/<PR>/reviews --jq '.[-1] | .user.login + " " + .state + " " + .html_url'
       ```
       The second command is the post-condition: it must report the bot login, not the human account.
       Treat any other login as a failed run and say so.
     - **GitLab**:
       Write body to file, then comment and optionally approve:
       ```sh
       glab-as-bot mr note create <MR> -m "$(cat /tmp/mr-reviews/<MR>.body)"
       # If verdict is APPROVE:
       glab-as-bot mr approve <MR>
       ```
