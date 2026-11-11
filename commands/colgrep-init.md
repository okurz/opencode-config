---
description: Initialize or update colgrep semantic index for the current project or a specified path.
---

Initialize or update the `colgrep` semantic index for the project.

Target path: ${ARGUMENTS:-.}

STEPS:
1. Verify `colgrep` is available in PATH (`which colgrep`).
2. Run `colgrep init ${ARGUMENTS:-.}` to build or refresh the semantic code index.
3. Display the status with `colgrep status`.
