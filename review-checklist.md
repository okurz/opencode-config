# Review checklist

Distilled from `review-learnings.md`. Read by `/pre-push-review` and `/address-review`. Keep each item one line, phrased as a question; merge or prune instead of growing.

## Reuse and consistency

- Does the codebase already solve this (helper, query pattern like `WITH RECURSIVE`, module)? `grep` before accepting new code.
- Are repetitive expressions, method calls, or hash lookups cached in a local variable, and repeated command flags/options consolidated into a property or helper?
- Is new prose, documentation, and UI text formatted like surrounding content (line wrapping; sentence case for headings, cards, badges, labels, tooltips, and buttons, e.g. 'Host summary', 'Warning' not 'WARNING')?

## Simplicity

- For each `eval`, `//`, `defined`, `ref` check, array-form branch, or guard `return`: `grep` callers and config defaults (e.g. `Setup.pm`)—if production guarantees the value, fix incomplete test setups instead of adding defensive fallbacks.
- Is anything created only to be deleted/ignored in some branches (dirs, temp files)? Create it only where needed.
- Can similar conditions/regexes be merged, or manual steps replaced by a library method (e.g. `Mojo::File->move_to`, `path()->slurp`/`spew`)?
- Do tests cover precedence between an explicit argument and a config fallback (arg wins; fallback used when arg absent)?
- Do multi-instance/multi-host settings or examples (e.g. global worker settings) support per-instance overrides or interpolation (port, hostname) rather than hardcoded values?

## Correctness

- If public API parameters, request payloads, or response schemas change, is backward compatibility preserved (optional fields, conflict disambiguation, accepting both scalar IDs and objects) to avoid synchronized deployments?
- Are regexes anchored (`/https?|ftp/` also matches `httpx`, `xftp`)?
- Could an unconditional overwrite/delete clobber valid state (e.g. re-sync/download replacing a populated target with an empty/absent source)?
- Under concurrency or repeated runs (thread pools, re-download/delete loops), can shared state race (files, caches, module-level YAML/XML parsers or clients)? Does skip-if-exists wrongly skip re-syncable dirs/repos, or does a cache key include a per-invocation ID (PR/request ID) that prevents hits?
- When output is captured, exceptions caught, or input dropped on parse/regex mismatch (`catch`, `return ()`, `next`, `continue`), does a log/stderr line identify the bad input instead of dropping silently?
- Are SQL subqueries and CTEs constrained to avoid full-table scans (e.g. correlated `EXISTS` instead of unconstrained `IN`)?
- Does a setting read in a shared base class leak into subclasses targeting a different host (e.g. hypervisor `sshVirtsh` inheriting SUT `sshXtermVt`)?

## Security

- Is any path, URL, or shell argument derived from user input without preventing `..` or absolute path traversal?

## External tools and dependencies

- If adding/removing/changing a dependency or external binary, is packaging updated (`dependencies.yaml`, spec `Requires`/`Recommends`) and are remaining references checked?
- In openSUSE container images, are Python deps installed via zypper RPMs (`python3-*`, e.g. `python3-PyYAML`) rather than `pip --break-system-packages` (and no stdlib in pip deps), with `#!BuildTag:` and a non-empty `_meta` title for OBS container builds?
- Are long options used for external/documented commands (`--debug`, `--mirror` instead of `-d`, `-m`)?

## Quality and Standards

- Did all local linting, static analysis (`perlcritic`, `tidy`, `eslint`, `ruff`), and unit/author tests pass?
- Does the commit Motivation state a guarantee not already provided by existing code (e.g. write-temp-then-`rename` is already atomic for readers; per-PID temp only guards concurrent writers), and do variable/option names match the code?
- Is any new user-facing config variable documented in `doc/*.md` (e.g. `doc/backend_vars.md`)?
- Is user-requested output (dry-run previews, results) visible at default CLI verbosity (not hidden at `INFO` when default is `WARNING`)?
- Are variable/parameter/target names accurate, non-colliding with existing project terms (`repo_type` vs `obs_repo_type`), consistent across siblings (`label_a`/`label_b`), and protocol-specific for global settings (`SUT_SSH_PORT` not `SUT_PORT`)?
- Do build targets (`Makefile`, `CMakeLists.txt`) write only local build artifacts without touching system paths, package managers, or root privileges?

## Scope

- Is the PR small enough to review in one sitting (< ~300 changed lines), or would a design discussion be cheaper?
