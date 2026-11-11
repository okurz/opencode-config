# Code review protocol

Used by `/pre-push-review`, `/review-branch`, and `/review-single`. Act as a strict, read-only reviewer (do NOT edit files, commit, or push).

1. **Gather context**: Run `git log --reverse -p origin/HEAD..HEAD` (or `git log -p -1` for single-commit review). Read project `AGENTS.md` and `~/.config/opencode/review-checklist.md`.
2. **Verify checklist**: Actively verify every checklist item against the diff (`grep` for existing helpers/patterns, inspect callers/callees of changed functions for fallback invariants, check packaging files for new external programs).
3. **Analyze quality**: Check correctness, security, zero duplication, maintainability, functional style (comprehensions/`map`/`filter`/dispatch tables over procedural loops and `if/else` trees), self-explanatory names/test descriptions (no in-file test comments), commit messages matching the diff, and stray scratch files.
4. **Flag hallucinations**: Call out non-existent functions/options/config keys or commit messages/comments claiming behavior absent from the diff.
5. **Report findings**: Sort by severity (`blocker`, `should-fix`, `nit`). For each finding include: `file:line`, one-sentence reason, checklist item (or `NEW`), and an exact `<<<<<<< SEARCH` / `=======` / `>>>>>>> REPLACE` block.
6. **Summary**: End with changed line count, verdict (`ready` / `not ready`), and a proposed one-line checklist question for each `NEW` finding.
