---
name: perl-dev
description: Use when writing, refactoring, or testing Perl and Mojolicious code.
---

# Perl Development Guidelines

- **Style**: Omit parentheses for `Test::More` assertions (`is $a, $b, 'msg'`). Prefer functional constructs (`map`, `grep`) over procedural loops and keep blank lines/comments minimal.
- **Efficiency & Idioms**: Avoid repeating chained method calls (e.g. `$self->req->json`), repetitive hash lookups, or redundant truthiness guards (`$val && ref $val eq 'HASH'`). Cache parsed request payloads or chained calls in a lexical variable (`my $json = $self->req->json;`) and check `ref $json eq 'HASH'` directly. Avoid redundant type coercions (e.g. `0 + CONSTANT`), defensive `ref` checks or fallbacks (`ref $val ? ... : $val`, `// ''`) for values already typed or guaranteed by the ORM/callers (e.g. `InflateColumn::DateTime` always returns a `DateTime` object or `undef`), and do not set test environment variables to values identical to module defaults (`//`); keep `0` delay/sleep settings in tests unless non-zero delay is required.
- **Self-Documenting Tests**: NEVER write in-file comments in tests (e.g. `# 1. Direct JSON`). Put scenario, inputs, and expected outcome into every assertion/subtest description (`$t->post_ok(...)->status_is(200, 'direct JSON payload accepted')`), using a `desc` field in data-driven test cases.
- **Mocking & Logging**: Prefer `Test::MockModule` or `Test::MockObject` over custom mock packages. Suppress Mojolicious logs in tests (`MOJO_LOG_LEVEL=fatal` or logger mock) unless testing log output.
- **Verification**: Always run the relevant test suite before claiming completion.
