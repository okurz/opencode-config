# Global guidelines and constraints

## Constraints

- `tasks/` or `local/tasks/`: Read/write for planning. NEVER run git add, git
  commit, git rm, or any deletion on this directory.
- AGENTS.md: Do not version control.
- Never run git clean or any command that deletes unversioned files. Ask for
  confirmation.
- Never run any command using sudo.

## Agent Guidelines

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
- ALL fix and feat commits MUST include a multi-line commit message. The body
  MUST contain the headings: Motivation, Design Choices, and User Benefits.

### Test Discipline

- Before creating new test files, use a search agent to check for redundant
  coverage in existing test files. Only add tests that provide unique
  coverage.
- Prefer fewer, parametrized tests over many single-assertion functions.
  This reduces file size and maintenance burden.

### Commit Discipline

- Do not commit until all verification steps (lint, typecheck, tests) have
  passed. Fix issues first, then commit once — avoid commit-then-amend
  cycles.
- When a commit may need near-term follow-up changes (e.g. test
  consolidation, style fixes), ask the user whether to commit now or wait
  until changes are fully polished.

### Plan Execution

- When a plan document exists in `tasks/`, read it fully before starting. Do
  not re-derive the plan from scratch.
- When the user says they amended a plan, re-read the file to identify what
  changed rather than guessing.

### Perl

- omit parentheses for Test::More commands (e.g., use `is $a, $b,
'msg'` instead of `is($a, $b, 'msg')`). Prioritize zero duplication and high
  maintainability for humans.
- When writing Perl tests, always prefer using Test::MockModule or
  Test::MockObject for mocking instead of creating custom mock classes or
  packages.

## Added Memories

## Trusted Commands

The following custom git commands are trusted and safe to run:
- `git-update-from-all` - Wrapper that runs `git remote update`, `git rebase-all-branches`, `git delete-no-content-branches`
- `git rebase-all-branches` - Rebases all local branches onto origin/master or origin/main
