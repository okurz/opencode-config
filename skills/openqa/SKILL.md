---
name: openqa
description: Use when fetching and analyzing openQA job logs (autoinst-log.txt) or diagnosing openQA test failures.
---

# openQA Log Analysis

- **Raw Log URL**: Convert frontend URLs (`.../tests/<id>/logfile?filename=autoinst-log.txt`) to raw file URLs: `https://openqa.opensuse.org/tests/<id>/file/autoinst-log.txt`.
- **Fetch & Filter (context-mode safe)**: Do not use `webfetch` or bare `curl` in `bash`. Fetch and filter in sandbox via `ctx_execute` (e.g. save to `/tmp/opencode/autoinst-log.txt` with `curl -sL` inside `ctx_execute(language: "shell")` or `ctx_execute_file`), printing only matching sections.
- **Root Cause Analysis**: Search for `[error]`, `[fatal]`, `fail`, `die`, or `timed out`, inspect surrounding lines, and trace back to the failing test module, command, or earlier setup warnings.
