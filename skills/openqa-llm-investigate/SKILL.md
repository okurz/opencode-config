---
name: openqa-llm-investigate
description: Use when changing, evaluating or debugging `openqa-llm-investigate` prompts, verdicts, classification rules, its analysis text, or the LLM endpoints it calls.
---

# openQA LLM investigation (`os-autoinst-scripts/openqa-llm-investigate`)

## Read-only runs

- **Inspect the prompt without any LLM call**: `./openqa-llm-investigate <job> --print-prompt`.
- **Re-run without posting a comment**: `--dry --force` (`--dry` alone skips a job that already has an LLM comment and prints no footer).
- Prompt text is printed as `===== Prompt 1/3 =====`, `2/3`, `3/3`: job details + analysis, the summary question, the verdict question with the statistics.

## Endpoints

- **o3 production**: `http://REDACTED-HOST/v1/chat/completions` (gemma-4-26B-A4B-it) resolves only on the production host, so run through `ssh -o BatchMode=yes o3 '…'`. `/api/chat` on that gateway answers in OpenAI shape, so `--llm-api ollama` fails with `KeyError: 'message'`.
- **SUSE ollama**: `http://REDACTED-HOST:80/v1` with `--llm-model default:latest` (Qwen3.8-27B) or `gemma4:latest`. Single-slot: concurrent requests get `503 server busy, please try again`; one evaluation per tool call, 1.5–2 min each.

## Evaluating a prompt change

1. Run the target job on the **production small model**, not only on a large model. gemma ignored added classification rules for a worker-killed job (`Reason: quit: worker has been stopped or restarted`) and answered `Product bug` while Qwen answered `Test issue`.
2. Add a **control job of the opposite class**: a rule that fixed the target class regressed a genuine infrastructure job. Reference jobs: 6287643 (test-code issue, expected `Test issue` / `BISECT: NO` / `Restart: NO`), 6287595 (worker killed, expected `Infrastructure problem` / `Restart: YES`), 6287693 (needle, accepted as ambiguous).
3. Small models ignore prompt rules: enforce verdicts in code (precedent `_enforce_bisect_rule`) and keep example reasons as `<short reason>` placeholders, since concrete example text gets copied verbatim.
4. Decisive evidence goes in the **head** of the analysis, rules in the **last** message: the gateway sends no `num_ctx`, so gemma truncates the tail of prompt 1 at 4096 tokens.

## Code anchors & data gaps

- `OUTAGE_HINT` fires on every daily Tumbleweed build: `_build_failures` counts failed jobs across all groups (70 for Build 20261021), threshold `--build-failure-threshold` defaults to 20.
- `_consecutive_failures` uses `--history-limit`; the streak note is appended to the comment when the job is not in the recent history.
- `uploads._UPLOAD_TEXT_RE` excludes `.tap`, so `select_uploaded_logs` never feeds the TAP assertion diff (`not ok N`, `Structures begin differing`, `# sqlite3 version: 3.54.1`) that decides a TAP module failure; the 4-file cap cuts it as list position 11. `_SKIP_UPLOAD_RE` drops `zypper.log`, `rpm-qa` and `rpm-list`, so package versions appear only inside command output.
- `investigation_ajax` `diff_to_last_good` is inserted uncapped into prompt 1 and carries the `TEST_GIT_HASH`/`CASEDIR` test-code change signal.
- No known-issues label, RPM changelog, git log, or test-suite source lookup exists in the tool; the `BISECT: YES` stdout line is the gate that triggers `openqa-investigate`, `Restart` is human-facing only.
