---
description: Automate the sync of a package from Factory to Leap branches
---

Execute the Leap sync workflow for the current package repository. Optional target branches/args: $ARGUMENTS

1. Load and follow the `leap-sync` and `rpm-packaging` skills.
2. Run `osc-sync-leap --dry-run`, present the planned operations, and PAUSE AND WAIT for user approval.
3. After approval, run `osc-sync-leap $ARGUMENTS`.
4. If an OBS project is known/provided, check `osc-get-pr-status <obs_project> <package>` and resolve unresolvables or `-lpython3.x` link errors per `leap-sync` (if `.spec` requirements can be lowered or `BuildRequires: %{use_python}-devel` added, edit `.spec`, commit, and push to the PR branch; otherwise report `osc-sync-deps` output and offer to sync missing dependencies).
