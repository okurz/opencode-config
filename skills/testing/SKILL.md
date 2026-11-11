---
name: testing
description: Use when writing, fixing, or running tests, enforcing statement-coverage thresholds, or running lint/type-check before claiming completion. Covers test execution after fixes, targeted coverage, clean output, and self-explanatory data-driven tests.
---

# Test discipline

- **Execute Tests After Fixing**: When asked to fix a failing test, you MUST run the test command to verify the fix is effective. Do not assume the fix works without execution — always confirm the test passes.
- **Targeted Coverage Verification**: When a project requires strict statement coverage, do NOT rely on CI (like Codecov) to find missing coverage, as the feedback loop is too slow. Instead, run coverage locally, but strictly limit the execution to the specific test files associated with your changes to save time (e.g., target specific `.t` or `test_*.py` files). Check the local coverage report specifically for the lines you added/modified before committing.
- **Proactive Linting**: Always run identified linting, style, and type-checking commands (e.g. `perlcritic`, `ruff`, `eslint`, `tools/tidy`) _before_ attempting verification of functional logic and _before_ claiming completion. Adhere to project style from the first implementation turn.
- **Integration Realism**: For features affecting the execution flow or integration points, prioritize using or adapting existing "full stack" tests or reusing existing failing/softfailing modules to ensure the real-world execution path is exercised.
- **Clean Test Output**: Tests must not produce extraneous output. Verify that the test runner output is "clean" (e.g., only "ok" or progress indicators).
- Before creating new test files, use a search agent to check for redundant coverage in existing test files. Only add tests that provide unique coverage.
- **Self-Explanatory Test Descriptions (NO in-file comments in tests)**: NEVER add in-file comments to explain test steps, assertions, setup, or numbered sections (e.g. `# 1. Direct JSON`, `# Assert fields`, `# Test error case`). Instead, bake all context, intent, inputs, and expected outcomes directly into the test description strings passed to test functions or subtests. In data-driven tests, include a `desc` property in each case. The test runner output must be fully self-documenting on its own without needing in-file comments.
- **Data-Driven and Parametrized Tests**: Prefer fewer, parametrized or data-driven tests (e.g., using arrays of test cases) over many single-assertion functions or repetitive helper function calls. This reduces file size and maintenance burden. Bake the logic, context, and expectations directly into self-explanatory test description strings rather than relying on in-file code comments, ensuring the test runner output is fully self-documenting.
