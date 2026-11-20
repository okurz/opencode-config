---
description: Review many pull requests (an org, repositories, or a count) as the review bot, one isolated session per PR
argument-hint: "<org|owner/repo...> [--limit N] [--dry-run|--post] [--model M]"
---

Run the deterministic batch driver. Do not review, triage, or select PRs yourself, and do not call
`/review-as-bot` directly.

Translate `$ARGUMENTS` into driver flags — never pass fuzzy wording through as a target:
- an org or user ("os-autoinst org", "all in os-autoinst", "any 10 PRs in os-autoinst") →
  `--owner os-autoinst`
- one or more `owner/repo` names → repeat `-R owner/repo`
- a count ("10 PRs", "up to 5") → `--limit N`
- `--dry-run` → keep it; `--post` or "no dry-run" → omit it (the driver posts by default)
- `--model <id>` → pass through to the nested review sessions
- `--oldest` / "backlog" / "oldest first" → `--oldest` (default is newest open PRs)
- `--recheck` → keep it only when the user wants already-reviewed heads re-examined

Then run `review-bot-batch <flags>` and relay its stderr summary unchanged. The driver filters
drafts, bot-authored PRs and heads the bot already reviewed, maps each repo to a local checkout,
and spawns one `pi -p "/review-as-bot <url> --post"` per PR. Never post reviews yourself. If the
driver exits non-zero, report its summary and failing log paths; do not retry those PRs.
