# opencode-config

Personal configuration for [opencode](https://opencode.ai) and the
[pi](https://github.com/badlogic/pi-mono) coding agent: model providers,
agents, slash commands, skills, prompts, and review rules. The repository
is the live `~/.config/opencode` directory, and pi reads the same files
through symlinks.

## Layout

| Path | Purpose |
|---|---|
| `opencode.jsonc` | Plugins, providers and models, agents, MCP servers |
| `AGENTS.md` | Global constraints and agent guidelines (also read by pi) |
| `agents/` | Sub-agent definitions (`explore`, `precision-fixer`, `pro-architect`) |
| `prompts/` | Shared prompt fragments referenced from `opencode.jsonc` |
| `commands/` | Slash commands; mirrored to pi as prompt templates |
| `skills/` | Skills loaded on demand; mirrored to pi unchanged |
| `review-checklist.md` | Checklist used by the pre-push and review commands |
| `review-protocol.md` | Read-only reviewer protocol used by the review commands |
| `Modelfile.30b-32k` | Ollama Modelfile for a local 32k-context coder model |

## Plugins

`opencode.jsonc` loads these plugins: `opencode-gemini-auth` (Gemini OAuth),
`opencode-notifier`, `opencode-tps-meter`, `opencode-plugin-llama.cpp`, and
`context-mode`. Plugins are fetched at startup, so a fresh machine needs
network access on first run.

## Providers and secrets

Endpoints and API keys are never stored in this repository. `opencode.jsonc`
references them with `{file:...}` placeholders that opencode resolves at
startup. The referenced files live outside the repo, in
`~/.config/opencode_secrets/` (for endpoint URLs and keys) or in the home
directory (for some tokens):

- `gateway_<name>_url` and `gateway_<name>_key`: LiteLLM-style gateways
- `ollama_url`, `lmstudio_<name>_url`: local or LAN model servers
- `suse_osd_llm_url`, `prometheus_llm_url`: llama.cpp endpoints
- `amazon-bedrock`: Authenticates via standard AWS profile `bedrock` in
  `~/.aws/config` without storing keys or credentials in this repository. In
  `opencode.jsonc`, configured via `@ai-sdk/amazon-bedrock` with
  `"profile": "bedrock"`. In pi, auth is delegated in `~/.pi/agent/auth.json`
  via `AWS_PROFILE` and scoped in `~/.pi/agent/settings.json` via `enabledModels`.
- `homeassistant_url`, `homeassistant_token`, `evcc_url`: optional integrations

Each file holds a single value with no trailing newline. A provider whose
files are missing fails at request time, not at startup. `.gitignore`
excludes `*_url`, `*.url`, `*_token`, and `*.token` as a safety net.

To check that every placeholder resolves, run from the repo root:

```sh
grep -oE '\{file:[^}]+\}' opencode.jsonc | sort -u
```

## Agents and models

- Models are set per agent in `opencode.jsonc`; there is no global default.
- Builder agents (`haiku-builder`, `flash-builder`, `gateway-builder`) share
  `prompts/builder.txt` and differ only in model.
- `explore` is a read-only research agent. It has no edit or write tools.
- `pro-architect` and `precision-fixer` are the planning and fixing roles
  used by the multi-agent command variants.

Commands accept `architect=`, `builder=`, `fixer=`, and `reviewer=` overrides
to swap the agent behind a role for one invocation.

## Commands

Commands are Markdown files in `commands/`. The file name is the slash
command name. Groups:

- **Planning and tickets**: `plan`, `plan-thorough`, `plan-with-agents`,
  `start-ticket`, `start-ticket-with-agents`, `execute-plan`, `tasks-status`,
  `tasks-apply`, `handoff`, `to-spec`, `to-tickets`, `triage`.
- **Implementation and tests**: `implement`, `tdd`, `verify`,
  `verify-coverage`, `acceptance`.
- **Review**: `pre-push-review`, `review-branch`, `review-single`,
  `review-as-bot`, `address-review`, `review-retro`, `pr-status`.
- **Git**: `commit`, `rebase-all`.
- **Domain tools**: `analyze-openqa-log`, `sync-leap`, `fetch_redmine`.
- **Config and learning**: `opencode-config`, `learn`, `teach`, `explain`,
  `wait-what`, `wayfinder`, `improve-codebase-architecture`.
- **Vendored upstream commands**: `addy-*` (from addyosmani/agent-skills),
  `grill-*`, `domain-modeling`, `setup-matt-pocock-skills` (from
  mattpocock/skills). Edit the whitelist, not the copies.

## Skills

Skills are `skills/<name>/SKILL.md` files with frontmatter (`name`,
`description`). The description decides when an agent loads the skill.

Project-specific skills cover openQA (`openqa-log-analysis`,
`openqa-llm-investigate`, `openqa-svirt`), Perl and Python development,
testing, Git workflow, RPM packaging, Leap package sync, Redmine access, and
branch triage. Skills that are not project-specific come from the vendored
upstream collections in `~/.agents/skills`.

## Review rules

`review-checklist.md` holds the checklist that reviewer commands apply, and
`review-protocol.md` defines the read-only reviewer procedure. Review
learnings are recorded outside the repo (`review-learnings.md`, git-ignored)
and promoted into the checklist once a class of comment recurs.

## Using with pi

pi reads the same content through symlinks, so there is no separate copy to
keep in sync:

- `~/.pi/agent/AGENTS.md` → `AGENTS.md`
- `~/.pi/agent/prompts` → `commands/`
- `~/.pi/agent/skills` → `skills/`

Edit files in this repository only. Do not edit the pi paths directly.

## Development

Edits to this repository are configuration, not code. Before committing:

- Validate `opencode.jsonc` as JSON with comments stripped. Lines beginning
  with `//` are comments in this file.
- Check that every `{file:...}` placeholder resolves (see above).
- Lint commit messages with `gitlint` where the commit is new.
- Run a non-interactive smoke test against one provider:

  ```sh
  opencode run -m <provider>/<model> "Reply with exactly: OK"
  ```

Commit messages follow Conventional Commits with `Motivation`,
`Design Choices`, and `Benefits` sections for behaviour changes. Commits are
GPG-signed.

