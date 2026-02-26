---
description: Perform a strict project-wide verification of recent changes
---

Perform a comprehensive verification of the changes made in the current workspace according to the projects rule.

VERIFICATION PROTOCOL:
1. **Rule Compliance**: Check if any 'tasks/' files or 'GEMINI.md' were accidentally staged or modified in Git. If so, list them immediately as ERRORS.
2. **Code Integrity**: Run the project-specific test suites (e.g. `make test-with-coverage` or `make test`).
3. **Commit Status**: Ensure that all pending changes are commited in the version control system

User Context: $ARGUMENTS
