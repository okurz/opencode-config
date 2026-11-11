---
name: rpm-packaging
description: Use when building RPM/spec files, fixing missing/unresolvable OBS build dependencies, or resolving native-extension link errors (-lpython, abi3).
---

# Packaging & dependency discipline

- **Lower Spec Requirements First**: On missing/unresolvable build dependencies, do NOT blindly update the dependency. Inspect upstream's true minimum in the source archive (`pyproject.toml`, `setup.py`, `Cargo.toml`) and lower the `.spec` requirement (e.g. inside older-distro `%else` blocks) if safe.
- **Fix `-lpython3.x` Link Errors**: When native extensions (e.g. Rust/Maturin) fail with `unable to find library -lpython3.x` (missing/disabled `abi3`), add `BuildRequires: %{use_python}-devel` to the `.spec`.
