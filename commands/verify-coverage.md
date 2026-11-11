---
description: Run coverage tools and verify specific lines or functions are covered
---

Perform a comprehensive coverage verification of the changes.

VERIFICATION PROTOCOL:

1. **Tool Execution**: Identify and execute the project's coverage tool (e.g., `make COVERAGE=1`, `pytest --cov`, `go test -cover`).
2. **Report Analysis**: Read the coverage report (text, HTML, or JSON) to find the specific files and lines affected by the changes.
3. **Explicit Confirmation**: Verify that the lines previously reported as missing coverage are now explicitly marked as covered in the new report.
4. **No Skipping**: If the coverage tool fails or produces an invalid report, you MUST troubleshoot and resolve the issue. Do NOT proceed with a commit until the coverage is verified.

User Context: $ARGUMENTS
