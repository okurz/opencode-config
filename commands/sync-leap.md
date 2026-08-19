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
6. If unresolvable dependencies are found:
   a) FIRST check if the dependency requirements in the `.spec` file can be safely lowered to match the versions available in Leap (by extracting and inspecting upstream's actual requirements in e.g. `pyproject.toml` from the source archive).
   b) IF requirements can be lowered, edit the `.spec` file, commit, and push to the PR branch.
   c) ONLY IF they cannot be lowered, pipe the output to `osc-sync-deps` to get a list of source packages that need syncing.
7. Present the list of missing dependencies to the user and offer to guide them through syncing those packages next.
8. If the package builds but fails during linking with `unable to find library -lpython3.x` (common for Rust extensions when `abi3` is disabled), add `BuildRequires: %{use_python}-devel` to the `.spec` file.