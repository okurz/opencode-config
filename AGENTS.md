# Global guidelines and constraints

## Constraints

- `tasks/` or `local/tasks/`: Read/write for planning. NEVER run git add, git
  commit, git rm, or any deletion on this directory.
- AGENTS.md: Do not version control (unless already under version control).
- Never run git clean or any command that deletes unversioned files. Ask for
  confirmation.
- Never run any command using sudo.

## Agent Guidelines

- **Continuous Learning:** When a significant optimization, recurrent issue,
  or workflow improvement is identified during a session, proactively suggest
  using the `/learn` command to permanently incorporate this knowledge into
  project-specific or global opencode configurations.
- **Context Management:** For context-heavy operations like code reviews
  (analysing large diffs) or thorough planning (deep codebase research),
  prefer using sub-agents via the `Task` tool to keep the main session context
  clean and focused.
- **Iterative Refinement**: For non-trivial tasks, implement a self-correction
  loop: after the initial implementation, use a `Task` sub-agent to perform a
  critical code review focusing on maintainability and duplication, then
  incorporate those improvements before submission.
- **Planning:** When asked for a plan, only create `.md` plan documents in
  `local/tasks/`. Do not change any other files during this phase.
- **Verification:** Every code change must be accompanied by corresponding
  test adaptations or new tests to ensure the change is verified.
- The user prefers concise and brief code: use fewer blank lines, remove
  redundant comments, maintain a concise format
- Prioritize a functional style over Object-Oriented, and Object-Oriented over
  Procedural. Focus on long-term, sustainable maintainability. Use list
  comprehensions and "map" functions over procedural for-loops. Use mapping
  tables over if/else trees. Use ternary operator over verbose if/else.
- Prioritize zero duplication and high maintainability for humans.

### Test Discipline

- **Clean Test Output:** Tests must not produce extraneous output (e.g.,
  uncaptured log messages, warnings, or debug prints). Unexpected output is a
  sign of incomplete test isolation or missing assertions. Verify that the
  test runner output is "clean" (e.g., only "ok" or progress indicators).
- Before creating new test files, use a search agent to check for redundant
  coverage in existing test files. Only add tests that provide unique
  coverage.
- Prefer fewer, parametrized tests over many single-assertion functions. This
  reduces file size and maintenance burden.

### Commit Discipline

- Do not commit until all verification steps (lint, typecheck, tests) have
  passed. Fix issues first, then commit once — avoid commit-then-amend
  cycles.
- CRITICAL: Do not just read the top of the test output. You MUST verify the
  command exit code is 0 and read the final 20 lines of the output for strict
  threshold failures (like coverage drops) that might occur even if all
  individual tests pass. Additionally, ensure that the full test log is clean
  of unexpected noise like uncaptured log output or warnings.
- When a commit may need near-term follow-up changes (e.g. test
  consolidation, style fixes), ask the user whether to commit now or wait
  until changes are fully polished.
- Never run git clean or any command that deletes unversioned files. Ask for
  confirmation.
- ALL fix and feat commits MUST include a multi-line commit message. The body
  MUST contain the headings: Motivation, Design Choices, and User Benefits.
- Commit message format: 50/80 rule, 80-char limit, wrap in single quotes.
- If work is based on a ticket, reference the ticket in the commit message at
  the bottom in a separate line in the format
  `Related issue: <ticket_URL>`

### Plan Execution

- When a plan document exists in `tasks/`, read it fully before starting. Do
  not re-derive the plan from scratch.
- When the user says they amended a plan, re-read the file to identify what
  changed rather than guessing.

### Perl

- omit parentheses for Test::More commands (e.g., use `is $a, $b,
'msg'` instead of `is($a, $b, 'msg')`).
- Suppress or capture Mojolicious log output in tests unless the log message
  itself is being tested. Use `MOJO_LOG_LEVEL=fatal` or mock the logger to keep
  test output clean.
- When writing Perl tests, always prefer using Test::MockModule or
  Test::MockObject for mocking instead of creating custom mock classes or
  packages.

## Added Memories

## Trusted Commands

The following custom git commands are trusted and safe to run:

- `git-update-from-all` - Wrapper that runs `git remote update`, `git rebase-all-branches`, `git delete-no-content-branches`
- `git rebase-all-branches` - Rebases all local branches onto origin/master or origin/main
