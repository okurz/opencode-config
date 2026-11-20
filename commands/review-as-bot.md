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
   - In a non-interactive run (`pi -p`) nobody answers: never ask a question and never end with an
     interactive prompt. Finish with a submitted review (`--post`), the dry-run block, the
     blocked-write block, or a `--- REVIEW FAILED ---` block. The harness owns the exit code.
   - This command's output contract and verdict rubric override any loaded skill. In `pi -p` the
     `code-review` skill's approval/todowrite workflow does not apply: do not ask, offer, plan, or
     request confirmation.
   - **One target per invocation.** A scope is not a target: a count ("any 10 PRs"), "all"/"every",
     an org/user or repository-wide request, or several numbers/URLs. For a scope, print
     `--- REVIEW FAILED (<forge> <scope>) ---` plus
     `one target per invocation; use /review-as-bot-batch <scope> [--post|--dry-run]`, and stop.
     Do not enumerate, triage, or call any tool.

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
   - If the target provides a number or URL, target that PR/MR. Refuse a merged or closed target:
     `gh-as-bot api repos/<owner>/<repo>/pulls/<PR> --jq .state`.
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
   - Isolate inspection in `git worktree add --detach <temp-root>/<owner>-<repo>-<PR> <head-sha>`
     (`<temp-root>` defaults to `/tmp`; remove the worktree before step 5). Keep it in the temp
     root: when a repo needs a sibling checkout (distri tests need `os-autoinst`), symlink that
     checkout inside the worktree instead of relocating it. Never modify the working tree of the
     checkout the run starts in.
   - Test budget: run at most the targeted test for the changed files, once. Skip the run and record
     `not verified (environment)` when the repo layout, dependencies, or harness are unavailable.
     Never run coverage, `make tidy`, or checkstyle unless the PR changes those themselves. Do not
     retry an environment failure.
   - Tool budget: after the diff, CI state, review threads, and at most one targeted test, stop
     investigating and draft. Aim for at most ~12 tool calls; do not chase a helper's full call
     graph or an unrelated test failure.
   - Write planned inline comments to `<temp-root>/<owner>-<repo>-<PR>.inline.json` as
     `[{"path": ..., "line": ..., "body": ...}]` so the claim gate can validate them.
   - When you run a command you will cite under "Verified by execution", append the command and its
     exit code to `<temp-root>/<owner>-<repo>-<PR>.evidence.log` (`$ <command>` then `exit=<code>`).
   - Inspect check runs / CI pipelines:
     - GitHub: `gh-as-bot pr checks <PR>`.
     - GitLab: pipeline status from `glab-as-bot api "projects/<owner>%2F<repo>/merge_requests/<MR>"`.
   - Quote review facts verbatim, never from memory: approvals, requested reviewers, check counts and
     reviewer logins come from
     `gh-as-bot pr view <PR> --json reviews,reviewDecision,statusCheckRollup`.
   - Review replies live in the same `repos/<owner>/<repo>/pulls/<PR>/comments` listing; group by
     `in_reply_to_id`. Never call an `/in_reply_to` endpoint.
   - Verification runs: use unauthenticated API/`openqa-cli`; never read `~/.config/openqa/client.conf`
     or other credential files.
   - Read `~/.config/opencode/review-checklist.md` and load only skills that supply domain facts
     (`openqa`, `perl-dev`, `python-dev`, `testing`). Do not load `code-review` (it is for addressing
     feedback, not bot review). If `openqa` is loaded, ignore its PR-review/post playbook
     (`openqa/SKILL.md` section F).
   - Record the basis in the draft: `Basis: review-checklist.md; skills: <names or none>`.

4. **Assess Quality**:
   - Verify alignment with project conventions, commit style (Conventional Commits, 50/80 rule), and
     test coverage requirements.
   - For dependency updates: check for breaking changes, dropped assets, or failing test suites.
   - Determine the verdict from the findings, not from the PR's overall impression. This rubric
     overrides any loaded skill (including `code-review-and-quality`'s "approve if it improves code
     health"):
     - Label every finding `blocking` or `non-blocking` with a one-line justification.
     - If a finding asks for any edit, it is `blocking`: mergify merges on approvals and does not
       check unresolved threads, so an approval carrying edit requests drops them. Do not propose a
       concrete edit and then approve; if it is not worth blocking, keep it as an observation without
       naming an edit.
     - `blocking` also covers a concrete failure of the PR's stated goal (data loss, wrong
       branch/condition, a branch the PR claims to cover but does not) and an existing helper/rule
       the author has not already committed to follow. Do not downgrade a concrete failure to an
       open question by calling it "could" or "heuristic".
     - `non-blocking` is an observation or open question with no edit request, a readability /
       duplication / preference item that creates no concrete failure, or documented residual risk
       that the change strictly reduces and the PR does not claim to eliminate. Do not call a
       finding blocking after admitting the current code works; demote it.
     - `APPROVE` when nothing is left to change. `COMMENT` only when the PR cannot be judged at all
       (e.g. unreadable diff, CI outage); code findings are `REQUEST_CHANGES`, not `COMMENT`.
     - Do not re-raise a point a human already answered or dismissed in a reply on the same commit.
     - Anchor blocking findings as inline comments on the line
       (`gh-as-bot api repos/<owner>/<repo>/pulls/<PR>/reviews -X POST -f event=REQUEST_CHANGES
       -f body=... -f 'comments[][path]=<file>' -F 'comments[][line]=<line>' -f 'comments[][body]=...'`),
       so the author sees them next to the code; keep body-only findings for the summary. When the line is
       not part of the diff (unchanged line, or the review is submitted after a force-push), keep the
       finding in the body instead of failing the API call.
   - Keep the verdict stable per commit, not per sampling run: check the bot's own earlier reviews on this
     head sha and its still-unresolved threads. If it requested changes on this sha and those threads are
     unresolved, keep that verdict and only add what the earlier review missed. Approve once the author
     resolved them, even without a new commit; never let a re-roll of the same unresolved state change
     the verdict.
   - Name no model in the review body: the review speaks for the bot, not for a model.
   - Keep "verified by execution" (command and result) apart from "read only" in the body. Only
     claim verification for a command that appears in the evidence log with exit 0; if you did not
     run it, put the evidence under "Read only".

5. **Draft & Submit**:
   - Formulate a concise, pragmatic review summary.
   - If a write tool is available, write the draft to `<temp-root>/<owner>-<repo>-<PR>.md` outside
     the worktree; otherwise keep it in memory. The file, when written, is the source of truth and
     the printed block must match it.
   - Run the claim gate before printing or posting:
     ```sh
     python3 ~/.config/opencode/tools/verify-review-claims.py \
       --repo <owner>/<repo> --pr <PR> --head <head-sha> \
       --draft <temp-root>/<owner>-<repo>-<PR>.md \
       --inline <temp-root>/<owner>-<repo>-<PR>.inline.json \
       --evidence <temp-root>/<owner>-<repo>-<PR>.evidence.log
     ```
     If it exits non-zero, do not post and do not print a DRAFT block: fix the draft and re-run, or
     print `--- REVIEW BLOCKED (claim verification failed) ---` plus the gate errors and stop. A
     draft the gate rejected must never be posted. Pass `--strict-evidence` for `--post`; for
     `--dry-run` the same gate runs with evidence optional.
   - With `--dry-run`: after all tool work, worktree removal, and the claim gate passes, print
     exactly one final message:
     `--- DRAFT REVIEW (<forge> <target>, <VERDICT>, reviewer <identity>) ---`
     where `<target>` is `<owner>/<repo>#<PR>` on GitHub or `<owner>/<repo>!<MR>` on GitLab, the
     body, and `--- END DRAFT, nothing posted ---`. The verdict is uppercase. No text before or
     after, no notes, no "to submit" offer, no exit code, and no tool calls after it. If you already
     printed a draft earlier, repeat the full block as the final message. Post nothing.
   - If you cannot finish, print `--- REVIEW FAILED (<forge> <target>) ---` plus one line of reason
     and stop; do not print a partial draft.
   - Otherwise, unless `--post`/`REVIEW_BOT_POST=1` was given, keep the write gate: print the same
     draft inside `--- REVIEW BLOCKED (write gate, not posted) ---` and stop. In `pi -p` never ask
     for approval and never post without `--post`.
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
