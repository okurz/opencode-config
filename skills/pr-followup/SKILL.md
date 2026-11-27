---
name: pr-followup
description: Use when an open pull request must be followed up in the same session, e.g. right after opening it or when its review feedback, CI status, or merge state needs a reaction.
---

# Following up on an open PR

The session that opened the PR owns the first feedback cycle: do not end it while the user
expects a reaction to review or CI. React immediately, but never merge and never chase approvals
(`Merge Advice` in `AGENTS.md`).

## Waiting

Poll with one bounded read-only `gh` call per cycle — a `sleep`/`for` loop inside a single `bash`
call with an explicit `timeout`, never one tool call per interval. Print one line per cycle
(`time | state | new items | action`). Stop a cycle on the first actionable event:

- a review or inline comment newer than the handled ids
  (`gh api repos/:owner/:repo/pulls/<n>/comments`, `.../pulls/<n>/reviews`),
- a failed required check (`gh pr view <n> --json statusCheckRollup`),
- a new merge-state blocker (conflict, `DIRTY`, blocking label, dismissed approval),
- a resolved change request that leaves a stale `CHANGES_REQUESTED` needing a re-review request.

An approval alone, a missing human approval, or a thread that is already answered is not
actionable: report the state plus the single remaining blocker ("nothing to do" when none) and stop.

## Dedupe

Keep handled ids in `~/.cache/pr-followup/<owner>-<repo>-<n>.json` (`comment_ids`, `review_ids`,
`handled_head`), updated after the fix is pushed, so a resumed session reacts only to what is new
instead of re-reading the whole thread.

## Reacting

Evaluate each new item with the `code-review` skill, then present the fix set, prevention findings
and draft thread replies and pause for approval before editing or pushing. Unattended application
(`--auto`) is allowed only when the user pre-authorized it; a `/pr-sweep` session is unattended
(`PR_SWEEP=1`), so it reports its fix set and stops instead of pausing, and applies nothing unless
`PR_SWEEP_APPLY=1` (`--apply`) is set. Verify (repo tests, lint, coverage), push, reply, update the
cache, then wait again. Replying belongs to this loop, which unlike `/address-review` reports the
pushed fix in the thread it answers.

## Several PRs

More than one own open PR that owes an answer: `/pr-sweep` drives the loop instead of repeating
`/pr-watch` by hand.

- **Scope**: only my PRs that still owe an answer — `CHANGES_REQUESTED`, or a failing required check.
  A PR waiting for a missing approval owes nothing (`Merge Advice`), and a PR another session already
  works stays out (`--exclude 1,2`).
- **One worktree per PR**: reuse the checkout that already has the PR branch, else create
  `~/local/worktrees/<repo>-<PR#>`. Never run two sessions in one worktree, and never work a PR whose
  worktree is dirty or lacks commits of the PR head: both mean an earlier session is mid-change.
- **Writes stay serial**: work the PRs one at a time. `-j N` pays off only when the endpoint has slots
  and every session stays inside its own worktree; reviewer-facing text is where parallel sessions
  contradict each other.
- **Test isolation**: openQA's `TEST_PG_PATH` defaults to one fixed `/dev/shm/tpg`, so concurrent suites
  share a cluster. Give each session its own (`/dev/shm/tpg-sweep-<PR#>`), or run only the tests that
  touch the diff and leave the full matrix to PR CI.
- **Resume**: `<cache>/<slug>.json` records the head each session worked on, `<cache>/logs/<slug>.log`
  its transcript; a log ending in `PR SWEEP TIMEOUT` is unfinished work, not an approval.

## Stopping

Stop when nothing is actionable and the PR is green, when the user stops the loop, or when the
remaining work is human-only (approval, label) or would hold the session for days: record
`## Blocked` with the read-only verification command in the plan or hand off, and name the exact
command that resumes the watch.
