---
name: perl-dev
description: Specialized instructions for Perl development and testing.
---

# Perl Development Guidelines

## Coding Style
- Omit parentheses for `Test::More` commands (e.g., use `is $a, $b, 'msg'` instead of `is($a, $b, 'msg')`).
- Prioritize a functional style (e.g., `map`, `grep`) over procedural for-loops where appropriate.
- Keep code concise: fewer blank lines, remove redundant comments.

## Testing Discipline
- **Mocking**: When writing Perl tests, always prefer using `Test::MockModule` or `Test::MockObject` for mocking instead of creating custom mock classes or packages.
- **Logging**: Suppress or capture Mojolicious log output in tests unless the log message itself is being tested. Use `MOJO_LOG_LEVEL=fatal` or mock the logger to keep test output clean.
- **Verification**: Always run the relevant test suite before claiming completion.
