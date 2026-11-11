---
description: Create a git commit following the git-workflow skill (atomic, verified, message format)
---

Create a git commit for: $ARGUMENTS

1. Load the `git-workflow` skill with the `skill` tool and follow it strictly.
2. Inspect `git status`, `git diff`, and `git log --oneline -10`. Stage only the intended files.
3. Run the project verification (e.g. `make check-ruff`, `make test`, or the relevant check) and confirm exit code 0 before committing.
4. Write the message per the skill: imperative subject, body with Motivation / Design Choices / Benefits for fix and feat commits, hard-wrapped at 80 columns, `Related issue:` line if a ticket applies.
5. Commit with `git commit -F - <<'EOF'`. Never use `--no-verify`, never amend unless asked.
6. Run `make test-gitlint` if the project provides it and amend the message on failure.
