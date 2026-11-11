---
description: Create a git commit following the git-workflow skill (atomic, verified, message format)
---

Create a git commit for: $ARGUMENTS

1. Load and strictly follow the `git-workflow` skill.
2. Inspect `git status`, `git diff`, and `git log --oneline -10`; stage only intended files.
3. Run project lint/test verification (confirm exit code 0 and check final 20 lines), commit via `git commit -F - <<'EOF'` (never `--no-verify` or unrequested `--amend`), and run `make test-gitlint` if available.
