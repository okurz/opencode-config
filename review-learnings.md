# Review learnings log

One line per reviewer comment. Written by `/address-review`, aggregated by
`/review-retro`. A lesson is promoted to a durable prevention once its class
occurs at least twice, or immediately if security-related.

Categories: `lintable` | `repo-rule` | `global-rule` | `checklist` | `design` | `one-off`
Status: `logged` | `promoted:<target>` | `rejected` (reviewer comment not accepted)

| Date       | Ref                     | Reviewer | Category  | Lesson                                                                                         | Status                       |
| ---------- | ----------------------- | -------- | --------- | ---------------------------------------------------------------------------------------------- | ---------------------------- |
| 2026-09-25 | openQA#7872 r4104549734 | Martchus | checklist | Defensive fallback for a value the code already guarantees (`exit_code` always set on failure) | promoted:review-checklist.md |
| 2026-09-25 | openQA#7871 r4104597624 | Martchus | repo-rule | Hand-built dynamic multi-join SQL where the codebase uses `WITH RECURSIVE` for similar queries | promoted:review-checklist.md |
| 2026-09-25 | openQA#7849             | Martchus | lintable  | New external tool (`wget`) not declared as dependency                                          | promoted:review-checklist.md |
| 2026-09-25 | openQA#7849             | Martchus | design    | Concurrent/repeated downloads of the same repo not considered                                  | promoted:review-checklist.md |
| 2026-09-18 | openQA#7849             | Martchus | lintable  | Markdown not wrapped consistently with surrounding text                                        | logged                       |
| 2026-09-18 | openQA#7849             | Martchus | checklist | Too many fallbacks in `$is_repo` detection                                                     | promoted:review-checklist.md |
| 2026-09-25 | openQA#7849             | Martchus | one-off   | Manual move instead of `Mojo::File->move_to`                                                   | promoted:review-checklist.md |
| 2026-09-25 | openQA#7849             | Martchus | checklist | Path derived from `$target` not checked for `..` traversal                                     | promoted:review-checklist.md |
| 2026-09-25 | openQA#7849             | Martchus | repo-rule | Cryptic short option instead of `--mirror`                                                     | promoted:review-checklist.md |
| 2026-09-25 | openQA#7849             | Martchus | checklist | Several conditions could be one regex                                                          | promoted:review-checklist.md |
| 2026-09-25 | openQA#7849             | Martchus | checklist | Target overridden unconditionally                                                              | promoted:review-checklist.md |
| 2026-09-27 | openQA#7849             | perlpunk | checklist | Unanchored scheme regex matches `httpx`/`xftp`                                                 | promoted:review-checklist.md |
| 2026-09-27 | openQA#7849             | perlpunk | checklist | Directory created early, deleted later in unrelated branches                                   | promoted:review-checklist.md |
