---
name: perl-dev
description: Use when writing, refactoring, or testing Perl and Mojolicious code.
---

# Perl Development Guidelines

- **Style**: Omit parentheses for `Test::More` assertions (`is $a, $b, 'msg'`). Prefer functional constructs (`map`, `grep`) over procedural loops and keep blank lines/comments minimal.
- **Self-Documenting Tests**: NEVER write in-file comments in tests (e.g. `# 1. Direct JSON`). Put scenario, inputs, and expected outcome into every assertion/subtest description (`$t->post_ok(...)->status_is(200, 'direct JSON payload accepted')`), using a `desc` field in data-driven test cases.
- **Mocking & Logging**: Prefer `Test::MockModule` or `Test::MockObject` over custom mock packages. Suppress Mojolicious logs in tests (`MOJO_LOG_LEVEL=fatal` or logger mock) unless testing log output.
- **Verification**: Always run the relevant test suite before claiming completion.
