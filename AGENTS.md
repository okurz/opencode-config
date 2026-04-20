# Global guidelines and constraints

## Constraints

- `tasks/` or `local/tasks/`: Read/write for planning. NEVER run git add, git
  commit, git rm, `rm` or any deletion on this directory.
- AGENTS.md: Do not version control (unless already under version control).
- Never run git clean or any command that deletes unversioned files. Ask for
  confirmation.
- Never run any command using sudo.

## Agent Guidelines

- **Skill Loading**: Proactively load the relevant language-specific (e.g.,
  `perl-dev`, `python-dev`) skills using the `skill` tool at the beginning of
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
  type-checking commands (e.g. `perlcritic`, `ruff`, `eslint`) *before*
  attempting verification of functional logic and *before* claiming completion.
  Adhere to project style from the first implementation turn.
- **Integration Realism**: For features affecting the execution flow or
  integration points, prioritize using or adapting existing "full stack" tests
  or reusing existing failing/softfailing modules to ensure the real-world
  execution path is exercised.
- **Clean Test Output**: Tests must not produce extraneous output. Verify that the
  test runner output is "clean" (e.g., only "ok" or progress indicators).
- Before creating new test files, use a search agent to check for redundant
  coverage in existing test files. Only add tests that provide unique
  coverage.
- Prefer fewer, parametrized tests over many single-assertion functions. This
  reduces file size and maintenance burden.

### Commit Discipline

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
- To execute multi-line commits reliably without temporary files, ALWAYS use a bash heredoc.
- If work is based on a ticket, reference the ticket in the commit message at
  the bottom in a separate line in the format `Related issue: <ticket_URL>`

### Plan Execution

- When a plan document exists in `tasks/`, read it fully before starting. Do
  not re-derive the plan from scratch.
- When the user says they amended a plan, re-read the file to identify what
  changed rather than guessing.

### Review Management

- **Fetch Feedback**: Use the `gh` tool to fetch review comments from GitHub PRs.
- **Direct Comment Targeting**: If a URL with `#discussion_r(\d+)` is provided, parse the ID and use `gh api repos/:owner/:repo/pulls/comments/:id` to fetch only that specific feedback and its context.
- **Structured Address**: Create a plan in `tasks/` that explicitly lists all
  reviewer suggestions as a checklist (or use `todowrite`) to ensure 100%
  coverage of feedback.
- **Fixup Commits**: For PRs already in review, default to using `git commit --fixup <commit_hash>`
  to address feedback, unless a full rebase or new commit is explicitly requested.
- **Verify-Implement-Verify**: For each suggestion, first verify the current
  behavior/issue, implement the fix, and then verify again with tests and linting.
- **No Force Push**: Never force push to a remote branch unless the user explicitly
  confirms it is safe (e.g., in a personal feature branch).
