---
description: Automate the sync of a package from Factory to Leap branches
---

Execute the Leap sync workflow for the package in the current directory.
Target branches or specific arguments (optional): $ARGUMENTS

STRICT RULES:
1. Automatically load the `leap-sync` skill to gain context on the tools.
2. Run `osc-sync-leap --dry-run` to show the planned sync operations.
3. PAUSE AND WAIT. Present the dry-run output and ask for user confirmation before proceeding.
4. ONLY AFTER user approval, execute `osc-sync-leap` with the provided arguments (or defaults if none provided).
5. After the sync and PR creation, check if an OBS project is provided or known. If so, run `osc-get-pr-status <obs_project> <package>` to check for unresolvable dependencies.
6. If unresolvable dependencies are found, pipe the output to `osc-sync-deps` to get a list of source packages that also need syncing.
7. Present the list of missing dependencies to the user and offer to guide them through syncing those packages next.