---
name: redmine
description: Use when reading, annotating, or updating Redmine tickets on progress.opensuse.org (notes, status, assignee, priority).
---

# Redmine tickets (progress.opensuse.org)

## Read

`redmine-fetcher <id>` prints the ticket summary, description, and journals (read-only). It loads
`~/.query_redminerc` (`redmine-host=`, `redmine-token=`) with `REDMINE_HOST`/`REDMINE_API_TOKEN`
overrides.

## Write

Redmine REST API: `PUT https://<host>/issues/<id>.json` with header `X-Redmine-API-Key`. Send only
the fields that change:

```json
{
  "issue": {
    "notes": "text",
    "status_id": 12,
    "assignee_id": 7,
    "priority_id": 4
  }
}
```

- `notes` appends a journal entry; put the MR/PR link on its own line.
- IDs come from the ticket JSON, not its labels. Look them up in the same call:
  `GET /issues/<id>.json` (status/assignee/priority carry `id`), `GET /statuses.json?project_id=<p>`.

Run the request with `ctx_execute` (python `requests`), never `curl`/`wget`/`webfetch`; one request
per tool call, explicit `timeout`, reuse the fetcher's config loader, never print the token, and
retry once on `503 server busy` (single-slot endpoints).

Policy: show the exact note text first, write only after explicit approval, then verify with
`redmine-fetcher <id>` (journal present, status correct). Leave the ticket In Progress until the MR
is merged. On missing token, 401, or 403, hand the note text to the user for manual entry.

Scope: notes, status, assignee, priority on existing tickets. Creation, deletion, attachments, and
bulk edits are out of scope.
