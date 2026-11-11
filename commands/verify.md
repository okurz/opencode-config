---
description: Perform a strict project-wide verification of recent changes
---

Perform a comprehensive verification of the changes made in the current workspace according to the projects rule.

VERIFICATION PROTOCOL:
1. **Rule Compliance**: Check if any 'tasks/' files or 'GEMINI.md' were accidentally staged or modified in Git. If so, list them immediately as ERRORS.
2. **Comprehensive Code Integrity**: Run the **entire** project-specific test suite (e.g., `make test`, `npm test`, `pytest`). Do NOT skip any tests unless explicitly instructed.
3. **Static Analysis & Linting**: Proactively identify and execute project-specific linting, style, and type-checking tools (e.g., `perlcritic`, `xt/` tests, `eslint`, `mypy`, `ruff`). Adhere to project style from the first implementation turn.
4. **Commit Status**: Ensure that all pending changes are committed in the version control system.

User Context: $ARGUMENTS
