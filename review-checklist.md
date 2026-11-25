# Review checklist

Distilled from `review-learnings.md`. Read by `/pre-push-review` and `/address-review`. Keep each item one line, phrased as a question; merge or prune instead of growing.

## Reuse and consistency

- Does the codebase already solve this (helper, query pattern like `WITH RECURSIVE`, module)? `grep` before accepting new code, and `grep` every new method/parameter outside `t/` — a helper only tests call is dead code, even when a follow-up PR is meant to use it.
- Are repetitive expressions, method calls (including repeated `$validation->is_valid()`/`->param()` accessor calls), or hash lookups (including repeated `$app->config->{section}->{key}` in tests, where the section hash ref is bound once and its keys `local`-ized) cached in a local variable, repeated command flags/options consolidated into a property or helper, repeated URLs/values across CI steps factored into workflow/job `env`, and time/size/count literals (`86400`, `3600`) or domain strings written as named constants (`Time::Seconds` `ONE_DAY`, `OpenQA::Jobs::Constants`) in lib and tests?
- Is new prose, documentation, and UI text formatted like surrounding content (line wrapping; sentence case for headings, cards, badges, labels, tooltips, buttons and dropdown options, including every word inside parentheses, e.g. 'Host summary', 'Dark mode (Halloween season)' not 'Dark mode (Halloween Season)', 'Warning' not 'WARNING')?

## Simplicity

- For each `eval`, `//`, `defined`, `ref` check, type coercion (`int`, `0 +`), guard `return`, predicate inlined/copied from another context (e.g. a UI display condition reused in a data-selection loop), or test environment override: `grep` callers, config defaults (e.g. `Setup.pm`, module constants), ORM schema column inflation/defaults (e.g. integer primary keys like `->id`), and upstream query `WHERE` filters (e.g. `_previous_scenario_jobs` restricts to `state=done` + `COMPLETE_RESULTS`)—if a clause is already guaranteed, drop it; when data is missing in a consumer, fix the upstream producer/loader (schemas, key names like `scminfo` vs `scm_info`) instead of adding a defensive fallback or dynamic fetch; and avoid arbitrary non-zero delays (`0.01`) when `0` is supported.
- Is anything created only to be deleted/ignored in some branches (dirs, temp files)? Create it only where needed.
- Can similar conditions/regexes be merged, a predicate duplicating an existing result method (`is_ok`, `is_final`) replaced by that method, or manual steps replaced by a library method (e.g. `Mojo::File->move_to`, `path()->slurp`/`spew`)?
- Do tests cover precedence between an explicit argument and a config fallback (arg wins; fallback used when arg absent)?
- Does a non-obvious parser, format or normalization helper show a worked input→output example in the README or its docstring, so a reader does not have to reconstruct the rule from the code?
- Do multi-instance/multi-host settings or examples (e.g. global worker settings) support per-instance overrides or interpolation (port, hostname) rather than hardcoded values?
- Do shared plugin and domain helpers accept plain scalar values or models rather than controller validation objects (`$validation`, `$req`), keeping HTTP request validation at the controller boundary?

## Correctness

- If public API parameters, request payloads, or response schemas change, is backward compatibility preserved (optional fields, conflict disambiguation, accepting both scalar IDs and objects) to avoid synchronized deployments?
- Are regexes anchored (`/https?|ftp/` also matches `httpx`, `xftp`)?
- Could an unconditional overwrite/delete clobber valid state (e.g. re-sync/download replacing a populated target with an empty/absent source)?
- Under concurrency or repeated runs (thread pools, re-download/delete loops), can shared state race (files, caches, module-level YAML/XML parsers or clients)? Does skip-if-exists wrongly skip re-syncable dirs/repos, or does a cache key include a per-invocation ID (PR/request ID) that prevents hits?
- When output is captured, exceptions caught, HTTP/API responses discarded (`--output /dev/null`), or input dropped on parse/regex mismatch (`catch`, `return ()`, `next`, `continue`), does a log/stderr line identify the bad input (response body on non-2xx) instead of dropping silently?
- For alert-suppression, pipeline cancellation, deploy-gating or other CI-side control flow, does each acceptance criterion trace through the exact job outcomes (exit code, `allow_failure`, which later-stage jobs are prevented), and is the auth scope of every API call from a CI job checked against the instance's endpoint list (a `CI_JOB_TOKEN` is read-only for the Pipelines API — `POST /pipelines/:id/cancel` needs a project access token)?
- Are SQL subqueries, CTEs, and `count()`/`max()`/`GROUP BY` aggregate queries on filtered resultsets (including ones behind public endpoints that load all rows of a table and build `IN` lists in Perl) bounded by an index (`grep` `add_index`/`CREATE INDEX` for the filter columns, check the deployed schema), and are multiple counts merged into one aggregate with `count(*) FILTER (WHERE …)` instead of separate `count()` calls (correlated `EXISTS` over unconstrained `IN`)?
- Does a setting read in a shared base class leak into subclasses targeting a different host (e.g. hypervisor `sshVirtsh` inheriting SUT `sshXtermVt`)?
- Does a guard on externally sourced data (file, JSON, API response) validate each field the consumer dereferences, not only the top-level container, and does a test feed every malformed shape (wrong container type, wrong field type, `null`), so reverting the guard fails?

## Security

- Is any path, URL, or shell argument derived from user input without preventing `..` or absolute path traversal, and are JSON payloads/parameters validated for scalar types before passing into ORM/database queries to prevent arbitrary structure/operator injection?
- When effective permissions are scoped by a credential (API key/token), is that scope authoritative for the current request, with no explicit-argument or alternate code path bypassing it?

## External tools and dependencies

- If adding/removing/changing a dependency, external binary or a direct `import`, is every manifest updated (Python: `pyproject.toml` `dependencies`/optional-dependencies — never rely on a transitive pin; packaging: `dependencies.yaml`, spec `Requires`/`Recommends`) and are remaining references checked?
- In openSUSE container images, are Python deps installed via zypper RPMs (`python3-*`, e.g. `python3-PyYAML`) rather than `pip --break-system-packages` (and no stdlib in pip deps), with `#!BuildTag:` and a non-empty `_meta` title for OBS container builds?
- Are long options used for external/documented commands (`--debug`, `--mirror` instead of `-d`, `-m`)?
- Does a `Makefile`/CI test target's optional argument exist and come from the same interpreter/virtualenv the command runs in (grep the variable, e.g. an undefined `$(PYTEST_ARGS)`; probe plugins with `$(PYTHON_RUN)`/`uv run`, not a bare `python3`), and is a conditional flag (`pytest -n auto`) dropped when the suite finishes in hundredths of a second?

## Quality and Standards

- Does `git log --oneline origin/master..HEAD` show one change class per commit (fix, feat, refactor, build, docs), each independently green, so the fix can be read apart from the feature it ships with?
- Does each new endpoint, parameter, or filter test assert the returned data (ids, values, rejected inputs with 400/403, combinations with existing filters) instead of only the HTTP status, so that reverting the code fails the test?
- Do new tests drive the real code path (route, template, SQL statement/conflict case) instead of mocking the method under test or hand-copying its logic, is the `Test::MockModule`/mock import dropped when it is no longer needed, do new test-suite subs use signatures like production code, do constant `Test::MockModule` stubs pass the plain value (`redefine(foo => 0)`) instead of a closure, and do test description strings claim only what the assertion would catch on revert (no "instead of X" when the test cannot reproduce X), and do set/filter predicates cover the boundary outcomes (empty result, all kept, some dropped) with an explicit fail-open or fail-closed choice?
- Did all local linting, static analysis (`perlcritic`, `tidy`, `eslint`, `ruff`), the repository's own checker (e.g. `./check_links.py` in the suse/wiki docs repo, `gitlint --commits origin/master..HEAD` for the commit message title regex), and did it run the repo's own target (`make checkstyle`/`make check-ruff`) rather than a bare `ruff check .`, which skips extensionless scripts that the target lints by explicit file list, and unit/author tests pass?
- Does the PR body say how the change was verified beyond unit tests, with exact commands and links to live runs/PRs/jobs, instead of only claiming it works, and does it still describe the commits on the branch after a history rewrite (no dropped commits, no behaviour the diff narrows silently, e.g. a prune that now deletes only `*.dump` instead of any file)?
- Does the commit Motivation or PR body state a guarantee the implementation, a test, or CI already provides (e.g. write-temp-then-`rename` is already atomic for readers; per-PID temp only guards concurrent writers; a regenerating script is idempotent by definition and a test checks it anyway), is every performance claim (also in a review reply) grounded in a named, production-scale input and measurement (`EXPLAIN ANALYZE` on o3, 1.14M jobs, 725 workers; the 702 KiB `default.productcompose`, not the 112-byte test fixture) instead of an unverifiable one ("3M synthetic jobs ... about 0.5 s"), do variable/option names match the code, can a reader without the author's context parse every term (call a method a method, not a "predicate" or "template helper", unless that term is established in the codebase), and does the PR body follow the repo's own layout (repo `AGENTS.md`, PR template, `openqa` skill) rather than a vendored generic template, so no `Evidence`/`Merge Danger` section appears that the repo does not ask for?
- Is any new user-facing config variable documented in `doc/*.md` (e.g. `doc/backend_vars.md`)?
- Is interface documentation for a helper/sub written as POD (`=head2`) rather than a leading `#` comment?
- Is user-requested output (dry-run previews, results) visible at default CLI verbosity (not hidden at `INFO` when default is `WARNING`)?
- Are variable/parameter/target names and UI labels/table headers accurate, non-colliding with existing project terms (`repo_type` vs `obs_repo_type`; `Roles`/`role` not `Permissions` for openQA access levels), matching underlying form control names/IDs, consistent across siblings (`label_a`/`label_b`), and protocol-specific for global settings (`SUT_SSH_PORT` not `SUT_PORT`)?
- Do build targets (`Makefile`, `CMakeLists.txt`) write only local build artifacts without touching system paths, package managers, or root privileges?

## openQA: CI gates and packaging

- Is a failing `OBS: openQA - openSUSE_Tumbleweed/x86_64` or another stale-base build context only behind master, so a rebase clears it, rather than a real failure of the change?
- Does the PR reach the mergify floor: 2 approvals, `#check-success>=39`, `#check-pending=0`, linear history, no `acceptance-tests-needed`/`not-ready`/`merge-skip-*` label?
- Did changed Perl lines run `COVERAGE=1 make test-unit-and-integration TESTS=<file>` plus `make check-line-coverage`, and did `make tidy` and `make test-checkstyle` pass on a clean tree?
- Was every test run started through the repo's own target (`make test-unit-and-integration TESTS=<file>`) instead of bare `prove -l`, so a harness failure is not misreported as "cannot be executed locally"?
- Is a new Python test file executed by a Makefile target or CI job (this repo only runs `ruff`), or would its assertions never run?
- Do packaging conditionals agree: units in `%files`, the script behind `%if %{with python_scripts}`, and a matching `%exclude` or `%if`, so rpmbuild does not stop on unpackaged files?
- Does `git log --format=%B origin/master..HEAD` show a `Related issue: https://progress.opensuse.org/issues/<id>` line in every feature/fix commit (not only the PR body), was the ticket created before the first commit and does its subject describe this change (open it and read the subject), and does the PR body avoid claims the diff and CI already show?

## Salt states

- Does a `require`/`order` duplicate the ordering Salt already gives states in one sls file (`state_auto_order` runs them top to bottom), and is every cross-file dependency (e.g. a user state in another sls, a package) declared explicitly with `require`?
- Does a `cmd.run` precondition (`onlyif`, `unless`) hold on a fresh host's first highstate, and does a state that must reconcile (directory, ownership, mode) use an idempotent state (`file.directory`) instead of a one-shot command triggered by `onchanges` on another file?
- Does a remount, reload, or other command that fails when its target is absent carry a guard (`onlyif: mountpoint -q …`)?

## Scope

- Is the PR small enough to review in one sitting (< ~300 changed lines), or would a design discussion be cheaper?
- When adding integration or end-to-end checks to CI, start with a single, fast scenario (e.g. testing directly from git source) rather than waiting on external packaging builds (like OBS) or scheduling full matrices?
