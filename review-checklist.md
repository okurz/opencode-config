# Review checklist

Distilled from real reviewer feedback (see `review-learnings.md`). Read by
`/pre-push-review-*` and `/address-review`. Keep each item one line, phrased
as a question. Merge or remove items instead of growing the list.

## Reuse and consistency

- Does the codebase already solve this (helper, query pattern like `WITH RECURSIVE`, module)? `grep` before accepting new code. (openQA#7871)
- Is new prose, documentation, and UI text formatted like surrounding content (e.g. line wrapping, sentence-case headings and card titles like 'Host summary', 'Worker host administration')? (openQA#7849, openQA#7857)

## Simplicity

- Which fallbacks, `//` chains or type checks can never trigger given existing invariants? Remove them. (openQA#7872, openQA#7849)
- Is anything created only to be deleted/ignored in some branches (dirs, temp files)? Create it where it is needed. (openQA#7849)
- Can multiple similar conditions/regexes be merged into one? Is there a library method (e.g. `Mojo::File->move_to`, `path()->slurp`/`spew`) for the manual steps? (openQA#7849, os-autoinst#3118)

## Correctness

- Does the change modify public API parameters, request payloads, or response schemas? If yes, ensure backward compatibility is maintained (e.g. optional fields with disambiguation on conflict, accepting both scalar IDs and objects) to avoid forcing synchronized deployments. (qem-dashboard#3423)
- Are regexes anchored? `/https?|ftp/` also matches `httpx`, `xftp`. (openQA#7849)
- Is anything overwritten/deleted unconditionally that might be valid existing state (e.g. a re-sync/download replacing a populated target with an empty or absent source)? (openQA#7849)
- When work runs concurrently or repeatedly (thread pools, re-download/re-delete loops), can it race on shared state: file/cache targets or module-level in-memory objects such as YAML/XML parsers and clients? Does a skip-if-exists guard wrongly apply to asset types where re-syncing is the point (directories/repos)? (openQA#7849, qem-bot#704)
- When output is captured (`capture_output`, `PIPE`) or an exception is caught, does the failure path still show stderr or the error text to the user? Silent swallowing is a recurring pattern. (backlogger#73, os-autoinst-scripts#756)
- Are SQL subqueries and CTEs properly constrained to prevent full-table scans (e.g. using correlated `EXISTS` instead of unconstrained `IN`)? (openQA#7871)

## Security

- Is any path, URL or shell argument derived from user input? Is `..`/absolute path traversal prevented? (openQA#7849)

## External tools and dependencies

- Does the change add, remove, or modify a dependency or external program? If adding, is it declared in packaging (e.g. `dependencies.yaml`, spec `Requires`/`Recommends`)? If removing/downgrading, did you check that no other files still require it? (openQA#7849, os-autoinst-scripts#723)
- On an openSUSE container image, are Python deps installed via zypper RPMs (`python3-*`, capitalized like `python3-PyYAML`/`python3-Markdown`) rather than `pip --break-system-packages`? Are stdlib modules wrongly listed as pip deps? Does the Dockerfile carry `#!BuildTag:` and a non-empty `_meta` title so OBS builds a container, not an RPM? (backlogger#73)
- Are long options used for external/documented commands (e.g. `--debug` and `--mirror` instead of `-d` or `-m`)? (openQA#7849)

## Quality and Standards

- Have all local linting, static analysis (e.g. perlcritic, tidy, eslint), and author/unit tests been run and verified to pass? (os-autoinst#3113)
- Does the commit-message Motivation state necessity the code actually has, or overstate it? Verify the original code already provides the claimed guarantee (e.g. write-temp-then-`rename` is already atomic for readers; a per-PID temp only guards concurrent writers). (qem-bot#704, openQA#7907, os-autoinst#3120)
- Is output the user asked for (dry-run previews, results) visible at the tool's default verbosity? INFO is hidden by default in most CLIs (WARNING), so print to stdout or state the consequence instead of demoting to debug. (backlogger#73, qem-bot#709, os-autoinst-scripts#756)
- Do parameter, variable, and state/target names describe what they actually hold/do, avoid reusing an existing project term with a different meaning (`repo_type` vs `obs_repo_type`), and match sibling items in the same change (`label_a`/`label_b`)? (os-autoinst-scripts#730, openQA#7857, qem-bot#710, salt-states-openqa#MR1819)
- Do build targets (e.g. in `Makefile`, `CMakeLists.txt`) only generate local build artifacts without modifying global system directories, running package managers, or requiring root privileges? (os-autoinst#3118)

## Scope

- Is the PR small enough to review in one sitting (< ~300 changed lines)? Would a design discussion have been cheaper than the code? (openQA#7849)
