---
name: testing
description: Use when writing, fixing, or running tests, checking statement coverage, or running lint/type-check before completion.
---

# Test discipline

- **Execute After Fixing**: Always run the test command to confirm a fix passes; never assume.
- **Targeted Coverage**: Do not wait for CI (Codecov). Run coverage locally on only the test files for your changes (e.g. `.t` or `test_*.py`) and verify all added/modified lines are covered before committing.
- **Proactive Linting**: Run project linters, formatters, and type-checkers (`perlcritic`, `ruff`, `eslint`, `tools/tidy`) before functional verification and before claiming completion.
- **Integration Realism**: For execution-flow or integration changes, adapt existing full-stack tests or reuse failing/softfailing modules to exercise the real path.
- **Clean Output & No Redundancy**: Test runner output must be clean (no stray logs/warnings). Check existing test files before adding new ones and add only unique coverage.
- **Data-Driven & Self-Documenting Tests**: Prefer parameterized/data-driven test tables (with a `desc` field per case) over repetitive single-assertion tests. NEVER write in-file comments in tests (e.g. `# 1. Direct JSON`, `# Assert fields`); encode all intent, inputs, and expected outcomes in test/subtest description strings.
