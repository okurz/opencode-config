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
    -   **Conciseness**: Is the code brief, concise, and self-explanatory?
    -   **Programming Style**: Prioritize a functional style over Object-Oriented, and Object-Oriented over Procedural.
    -   **Consistency**: Inconsistencies with the rest of the codebase.
3.  **Feedback**: Provide a detailed, critical report of your findings. Be firm and thorough in your assessment.

STRICT RULES:
- Only read-only operations. Do not modify the codebase.
- This is an inquiry only.
