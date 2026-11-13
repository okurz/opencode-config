---
name: gitlab-review
description: Use when inspecting, reviewing, triaging, commenting, or approving GitLab merge requests using glab or glab-as-bot.
---

# GitLab merge request review

## CLI helper & identity

- Use `glab-as-bot` to invoke `glab` under configured review credentials. It automatically reads `~/.config/review-assistant/<host-slug>.env` (e.g. `gitlab-suse-de.env`) and injects `GITLAB_TOKEN` and `GITLAB_HOST`.
- Check active identity before writing:
  ```sh
  glab-as-bot api user | jq -r '.username + " (" + .name + ") bot=" + (.bot|tostring)'
  ```
- Bot provisioning:
  - GitLab Self-Managed supports **Project Access Tokens** (Settings -> Access Tokens) or **Group Access Tokens** with role Developer / Maintainer and scopes `api` (or `read_api` + `write_repository`).
  - When configuring a dedicated bot, name it appropriately (e.g. `os-autoinst-review` or project bot), save its token to `~/.config/review-assistant/<host-slug>.env` (`chmod 600`), and the helper automatically adopts that identity.

## Finding candidates

- `glab mr list` lacks a `--state` flag on some versions; query the REST API directly for robust sorting:
  ```sh
  # URL-encode the repo path, e.g. openqa/salt-states-openqa -> openqa%2Fsalt-states-openqa
  glab-as-bot api "projects/<owner>%2F<repo>/merge_requests?state=opened&order_by=created_at&sort=asc&per_page=100" \
    | jq -r '.[] | select(.draft==false) | [.iid, .created_at[0:10], .author.username, .title, (.reviewers|length), (.detailed_merge_status // "n/a")] | @tsv'
  ```
- Exclude MRs authored by the active reviewer identity when reviewing incoming work.
- Check approvals via the separate `/approvals` endpoint (the single-MR endpoint does not list `approved_by` users):
  ```sh
  glab-as-bot api "projects/<owner>%2F<repo>/merge_requests/<iid>/approvals" | jq -r '.approved_by[].user.username'
  ```

## Inspection & Rebase Truth

- **Details & Diff**:
  ```sh
  glab-as-bot mr view <iid>
  glab-as-bot mr diff <iid>
  glab-as-bot api "projects/<owner>%2F<repo>/merge_requests/<iid>" | jq -r '"pipeline=\(.head_pipeline.status // "none") changes=\(.changes_count)"'
  ```
- **Rebase Truth**:
  GitLab's `detailed_merge_status` can be stale or `unchecked`. Verify locally without checking out the branch:
  ```sh
  git fetch origin "refs/merge-requests/<iid>/head:mr-<iid>" --quiet
  git merge-tree --write-tree origin/master mr-<iid>
  ```
  A non-zero exit or `CONFLICT` output indicates a rebase is required before merge.

## Verdicts & Submission

GitLab has no native `REQUEST_CHANGES` review verb. Map verdicts as follows:

| Verdict | GitLab Action |
|---|---|
| `APPROVE` | Submit review comment + `glab-as-bot mr approve <iid>` |
| `COMMENT` | Submit review comment |
| `REQUEST_CHANGES` | Submit review comment listing blocking items |

- **Submitting comments**: Write review bodies to temporary files first to avoid shell quoting and backtick breakage:
  ```sh
  glab-as-bot mr note create <iid> -m "$(cat /tmp/mr-reviews/<iid>.body)"
  ```
- **Approving**:
  ```sh
  glab-as-bot mr approve <iid>
  ```
- If a call fails with `403 {error: insufficient_scope}`, the token lacks `api` write scope; verify token permissions in `~/.config/review-assistant/<host-slug>.env`.
