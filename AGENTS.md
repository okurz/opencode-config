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
- **Verification:**
  - Every code change must be accompanied by corresponding test adaptations
    or new tests to ensure the change is verified.
- The user prefers concise and brief code: use fewer blank lines, remove
  redundant comments, maintain a concise format
- Prioritize a functional style over Object-Oriented, and Object-Oriented over
  Procedural. Focus on long-term, sustainable maintainability. Use list
  comprehensions and "map" functions over procedural for-loops. Use mapping
  tables over if/else trees. Use ternary operator over verbose if/else.

### Perl

- omit parentheses for Test::More commands (e.g., use `is $a, $b,
'msg'` instead of `is($a, $b, 'msg')`). Prioritize zero duplication and high
  maintainability for humans.
- When writing Perl tests, always prefer using Test::MockModule or
  Test::MockObject for mocking instead of creating custom mock classes or
  packages.

## Added Memories
