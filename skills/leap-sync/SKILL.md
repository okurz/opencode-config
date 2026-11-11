---
name: leap-sync
description: Use when syncing openSUSE Leap packages from the Factory branch, resolving unresolvable OBS build dependencies, or opening leap-X.Y branch PRs.
---

# Leap package sync (`factory` -> `leap-X.Y`)

## Tools
- `osc-sync-leap`: Syncs `factory` into target `leap-X.Y` branches (replaces root files) and opens Gitea PRs via `tea`.
- `osc-get-pr-status <obs_project> <package>`: Extracts unresolvable dependency messages from OBS build results.
- `osc-sync-deps`: Reads `osc-get-pr-status` output and lists source packages to sync.

## Workflow
1. From the package repo root, run `osc-sync-leap --dry-run` to preview, then `osc-sync-leap` to sync and open PRs.
2. If builds fail, run `osc-get-pr-status <obs_project> <package>` and load the `rpm-packaging` skill:
   - **Lower spec requirements first**: Check upstream's true minimum in `.obscpio` (e.g. `cpio -i --to-stdout */pyproject.toml < *.obscpio`); if lower than `.spec`, lower `%global <Dep>_version` (typically in the Leap `%else` block).
   - **Sync missing deps**: Only if upstream requires the newer version, pipe `osc-get-pr-status` into `osc-sync-deps` and recursively sync those packages.
   - **Fix `-lpython3.x` link errors**: Add `BuildRequires: %{use_python}-devel` when `abi3` is disabled (e.g. Rust/maturin).
