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
- Can multiple similar conditions/regexes be merged into one? Is there a library method (e.g. `Mojo::File->move_to`) for the manual steps? (openQA#7849)

## Correctness

- Does the change modify public API parameters, request payloads, or response schemas? If yes, ensure backward compatibility is maintained (e.g. optional fields with disambiguation on conflict, accepting both scalar IDs and objects) to avoid forcing synchronized deployments. (qem-dashboard#3423)
- Are regexes anchored? `/https?|ftp/` also matches `httpx`, `xftp`. (openQA#7849)
- Is anything overwritten/deleted unconditionally that might be valid existing state? (openQA#7849)
- When work runs concurrently or repeatedly (thread pools, re-download/re-delete loops), can it race on shared state: file/cache targets or module-level in-memory objects such as YAML/XML parsers and clients? (openQA#7849, qem-bot#704)
- Are SQL subqueries and CTEs properly constrained to prevent full-table scans (e.g. using correlated `EXISTS` instead of unconstrained `IN`)? (openQA#7871)

## Security

- Is any path, URL or shell argument derived from user input? Is `..`/absolute path traversal prevented? (openQA#7849)

## External tools and dependencies

- Does the change add, remove, or modify a dependency or external program? If adding, is it declared in packaging (e.g. `dependencies.yaml`, spec `Requires`/`Recommends`)? If removing/downgrading, did you check that no other files still require it? (openQA#7849, os-autoinst-scripts#723)
- Are long options used for external/documented commands (e.g. `--debug` and `--mirror` instead of `-d` or `-m`)? (openQA#7849)

## Quality and Standards

- Have all local linting, static analysis (e.g. perlcritic, tidy, eslint), and author/unit tests been run and verified to pass? (os-autoinst#3113)

## Scope

- Is the PR small enough to review in one sitting (< ~300 changed lines)? Would a design discussion have been cheaper than the code? (openQA#7849)
