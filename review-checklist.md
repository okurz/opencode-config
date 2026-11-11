# Review checklist

Distilled from real reviewer feedback (see `review-learnings.md`). Read by
`/pre-push-review-*` and `/address-review`. Keep each item one line, phrased
as a question. Merge or remove items instead of growing the list.

## Reuse and consistency

- Does the codebase already solve this (helper, query pattern like `WITH RECURSIVE`, module)? `grep` before accepting new code. (openQA#7871)
- Are repetitive command flags, options, or expressions consolidated into a property or helper rather than duplicated across call sites? (openQA#7857, os-autoinst-scripts#753)
- Is new prose, documentation, and UI text formatted like surrounding content (line wrapping; sentence case for headings, cards, badges, labels, tooltips and buttons, e.g. 'Host summary', 'Warning' not 'WARNING')? (openQA#7849, openQA#7857, openQA#7877)

## Simplicity

- For each `eval`, `//`, `defined`, `ref` check, array-form branch or guard `return`: grep all callers and config defaults (e.g. `Setup.pm`). Does the production environment guarantee the value? Fix incomplete test setups instead of adding defensive fallbacks to production code. (openQA#7872, openQA#7849, openQA#7877, openQA#7935)
- Is anything created only to be deleted/ignored in some branches (dirs, temp files)? Create it where it is needed. (openQA#7849)
- Can multiple similar conditions/regexes be merged into one? Is there a library method (e.g. `Mojo::File->move_to`, `path()->slurp`/`spew`) for the manual steps? (openQA#7849, os-autoinst#3118)
- Do tests cover precedence between an explicit argument and a config fallback (arg wins; fallback used when arg absent)? (os-autoinst#3124)
- When adding configuration settings or examples that apply across multiple instances or hosts (e.g. global worker settings), can values vary per instance (e.g. port, hostname), and does the design support interpolation or per-instance overrides rather than hardcoded values? (salt-states-openqa#MR1804, os-autoinst#3118, openQA#7940)

## Correctness

- Does the change modify public API parameters, request payloads, or response schemas? If yes, ensure backward compatibility is maintained (e.g. optional fields with disambiguation on conflict, accepting both scalar IDs and objects) to avoid forcing synchronized deployments. (qem-dashboard#3423)
- Are regexes anchored? `/https?|ftp/` also matches `httpx`, `xftp`. (openQA#7849)
- Is anything overwritten/deleted unconditionally that might be valid existing state (e.g. a re-sync/download replacing a populated target with an empty or absent source)? (openQA#7849)
- When work runs concurrently or repeatedly (thread pools, re-download/re-delete loops), can it race on shared state: file/cache targets or module-level in-memory objects such as YAML/XML parsers and clients? Does a skip-if-exists guard wrongly apply to asset types where re-syncing is the point (directories/repos)? Does a cache key contain a value unique per invocation (PR number, request ID) so the cache never hits — verify the key has reuse before adding a cache? (openQA#7849, qem-bot#704)
- When output is captured, an exception is caught, or input is dropped on a parse/regex/format mismatch (`catch`, `return ()`, `next`, `continue`), does a log/stderr line name the bad input? Silent drops are a recurring pattern. (backlogger#73, os-autoinst-scripts#756, openQA#7877)
- Are SQL subqueries and CTEs properly constrained to prevent full-table scans (e.g. using correlated `EXISTS` instead of unconstrained `IN`)? (openQA#7871)
- Does a setting read in a shared base class leak into subclasses that target a different host (e.g. hypervisor `sshVirtsh` inheriting SUT `sshXtermVt`)? (os-autoinst#3124)

## Security

- Is any path, URL or shell argument derived from user input? Is `..`/absolute path traversal prevented? (openQA#7849)

## External tools and dependencies

- Does the change add, remove, or modify a dependency or external program? If adding, is it declared in packaging (e.g. `dependencies.yaml`, spec `Requires`/`Recommends`)? If removing/downgrading, did you check that no other files still require it? (openQA#7849, os-autoinst-scripts#723)
- On an openSUSE container image, are Python deps installed via zypper RPMs (`python3-*`, capitalized like `python3-PyYAML`/`python3-Markdown`) rather than `pip --break-system-packages`? Are stdlib modules wrongly listed as pip deps? Does the Dockerfile carry `#!BuildTag:` and a non-empty `_meta` title so OBS builds a container, not an RPM? (backlogger#73)
- Are long options used for external/documented commands (e.g. `--debug` and `--mirror` instead of `-d` or `-m`)? (openQA#7849)

## Quality and Standards

- Have all local linting, static analysis (e.g. perlcritic, tidy, eslint), and author/unit tests been run and verified to pass? (os-autoinst#3113)
- Does the commit-message Motivation state necessity the code actually has, or overstate it? Verify the original code already provides the claimed guarantee (e.g. write-temp-then-`rename` is already atomic for readers; a per-PID temp only guards concurrent writers). (qem-bot#704, openQA#7907, os-autoinst#3120)
- Do commit-message variable, option, and setting names match what the code actually reads (not a renamed/abandoned name)? (os-autoinst#3124)
- Is a new user-facing config variable documented in `doc/*.md` (e.g. `doc/backend_vars.md`)? (os-autoinst#3124)
- Is output the user asked for (dry-run previews, results) visible at the tool's default verbosity? INFO is hidden by default in most CLIs (WARNING), so print to stdout or state the consequence instead of demoting to debug. (backlogger#73, qem-bot#709, os-autoinst-scripts#756)
- Do parameter, variable, and state/target names describe what they actually hold/do, avoid reusing an existing project term with a different meaning (`repo_type` vs `obs_repo_type`), match sibling items in the same change (`label_a`/`label_b`), and name new global setting vars by the transport/protocol they configure (`SUT_SSH_PORT` not `SUT_PORT`)? (os-autoinst-scripts#730, openQA#7857, qem-bot#710, salt-states-openqa#MR1819, os-autoinst#3124)
- Do build targets (e.g. in `Makefile`, `CMakeLists.txt`) only generate local build artifacts without modifying global system directories, running package managers, or requiring root privileges? (os-autoinst#3118)

## Scope

- Is the PR small enough to review in one sitting (< ~300 changed lines)? Would a design discussion have been cheaper than the code? (openQA#7849)
