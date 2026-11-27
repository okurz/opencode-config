---
name: redmine
description: Use when reading, creating, or updating Redmine tickets on progress.opensuse.org (notes, status, assignee, priority, new tickets).
---

# Redmine tickets (progress.opensuse.org)

## Read

`redmine-fetcher <id>` prints the ticket summary, description, and journals (read-only). It loads
`~/.query_redminerc` (`redmine-host=`, `redmine-token=`) with `REDMINE_HOST`/`REDMINE_API_TOKEN`
overrides.

## Create

`POST https://<host>/issues.json` with the same header and body `{"issue": {...}}`:

```json
{
  "issue": {
    "project_id": 125,
    "tracker_id": 4,
    "subject": "[infra] …",
    "description": "## Observation\n…",
    "category_id": 817,
    "priority_id": 4
  }
}
```

- IDs: `GET /projects/<id>.json?include=trackers` lists tracker ids; `GET /projects.json?limit=100`
  finds a project. `openQA Infrastructure (public)` is project 125, tracker `action` is 4.
- The ticket type is a `category_id`, never a keyword in the subject: a feature ticket gets
  the project's `Feature requests` category, not ` (feature)` appended to the subject. Ids
  are per project — `GET /projects/<id>.json?include=issue_categories` — as Feature requests
  / Organisational / Regressions-Crashes / Support: 125 → 811/814/817/820, 18 →
  142/208/134/188.
- House style there: subject `[infra] <what> <where>` (add `[alert]` for alert tickets), description
  sections `## Observation`, then `## Acceptance criteria` with `* **AC1:** …`, then `## Suggestions`
  last, with `#<id>` references inline. One ticket per root cause.
- Verify with `redmine-fetcher <new id>` and report the URL.

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
  `GET /issues/<id>.json` (status/assignee/priority carry `id`), `GET /issue_statuses.json`
(`/statuses.json` is 404 on progress.opensuse.org).

Run the request with `ctx_execute` (python `requests`), never `curl`/`wget`/`webfetch`; one request
per tool call, explicit `timeout`, reuse the fetcher's config loader, never print the token, and
retry once on `503 server busy` (single-slot endpoints).

Policy: show the exact note text, or subject and description for a new ticket, first; write only
after explicit approval, then verify with `redmine-fetcher <id>`. Leave the ticket In Progress until the MR
is merged. On missing token, 401, or 403, hand the note text to the user for manual entry.

Scope: notes, status, assignee, priority on existing tickets, and creation of single tickets.
Deletion, attachments, and bulk edits are out of scope.
