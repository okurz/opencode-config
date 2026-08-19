# Skill: leap-sync

## Purpose
Automate the update of openSUSE Leap packages from the Factory branch following the git-workflow. This skill is generic and works for any package repository following the `factory` and `leap-X.Y` branch naming convention.

## Tools
- `osc-sync-leap`: Python script (using `typer`) for Git and Gitea (`tea`) automation.
- `osc-get-pr-status`: Extracts unresolvable dependency messages from OBS build results.
- `osc-sync-deps`: Suggests source packages to sync based on missing dependencies.
- `tea`: Gitea CLI for Pull Request creation.

## Workflow
1. **Navigate**: Go to the root of the package git repository.
2. **Sync**:
   - Run `osc-sync-leap --dry-run` to verify.
   - Run `osc-sync-leap` to perform the sync and create PRs.
3. **Verify and Resolve Dependencies**:
   - If builds fail due to missing dependencies, use `osc-get-pr-status <obs_project> <package>` to extract the unresolvables.
   - **First, try to lower requirements**: Before syncing a dependency, check if the newer version is actually required by upstream. Extract `pyproject.toml` or `setup.py` from the `.obscpio` (e.g., `cpio -i --to-stdout */pyproject.toml < *.obscpio`). If the upstream requirement is lower than what the `.spec` file demands, lower the `%global <Dep>_version` in the `.spec` file (typically in the non-poetry `%else` block for Leap).
   - **Second, sync dependencies**: If the dependency truly needs an update, pipe the output of `osc-get-pr-status` to `osc-sync-deps` to get a list of source packages that need to be synced from Factory to Leap.
   - **Third, check linking errors**: If a Python package builds native extensions (e.g. via Rust/maturin) and linking fails with `unable to find library -lpython3.x`, this often means `abi3` compatibility is disabled. You must add `BuildRequires: %{use_python}-devel` to the `.spec` file so the linker can find `libpython`.
   - Recursively apply this workflow to those missing dependencies.

## Global Installation
1. Move `sync_leap.py` to `~/bin/osc-sync-leap` (ensure `~/bin` is in your `$PATH`).
2. Create the skill directory: `mkdir -p ~/.config/opencode/skills/leap-sync/`.
3. Copy this `SKILL.md` to `~/.config/opencode/skills/leap-sync/SKILL.md`.

## Sync Logic
- Removes root files in the target Leap branch.
- Copies all files from the `factory` branch.
- Creates a Pull Request for each target branch.
