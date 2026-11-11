---
description: Analyze an openQA log file for errors and determine the root cause of a test failure.
---

Analyze the openQA log file for the given test ID or URL: $ARGUMENTS

**STRICT INSTRUCTIONS:**
1. Proactively load the `openqa` skill using the `skill` tool (e.g. `[tool_call: skill for 'openqa']`).
2. Do not use the `webfetch` tool as it typically retrieves the HTML frontend. Instead, identify the raw log file URL (`autoinst-log.txt`) and download it locally (e.g. to `/tmp/`) using `bash` and `curl`.
3. Once downloaded, utilize the custom `grep` and `read` tools to efficiently search the local file for keywords (`[error]`, `[fatal]`, `fail`, `die`, `timed out`) and review the surrounding context.
4. Conclude with a clear explanation of the root cause based on the log evidence.