---
description: Review many pull requests (an org, repositories, or a count) as the review bot, one isolated session per PR
argument-hint: "<org|owner/repo...> [--limit N] [--dry-run|--post] [--runner pi|opencode] [--model M] [--watch] [--interval N]"
---

Run the deterministic batch driver. Do not review, triage, or select PRs yourself, and do not call
`/review-as-bot` directly.

Translate `$ARGUMENTS` into driver flags — never pass fuzzy wording through as a target:
- an org or user ("os-autoinst org", "all in os-autoinst", "any 10 PRs in os-autoinst") →
  `--owner os-autoinst`
- one or more `owner/repo` names → repeat `-R owner/repo`; combine with `--owner` to review their union
- a count ("10 PRs", "up to 5") → `--limit N`
- `--dry-run` → keep it; `--post` or "no dry-run" → omit it (the driver posts by default)
- `--model <id>` → pass through to the nested review sessions
- `--runner opencode` (+ `--auto` when the run must not block on bash permission prompts) → use
  `opencode run` instead of the default `pi -p`
- `--oldest` / "backlog" / "oldest first" → `--oldest` (default is newest open PRs)
- `--recheck` → keep it only when the user wants already-reviewed heads re-examined
- `--watch` / "continuously" / "keep reviewing" → `--watch`, with `--interval N` when a different
  gap between cycles is requested (default 1200 s)

Then run `review-bot-batch <flags>` and relay its stderr summary unchanged. The driver filters
drafts, bot-authored PRs and heads the bot already reviewed, maps each repo to a local checkout,
and spawns one nested review session per PR (`pi -p "/review-as-bot <url> --post"`, or
`opencode run --command review-as-bot "<url> --post"` with `--runner opencode`). Never post reviews yourself. If the
driver exits non-zero, report its summary and failing log paths; do not retry those PRs.
