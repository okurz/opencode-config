---
name: python-dev
description: Use when writing, refactoring, or testing Python code.
---

# Python Development Guidelines

- **Tools & Types**: Use `pytest`, `unittest.mock`/`pytest-mock` (no manual mock classes), `pydantic`/`dataclasses` over raw dicts, and consistent PEP 484 type hints.
- **Style**: Prefer comprehensions, `map`/`filter`, `itertools`/`functools`, dispatch dicts over `if/else` chains, and ternary expressions over verbose `if/else`.
- **Testing**: Keep test output free of uncaptured logs, warnings, or debug prints; verify coverage with project tools when requested.
