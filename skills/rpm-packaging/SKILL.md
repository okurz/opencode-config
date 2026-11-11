---
name: rpm-packaging
description: Use when building RPM/spec files, fixing package builds with missing or unresolvable dependencies, or resolving native-extension link errors (Rust/Maturin, abi3, -lpython). Covers lowering spec requirements to match the distribution.
---

# Packaging & dependency discipline

- **Investigate Unresolvables**: When a package build fails due to missing or unresolvable dependencies, DO NOT blindly update the dependency. First, investigate if the requirement in the spec file can be lowered to match the currently available version in the distribution.
- **Check Upstream Requirements**: Extract the upstream requirement configuration (e.g. `pyproject.toml`, `setup.py`, or `Cargo.toml`) from the source archive to verify the true minimum required version.
- **Lower Requirements if Safe**: If upstream's requirement is lower than what the spec file demands, modify the spec file (often inside distribution-specific blocks like `%else` for older releases) to match the available version.
- **Handle Linking Errors**: If a package with native extensions (e.g., Rust/Maturin) fails during linking with `unable to find library -lpython3.x`, it likely means the `abi3` feature is disabled or missing. Ensure `BuildRequires: %{use_python}-devel` is present so the linker can find `libpython`.
