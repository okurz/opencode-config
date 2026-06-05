# Global guidelines and constraints

## Constraints

- `tasks/` or `local/tasks/`: Read/write for planning. NEVER run git add, git
  commit, git rm, `rm` or any deletion on this directory.
- AGENTS.md: Do not version control (unless already under version control).
- Never run git clean or any command that deletes unversioned files. Ask for
  confirmation.
- Never run any command using sudo.

## Agent Guidelines

- **Skill Loading**: Proactively load the relevant language-specific or domain-specific (e.g.,
  `perl-dev`, `python-dev`, `openqa`, `leap-sync`) skills using the `skill` tool at the beginning of
  a task.
- **Rule Discovery**: At the start of a project, always search for
  project-specific conventions (e.g., `AGENTS.md`, `CONTRIBUTING.md`, `xt/`
  tests, `Makefile` targets like `check` or `lint`) and incorporate them into
  your workflow.
- **Continuous Learning**: When a significant optimization, recurrent issue,
  or workflow improvement is identified during a session, proactively suggest
  using the `/learn` command to permanently incorporate this knowledge into
  project-specific or global opencode configurations.
- **Context Management**: For context-heavy operations like code reviews
  (analysing large diffs) or thorough planning (deep codebase research),
  prefer using sub-agents via the `Task` tool to keep the main session context
  clean and focused.
- **Iterative Refinement**: For non-trivial tasks, implement a self-correction
  loop: after the initial implementation, use a `Task` sub-agent to perform a
  critical code review focusing on maintainability and duplication, then
  incorporate those improvements before submission.
- **Planning**: When asked for a plan, only create `.md` plan documents in
  `tasks/` (or `local/tasks/` if exists). Use the naming convention
  `<3-digit-number>_<ticket_id>_<description>.md` for new tasks, where
  description is in snake_case. Determine the next free task number by taking
  the maximum of (a) the 3-digit prefixes of all local git branches, (b) the
  3-digit prefixes of all files in `tasks/`, and (c) any listed task numbers
  in `tasks/todo.md`. Increment this maximum by one (e.g., if the highest is
  061, use 062). If no numbers are found, start with 001. Do not change any
  other files during this phase.
- **Task Atomicity**: When planning, break down complex requests into smaller, independent tasks that can be implemented and committed individually to ensure clear and focused commits.
- **Verification**: Every code change must be accompanied by corresponding
  test adaptations or new tests to ensure the change is verified.
- The user prefers concise and brief code: use fewer blank lines, remove
  redundant comments, maintain a concise format. Prioritize self-explanatory
  code (e.g., descriptive variable/function names, clear structure) over
  in-file comments. Comments should only be used to explain the *why* of
  complex logic, not the *what* of the code.
- Prioritize zero duplication and high maintainability for humans.

### Test Discipline

- **Execute Tests After Fixing**: When asked to fix a failing test, you MUST
  run the test command to verify the fix is effective. Do not assume the fix
  works without execution — always confirm the test passes.
- **Targeted Coverage Verification**: When a project requires strict statement coverage, do NOT rely on CI (like Codecov) to find missing coverage, as the feedback loop is too slow. Instead, run coverage locally, but strictly limit the execution to the specific test files associated with your changes to save time (e.g., target specific `.t` or `test_*.py` files). Check the local coverage report specifically for the lines you added/modified before committing.
- **Proactive Linting**: Always run identified linting, style, and
  type-checking commands (e.g. `perlcritic`, `ruff`, `eslint`, `tools/tidy`)
  *before* attempting verification of functional logic and *before* claiming
  completion. Adhere to project style from the first implementation turn.
- **Integration Realism**: For features affecting the execution flow or
  integration points, prioritize using or adapting existing "full stack" tests
  or reusing existing failing/softfailing modules to ensure the real-world
  execution path is exercised.
- **Clean Test Output**: Tests must not produce extraneous output. Verify that the
  test runner output is "clean" (e.g., only "ok" or progress indicators).
- Before creating new test files, use a search agent to check for redundant
  coverage in existing test files. Only add tests that provide unique
  coverage.
- **Data-Driven and Parametrized Tests**: Prefer fewer, parametrized or
  data-driven tests (e.g., using arrays of test cases) over many single-assertion
  functions or repetitive helper function calls. This reduces file size and
  maintenance burden. Bake the logic, context, and expectations directly into
  self-explanatory test description strings rather than relying on in-file
  code comments, ensuring the test runner output is fully self-documenting.

### Commit Discipline

- **Atomic Commits**: Each commit MUST focus on a single conceptual change or task. Do not mix unrelated changes, such as bug fixes, logging improvements, and new features, into a single commit. If multiple unrelated changes are needed, implement and commit them sequentially.
- Do not commit until all verification steps (lint, typecheck, tests) have
  passed. Fix issues first, then commit once — avoid commit-then-amend cycles.
- CRITICAL: Do not just read the top of the test output. You MUST verify the
  command exit code is 0 and read the final 20 lines of the output for strict
  threshold failures (like coverage drops) that might occur even if all
  individual tests pass.
- When a commit may need near-term follow-up changes (e.g. test consolidation,
  style fixes), ask the user whether to commit now or wait until changes are
  fully polished.
- Never run git clean or any command that deletes unversioned files. Ask for
  confirmation.
- ALL fix and feat commits MUST include a multi-line commit message. The body
  MUST contain the headings: Motivation, Design Choices, and Benefits.
- Commit message format: 50/80 rule. You MUST explicitly insert physical newlines to hard-wrap the body text at 80 characters.
- To execute multi-line commits reliably without temporary files or interactive editors, ALWAYS use a bash heredoc via standard input: `git commit -F - <<EOF`.
- After creating or amending a commit, run any project-specific commit linters (e.g. `make test-gitlint`). If the linter fails, use `git commit --amend -F - <<EOF` to fix the message.
- If work is based on a ticket, reference the ticket in the commit message at
  the bottom in a separate line in the format `Related issue: <ticket_URL>`

### Plan Execution

- When a plan document exists in `tasks/`, read it fully before starting. Do
  not re-derive the plan from scratch.
- When the user says they amended a plan, re-read the file to identify what
  changed rather than guessing.

### Review Management

- **Evaluate Feedback First**: Do not blindly implement reviewer suggestions. First, review the original commit messages and design choices to understand the context. Evaluate whether the comment makes sense and aligns with the codebase. You MUST always formulate an implementation plan and present it to the user for approval BEFORE executing any code changes or commits, regardless of how straightforward the comment seems.
- **Fetch Feedback**: Use the `gh` tool to fetch review comments from GitHub PRs.
- **Direct Comment Targeting**: If a URL with `#discussion_r(\d+)` is provided, parse the ID and use `gh api repos/:owner/:repo/pulls/comments/:id` to fetch only that specific feedback and its context.
- **Structured Address**: Use the `todowrite` tool to explicitly list all
  reviewer suggestions as a checklist to ensure 100% coverage of feedback.
- **Fixup Commits**: For PRs already in review, default to using `git commit --fixup <commit_hash>`
  to address feedback, unless a full rebase or new commit is explicitly requested.
- **Verify-Implement-Verify**: For each suggestion, first verify the current
  behavior/issue, implement the fix, and then verify again with tests and linting.
- **No Force Push**: Never force push to a remote branch unless the user explicitly
  confirms it is safe (e.g., in a personal feature branch).

# context-mode — MANDATORY routing rules

context-mode MCP tools available. Rules protect context window from flooding. One unrouted command dumps 56 KB into context.

## Think in Code — MANDATORY

Analyze/count/filter/compare/search/parse/transform data: **write code** via `context-mode_ctx_execute(language, code)`, `console.log()` only the answer. Do NOT read raw data into context. PROGRAM the analysis, not COMPUTE it. Pure JavaScript — Node.js built-ins only (`fs`, `path`, `child_process`). `try/catch`, handle `null`/`undefined`. One script replaces ten tool calls.

## BLOCKED — do NOT attempt

### curl / wget — BLOCKED
Shell `curl`/`wget` intercepted and blocked. Do NOT retry.
Use: `context-mode_ctx_fetch_and_index(url, source)` or `context-mode_ctx_execute(language: "javascript", code: "const r = await fetch(...)")`

### Inline HTTP — BLOCKED
`fetch('http`, `requests.get(`, `requests.post(`, `http.get(`, `http.request(` — intercepted. Do NOT retry.
Use: `context-mode_ctx_execute(language, code)` — only stdout enters context

### Direct web fetching — BLOCKED
Use: `context-mode_ctx_fetch_and_index(url, source)` then `context-mode_ctx_search(queries)`

## REDIRECTED — use sandbox

### Shell (>20 lines output)
Shell ONLY for: `git`, `mkdir`, `rm`, `mv`, `cd`, `ls`, `npm install`, `pip install`.
Otherwise: `context-mode_ctx_batch_execute(commands, queries)` or `context-mode_ctx_execute(language: "shell", code: "...")`

### File reading (for analysis)
Reading to **edit** → reading correct. Reading to **analyze/explore/summarize** → `context-mode_ctx_execute_file(path, language, code)`.

### grep / search (large results)
Use `context-mode_ctx_execute(language: "shell", code: "grep ...")` in sandbox.

## Tool selection

0. **MEMORY**: `context-mode_ctx_search(sort: "timeline")` — after resume, check prior context before asking user.
1. **GATHER**: `context-mode_ctx_batch_execute(commands, queries)` — runs all commands, auto-indexes, returns search. ONE call replaces 30+. Each command: `{label: "header", command: "..."}`.
2. **FOLLOW-UP**: `context-mode_ctx_search(queries: ["q1", "q2", ...])` — all questions as array, ONE call (default relevance mode).
3. **PROCESSING**: `context-mode_ctx_execute(language, code)` | `context-mode_ctx_execute_file(path, language, code)` — sandbox, only stdout enters context.
4. **WEB**: `context-mode_ctx_fetch_and_index(url, source)` then `context-mode_ctx_search(queries)` — raw HTML never enters context.
5. **INDEX**: `context-mode_ctx_index(content, source)` — store in FTS5 for later search.

## Parallel I/O batches

For multi-URL fetches or multi-API calls, **always** include `concurrency: N` (1-8):

- `context-mode_ctx_batch_execute(commands: [3+ network commands], concurrency: 5)` — gh, curl, dig, docker inspect, multi-region cloud queries
- `context-mode_ctx_fetch_and_index(requests: [{url, source}, ...], concurrency: 5)` — multi-URL batch fetch

**Use concurrency 4-8** for I/O-bound work (network calls, API queries). **Keep concurrency 1** for CPU-bound (npm test, build, lint) or commands sharing state (ports, lock files, same-repo writes).

GitHub API rate-limit: cap at 4 for `gh` calls.

## Output

Write artifacts to FILES — never inline. Return: file path + 1-line description.
Descriptive source labels for `search(source: "label")`.

## Session Continuity

Skills, roles, and decisions persist for the entire session. Do not abandon them as the conversation grows.

## Memory

Session history is persistent and searchable. On resume, search BEFORE asking the user:

| Need | Command |
|------|---------|
| What did we decide? | `context-mode_ctx_search(queries: ["decision"], source: "decision", sort: "timeline")` |
| What constraints exist? | `context-mode_ctx_search(queries: ["constraint"], source: "constraint")` |

DO NOT ask "what were we working on?" — SEARCH FIRST.
If search returns 0 results, proceed as a fresh session.

## ctx commands

| Command | Action |
|---------|--------|
| `ctx stats` | Call `stats` MCP tool, display full output verbatim |
| `ctx doctor` | Call `doctor` MCP tool, run returned shell command, display as checklist |
| `ctx upgrade` | Call `upgrade` MCP tool, run returned shell command, display as checklist |
| `ctx purge` | Call `purge` MCP tool with confirm: true. Warns before wiping knowledge base. |

After /clear or /compact: knowledge base and session stats preserved. Use `ctx purge` to start fresh.
