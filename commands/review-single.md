---
description: Perform a critical review of the last commit
---

Pretend to be a code reviewer of the last commit. Provide a critical review focusing on long-term, sustainable maintainability.

### Protocol:
1.  **Context Gathering**: Start by retrieving the last commit using `git log -p -1`.
2.  **Critical Analysis**: Analyze the changes for:
    -   **Correctness & Security**: Logic errors, bugs, or security vulnerabilities.
    -   **Maintainability**: Is the code sustainable for the long term?
    -   **Duplication**: Ensure there is ZERO code duplication.
    -   **Conciseness**: Prioritize self-explanatory code (e.g., descriptive variable/function names, clear structure) over in-file comments. Comments should only be used to explain the *why* of complex logic, not the *what* of the code.
    -   **Programming Style**: Prioritize a functional style over Object-Oriented, and Object-Oriented over Procedural. Focus on long-term, sustainable maintainability. Use Python's list comprehensions, `map`, `filter`, and functional tools (e.g. from `itertools`, `functools`) over procedural for-loops. Use mapping tables over if/else trees. Use ternary operator over verbose if/else.
    -   **Maintainability**: Prioritize zero duplication and high maintainability for humans.
    -   **Consistency**: Inconsistencies with the rest of the codebase.
3.  **Feedback**: Provide a detailed, critical report of your findings. Be firm and thorough in your assessment.

STRICT RULES:
- ONLY perform read-only operations. Do not modify the codebase.
- This is an inquiry ONLY.
- NO duplication of code.
- NO redundant comments.
- Minimal blank lines.
- Concise format.
- Self-explanatory code.
- Functional style.
- Object-Oriented over Procedural.
- Zero duplication.
- High maintainability.
