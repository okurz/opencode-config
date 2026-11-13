# Review checklist

Distilled from `review-learnings.md`. Read by `/pre-push-review` and `/address-review`. Keep each item one line, phrased as a question; merge or prune instead of growing.

## Reuse and consistency

- Does the codebase already solve this (helper, query pattern like `WITH RECURSIVE`, module)? `grep` before accepting new code.
- Are repetitive expressions, method calls, or hash lookups cached in a local variable, repeated command flags/options consolidated into a property or helper, and repeated URLs/values across CI steps factored into workflow/job `env`?
- Is new prose, documentation, and UI text formatted like surrounding content (line wrapping; sentence case for headings, cards, badges, labels, tooltips, buttons and dropdown options, including every word inside parentheses, e.g. 'Host summary', 'Dark mode (Halloween season)' not 'Dark mode (Halloween Season)', 'Warning' not 'WARNING')?

## Simplicity

- For each `eval`, `//`, `defined`, `ref` check, type coercion (`int`, `0 +`), guard `return`, predicate inlined/copied from another context (e.g. a UI display condition reused in a data-selection loop), or test environment override: `grep` callers, config defaults (e.g. `Setup.pm`, module constants), ORM schema column inflation/defaults (e.g. integer primary keys like `->id`), and upstream query `WHERE` filters (e.g. `_previous_scenario_jobs` restricts to `state=done` + `COMPLETE_RESULTS`)—if a clause is already guaranteed, drop it; when data is missing in a consumer, fix the upstream producer/loader (schemas, key names like `scminfo` vs `scm_info`) instead of adding a defensive fallback or dynamic fetch; and avoid arbitrary non-zero delays (`0.01`) when `0` is supported.
- Is anything created only to be deleted/ignored in some branches (dirs, temp files)? Create it only where needed.
- Can similar conditions/regexes be merged, a predicate duplicating an existing result method (`is_ok`, `is_final`) replaced by that method, or manual steps replaced by a library method (e.g. `Mojo::File->move_to`, `path()->slurp`/`spew`)?
- Do tests cover precedence between an explicit argument and a config fallback (arg wins; fallback used when arg absent)?
- Do multi-instance/multi-host settings or examples (e.g. global worker settings) support per-instance overrides or interpolation (port, hostname) rather than hardcoded values?

## Correctness

- If public API parameters, request payloads, or response schemas change, is backward compatibility preserved (optional fields, conflict disambiguation, accepting both scalar IDs and objects) to avoid synchronized deployments?
- Are regexes anchored (`/https?|ftp/` also matches `httpx`, `xftp`)?
- Could an unconditional overwrite/delete clobber valid state (e.g. re-sync/download replacing a populated target with an empty/absent source)?
- Under concurrency or repeated runs (thread pools, re-download/delete loops), can shared state race (files, caches, module-level YAML/XML parsers or clients)? Does skip-if-exists wrongly skip re-syncable dirs/repos, or does a cache key include a per-invocation ID (PR/request ID) that prevents hits?
- When output is captured, exceptions caught, HTTP/API responses discarded (`--output /dev/null`), or input dropped on parse/regex mismatch (`catch`, `return ()`, `next`, `continue`), does a log/stderr line identify the bad input (response body on non-2xx) instead of dropping silently?
- For alert-suppression, pipeline cancellation, deploy-gating or other CI-side control flow, does each acceptance criterion trace through the exact job outcomes (exit code, `allow_failure`, which later-stage jobs are prevented), and is the auth scope of every API call from a CI job checked against the instance's endpoint list (a `CI_JOB_TOKEN` is read-only for the Pipelines API — `POST /pipelines/:id/cancel` needs a project access token)?
- Are SQL subqueries, CTEs, and `count()`/aggregate queries on filtered resultsets bounded by an index (`grep` `add_index`/`CREATE INDEX` for the filter columns, check the deployed schema), and are multiple counts merged into one aggregate with `count(*) FILTER (WHERE …)` instead of separate `count()` calls (correlated `EXISTS` over unconstrained `IN`)?
- Does a setting read in a shared base class leak into subclasses targeting a different host (e.g. hypervisor `sshVirtsh` inheriting SUT `sshXtermVt`)?

## Security

- Is any path, URL, or shell argument derived from user input without preventing `..` or absolute path traversal, and are JSON payloads/parameters validated for scalar types before passing into ORM/database queries to prevent arbitrary structure/operator injection?

## External tools and dependencies

- If adding/removing/changing a dependency or external binary, is packaging updated (`dependencies.yaml`, spec `Requires`/`Recommends`) and are remaining references checked?
- In openSUSE container images, are Python deps installed via zypper RPMs (`python3-*`, e.g. `python3-PyYAML`) rather than `pip --break-system-packages` (and no stdlib in pip deps), with `#!BuildTag:` and a non-empty `_meta` title for OBS container builds?
- Are long options used for external/documented commands (`--debug`, `--mirror` instead of `-d`, `-m`)?

## Quality and Standards

- Did all local linting, static analysis (`perlcritic`, `tidy`, `eslint`, `ruff`) and the repository's own checker (e.g. `./check_links.py` in the suse/wiki docs repo), and unit/author tests pass?
- Does the commit Motivation or PR body state a guarantee the implementation, a test, or CI already provides (e.g. write-temp-then-`rename` is already atomic for readers; per-PID temp only guards concurrent writers; a regenerating script is idempotent by definition and a test checks it anyway), do variable/option names match the code, can a reader without the author's context parse every term (call a method a method, not a "predicate" or "template helper", unless that term is established in the codebase), and does the PR body follow the repo's own layout (repo `AGENTS.md`, PR template, `openqa` skill) rather than a vendored generic template, so no `Evidence`/`Merge Danger` section appears that the repo does not ask for?
- Is any new user-facing config variable documented in `doc/*.md` (e.g. `doc/backend_vars.md`)?
- Is user-requested output (dry-run previews, results) visible at default CLI verbosity (not hidden at `INFO` when default is `WARNING`)?
- Are variable/parameter/target names and UI labels/table headers accurate, non-colliding with existing project terms (`repo_type` vs `obs_repo_type`; `Roles`/`role` not `Permissions` for openQA access levels), matching underlying form control names/IDs, consistent across siblings (`label_a`/`label_b`), and protocol-specific for global settings (`SUT_SSH_PORT` not `SUT_PORT`)?
- Do build targets (`Makefile`, `CMakeLists.txt`) write only local build artifacts without touching system paths, package managers, or root privileges?

## Scope

- Is the PR small enough to review in one sitting (< ~300 changed lines), or would a design discussion be cheaper?
