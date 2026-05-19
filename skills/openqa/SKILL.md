---
name: openqa
description: Specialized instructions for fetching and analyzing openQA logs.
---

# openQA Log Analysis Guidelines

## Retrieving Logs
- The `webfetch` tool usually retrieves the HTML frontend of an openQA test result, which is not useful for deep log analysis.
- To retrieve the raw log file (`autoinst-log.txt`), construct the raw file URL. If given `https://openqa.opensuse.org/tests/<id>/logfile?filename=autoinst-log.txt`, the raw text URL is `https://openqa.opensuse.org/tests/<id>/file/autoinst-log.txt`.
- Download the raw log file locally to a temporary location using `bash` and `curl`. Example: `curl -sL "https://openqa.opensuse.org/tests/<id>/file/autoinst-log.txt" -o /tmp/autoinst-log.txt`.
- Avoid streaming large log files directly through `grep` inside `bash` if you need to perform multiple searches or context reviews. Downloading it locally allows the use of the fast, specific `grep` and `read` tools.

## Analyzing Logs
- Once downloaded, use the `grep` tool to search the local file for keywords like `[error]`, `[fatal]`, `fail`, `die`, or `timed out`.
- Use the `read` tool to examine the surrounding context of any errors found by `grep`.
- Identify the root cause by tracing the failure back to the specific test module, command, or system state that failed.
- Check for earlier warnings or setup failures that might have caused the fatal error downstream.