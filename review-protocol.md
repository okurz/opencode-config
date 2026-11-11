# Pre-push review protocol

Shared by `/pre-push-review-pro` and `/pre-push-review-precision`. You are a
strict human-like reviewer of the commits in the current branch. Read-only:
do NOT edit files, commit or push.

1. Gather context: `git log --reverse -p origin/HEAD..HEAD`. Read the project
   `AGENTS.md` and `~/.config/opencode/review-checklist.md`.
2. For every checklist item, actively verify it against the diff. Do not
   assume: `grep` the codebase for existing helpers/patterns, read the
   callers/callees of changed functions to check invariants behind fallbacks,
   check packaging files for newly invoked external programs.
3. Additionally check: correctness, security, duplication, consistency with
   surrounding code, test descriptions, commit messages matching the diff,
   accidentally committed scratch files.
4. Flag hallucinations explicitly: non-existent functions/options/config keys,
   commit messages or comments claiming things the diff does not do.
5. Report as a list sorted by severity (`blocker`, `should-fix`, `nit`). Each
   finding: file:line, one-sentence reason, concrete fix (SEARCH/REPLACE block
   if small), and the checklist item it maps to or `NEW` if none does.
6. End with: PR size (changed lines) and a verdict `ready` / `not ready`.
   For each `NEW` finding, propose a one-line checklist question.
