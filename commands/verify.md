---
description: Perform a strict project-wide verification of recent changes
---

Verify recent workspace changes ($ARGUMENTS):

1. **Rule Compliance**: Flag an immediate ERROR if any `tasks/` files or `AGENTS.md` (unless tracked) are staged or modified in `git status`.
2. **Tests & Linting**: Run the full project test suite and all linting/style/type checks (`perlcritic`, `xt/`, `eslint`, `mypy`, `ruff`) without skipping.
3. **Commit Status**: Confirm all verified changes are committed.
