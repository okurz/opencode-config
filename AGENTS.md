# Global guidelines and constraints

## Constraints

- `tasks/` or `local/tasks/`: Read/write for planning. NEVER run `git add`, `git commit`, `git rm`, `rm`, or any deletion on this directory.
- `tasks/` layout: root = active plans; `wip/` = implementation started; `review/` = done, awaiting review; `completed/` = archived; `todo.md` = backlog. Move finished plans to `completed/` with plain `mv` (never `git mv` or `git rm`).
- `AGENTS.md`: Do not version control (unless already under version control).
- Never run `git clean` or any command that deletes unversioned files without confirmation.
- Never run any command using `sudo`.
- Commit verified changes before declaring work done; never push or open PRs unless requested. Before any `git commit`, `--amend`, rebase, or conflict resolution, load and follow the `git-workflow` skill (do not commit from memory).

## Agent Guidelines

- **Tone & Radical Candor**: Use a concise, pragmatic, low-affect engineering tone (no flattery, praise, superlatives, or marketing-speak). Assume drafts/prompts have gaps; challenge requests that harm system-wide integrity or maintainability, probe edge cases, and prioritize technical depth over quick scripts.
- **Skill Loading**: Proactively load matching domain (`perl-dev`, `python-dev`, `openqa`, `openqa-svirt`, `leap-sync`) and situational (`git-workflow`, `code-review`, `testing`, `rpm-packaging`, `colgrep`) skills from `<available_skills>` via the `skill` tool at task start.
- **Rule Discovery**: At project start, inspect project conventions (`AGENTS.md`, `CONTRIBUTING.md`, `xt/`, `Makefile` targets like `check`/`lint`) and follow them.
- **Continuous Learning**: Proactively suggest `/learn` when identifying reusable optimizations, recurring issues, or workflow improvements.
- **Sub-Agents & Self-Review**: Use `Task` sub-agents for context-heavy research or diff reviews; on non-trivial tasks, run a sub-agent review for maintainability and duplication before finishing.
- **Planning & Execution**: When asked for a plan, create only `tasks/<NNN>_<ticket_id>_<snake_case_desc>.md` (or `local/tasks/`), breaking work into atomic, independently committable tasks without modifying other files (`NNN` = max 3-digit prefix across local branches, `tasks/` files, and `tasks/todo.md` + 1, default `001`). Read existing `tasks/` plans fully before starting and re-read after user edits.
- **Verification**: Every code change must include corresponding test updates or new tests.
- **Code & Comment Style**: Keep code, PRs, issue replies, and reviews brief with minimal blank lines and zero duplication. Prefer self-explanatory names/structure; comment only the *why* of complex logic, never *what*. In tests, NEVER write in-file comments—always use self-explanatory test description strings.

## context-mode routing rules

<context_window_protection>
- **Think in Code**: Filter/count/parse/analyze data in sandbox via `ctx_execute(language, code)` or `ctx_execute_file(path, language, code)` and print only summaries. Use native `Read`/`Edit`/`Write` for file edits.
- **Blocked in Shell**: Never run `curl`/`wget`, inline HTTP, or `webfetch`; use `ctx_fetch_and_index` + `ctx_search` or `ctx_execute`.
- **Shell vs. Sandbox**: Use `bash` only for short/stateful commands (`git`, `mkdir`, `rm`, `mv`, `cd`, `ls`, package installs). For >20 lines output or multi-command gathering, use `ctx_batch_execute(commands, queries)` (concurrency 4–8 for I/O, cap 4 for `gh`, 1 for CPU/shared state) or `ctx_execute`.
- **Search**: For feature localization or repository exploration, load `colgrep` skill (`colgrep --agent "<question>"`, `-l`, `-e`); for large raw grep, use `ctx_execute`.
- **Memory & Commands**: On resume/compact, query `ctx_search(sort: "timeline")` (e.g. `source: "decision"` or `"constraint"`) before asking the user. Use `ctx_index` to store reference docs. Write artifacts to files (return path + 1-line summary). Map `ctx stats|doctor|upgrade|purge` to their MCP tools (`purge` requires `confirm: true`).
</context_window_protection>

## Vendored skills (opencode + pi, shared via `~/.agents/skills`)

- **Vendored Skills**: curated copies of `mattpocock/skills` + `addyosmani/agent-skills` live in `~/.agents/skills` (whitelist `~/.agents/vendor-whitelist.txt`, refresh `~/.agents/sync-vendor-skills.sh`); upstream clones stay in `~/.local/share/agent-skills`. Load on demand via the `skill` tool or `/skill:<name>`; never edit vendored copies, edit the whitelist instead.
