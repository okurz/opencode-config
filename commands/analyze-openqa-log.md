---
description: Analyze an openQA log file for errors and determine the root cause of a test failure.
---

Analyze the openQA log for test ID or URL: $ARGUMENTS

1. Load and follow the `openqa-log-analysis` skill (`skill` tool).
2. Fetch and filter the raw `autoinst-log.txt` using `context-mode` sandbox tools (never `webfetch` or bare `curl` in `bash`).
3. Report the root cause with supporting log lines and any preceding setup warnings.
