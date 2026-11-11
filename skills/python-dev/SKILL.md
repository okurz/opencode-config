---
name: python-dev
description: Specialized instructions for Python development and testing.
---

# Python Development Guidelines

## Tools & Frameworks
- Prefer `pytest` for all new test developments.
- Use `unittest.mock` or `pytest-mock` to isolate dependencies. Avoid manual mock implementations.
- Favor `pydantic` or `dataclasses` over raw dictionaries for structured data.

## Coding Style
- Mandate type hints (PEP 484) consistently to improve code clarity and LLM-assisted development.
- Prioritize a functional style: use list comprehensions, `map`, `filter`, and functional tools (e.g. from `itertools`, `functools`) over procedural for-loops.
- Use mapping tables over if/else trees.
- Use ternary operator over verbose if/else.

## Testing Discipline
- Ensure clean test output: no uncaptured log messages, warnings, or debug prints.
- Verify coverage when requested using project-specific tools.
