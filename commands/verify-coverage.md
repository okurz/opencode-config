---
description: Run coverage tools and verify specific lines or functions are covered
---

Perform a comprehensive coverage verification of the changes.

VERIFICATION PROTOCOL:

1. **Targeted Execution**: Identify the project's coverage tool. If running the full test suite is time-consuming, you MUST run the coverage tool **only** on the specific test files relevant to the recent changes (e.g., `COVERAGE=1 make test TESTS=t/specific.t` instead of `make coverage`).
2. **Report Analysis**: Generate and read the coverage report. Use filtering options if available (e.g., `cover -select_re`) to focus the output exclusively on the files you modified.
3. **Explicit Confirmation**: Verify that the specific lines added or modified in the code are now explicitly marked as covered in the report.
4. **No Skipping**: If the coverage tool fails or produces an invalid report, you MUST troubleshoot and resolve the issue. Do NOT proceed with a commit until the coverage of your modifications is verified.

User Context: $ARGUMENTS
