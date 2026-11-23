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

This tree runs OpenCode V2 and loads `opencode-gemini-auth@2.0.1`,
`@mohak34/opencode-notifier@1.1.3` and `context-mode@2.2.2`. Plugins are fetched
at startup, so a fresh machine needs network access on first run, and the pins
are exact so a running install cannot move under itself.

`context-mode` keeps tool output above 16 KB out of the context window: it
replaces the result with a pointer and archives the text for `ctx_search` under
`~/.context-mode/projects/`. Its nine `ctx_*` tools add about 8 KB of schema, so
the four unused built-ins (`generate_image`, `generate_video`, `websearch`,
`webfetch`) are disabled in `tools` to offset it.

## Versions and the V1 legacy sandbox

`opencode` resolves to a wrapper in `~/bin` that execs
`~/.local/opencode2/bin/opencode2` (V2, `@opencode/cli`):

| Path | Purpose |
|---|---|
| `~/bin/opencode` | V2 with the default dirs, i.e. this repository |
| `~/bin/opencode1` | V1 `opencode-ai@1.19.6`, frozen legacy sandbox |
| `~/.local/opencode2` | V2 npm prefix |
| `~/.local/opencode1` | V1 npm prefix |
| `~/.config/opencode-1/opencode/` | V1 config: forked `opencode.jsonc` with the pinned V1 plugin list, every other asset symlinked here |
| `~/.local/{share,state}/opencode-1/opencode`, `~/.cache/opencode-1/opencode` | V1 data, state and plugin cache |

The V2 wrapper unsets `GEMINI_API_KEY`: `~/.profile` exports a stale key that V2
would otherwise resolve as the Google credential.
`cli.json` (V2 terminal client) and `service.json` (background service
registration) are machine-local and untracked.

V1 is the escape hatch for what the V2 build of `opencode-gemini-auth` no longer
provides (`/gquota`, quota tool, retry transport, capacity notices) and for
V1-only plugins
(`opencode-tps-meter`, `opencode-plugin-llama.cpp`, `context-mode`). Upgrade V2
explicitly with `npm install -g --prefix ~/.local/opencode2 @opencode/cli@<version>`
plus `node postinstall.mjs` inside the installed package, because npm runs with
`ignore-scripts` here. Rollback is repointing `~/bin/opencode` at
`~/.local/opencode1/bin/opencode`.

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
- `deepseek-reviewer` (Helmcode `deepseek-v4-flash`) is a read-only reviewer
  for `/pre-push-review reviewer=deepseek-reviewer`.
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

