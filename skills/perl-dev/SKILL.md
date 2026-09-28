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

- **Zero In-File Comments / Self-Documenting Test Descriptions**: NEVER write in-file comments in test files (e.g. `# 1. Direct JSON`, `# Step 2: assert response`, `# Assert fields`). Instead, every assertion (`is`, `ok`, `like`, etc.) and `subtest` must carry a self-explanatory description string explaining the exact scenario, inputs, and expected outcome. When writing data-driven tests, include a `desc` field in each test case and interpolate it into the test message:
  - BAD:
    ```perl
    # 1. Direct JSON body
    $t->post_ok('/api/v1/resource', json => {foo => 'bar'})->status_is(200);
    is $res->{status}, 'ok', 'status ok';
    ```
  - GOOD:
    ```perl
    $t->post_ok('/api/v1/resource', json => {foo => 'bar'})->status_is(200, 'direct JSON payload accepted');
    is $res->{status}, 'ok', 'status is ok for valid JSON payload';
    ```
- **Mocking**: When writing Perl tests, always prefer using `Test::MockModule` or `Test::MockObject` for mocking instead of creating custom mock classes or packages.
- **Logging**: Suppress or capture Mojolicious log output in tests unless the log message itself is being tested. Use `MOJO_LOG_LEVEL=fatal` or mock the logger to keep test output clean.
- **Verification**: Always run the relevant test suite before claiming completion.
