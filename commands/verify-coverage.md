---
description: Run coverage tools and verify specific lines or functions are covered
---

Verify statement coverage of recent changes ($ARGUMENTS):

1. Load the `testing` skill and run the project's coverage tool ONLY on the test files relevant to your changes (e.g. `COVERAGE=1 make test TESTS=t/specific.t`).
2. Filter the report to modified files (e.g. `cover -select_re`) and confirm every added/modified line is covered before committing. Troubleshoot any tool failure; never skip.
