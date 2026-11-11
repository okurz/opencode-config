# Review checklist

Distilled from real reviewer feedback (see `review-learnings.md`). Read by
`/pre-push-review-*` and `/address-review`. Keep each item one line, phrased
as a question. Merge or remove items instead of growing the list.

## Reuse and consistency

- Does the codebase already solve this (helper, query pattern like `WITH RECURSIVE`, module)? `grep` before accepting new code. (openQA#7871)
- Is new prose/docs formatted like surrounding text (line wrapping, heading style)? (openQA#7849)

## Simplicity

- Which fallbacks, `//` chains or type checks can never trigger given existing invariants? Remove them. (openQA#7872, openQA#7849)
- Is anything created only to be deleted/ignored in some branches (dirs, temp files)? Create it where it is needed. (openQA#7849)
- Can multiple similar conditions/regexes be merged into one? Is there a library method (e.g. `Mojo::File->move_to`) for the manual steps? (openQA#7849)

## Correctness

- Are regexes anchored? `/https?|ftp/` also matches `httpx`, `xftp`. (openQA#7849)
- Is anything overwritten/deleted unconditionally that might be valid existing state? (openQA#7849)
- What happens when the same operation runs twice concurrently or repeatedly (re-download, re-delete loops)? (openQA#7849)

## Security

- Is any path, URL or shell argument derived from user input? Is `..`/absolute path traversal prevented? (openQA#7849)

## External tools and dependencies

- Does the change invoke a new external program? Is it declared in packaging (e.g. `dependencies.yaml`, spec `Requires`/`Recommends`)? (openQA#7849)
- Are long options used for external commands (`--mirror`, not `-m`)? (openQA#7849)

## Scope

- Is the PR small enough to review in one sitting (< ~300 changed lines)? Would a design discussion have been cheaper than the code? (openQA#7849)
