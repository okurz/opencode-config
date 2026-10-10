---
description: Perform a critical review of all commits in the branch based on origin/HEAD, using a reviewer sub-agent by default
---

Perform a critical review of all commits in the current branch based on origin/HEAD.

Reviewer: if $ARGUMENTS contains `reviewer=<agent>`, use that agent as the reviewer; remove the token from the context. Default: `general`. `reviewer=main` performs the review in the main session.

STRICT RULES:
1. If the reviewer is not `main`, you MUST use the `Task` tool to launch the reviewer sub-agent to perform this review. Do NOT run the git commands or perform the analysis in the main session.
2. Provide the reviewer with the following prompt:
   "Pretend to be a code reviewer of a pull request including all commits in the current branch based on origin/HEAD. Provide a critical review focusing on long-term, sustainable maintainability.

   ### Protocol:
   1. **Context Gathering**: Start by retrieving all commits using `git log -p origin/HEAD`.
   2. **Critical Analysis**: Analyze the changes for:
      - **Correctness & Security**: Logic errors, bugs, or security vulnerabilities.
      - **Maintainability**: Is the code sustainable for the long term?
      - **Duplication**: Ensure there is ZERO code duplication.
      - **Conciseness**: Prioritize self-explanatory code (e.g., descriptive variable/function names, clear structure) over in-file comments. Comments should only be used to explain the *why* of complex logic, not the *what* of the code.
      - **Programming Style**: Prioritize a functional style over Object-Oriented, and Object-Oriented over Procedural. Use Python's list comprehensions, `map`, `filter`, and functional tools (e.g. from `itertools`, `functools`) over procedural for-loops. Use mapping tables over if/else trees. Use ternary operator over verbose if/else.
      - **Consistency**: Inconsistencies with the rest of the codebase.
   3. **Feedback**: Provide a detailed, critical report of your findings. For every identified issue, you MUST provide an **Actionable Suggestion Block** optimized for cheaper, faster LLMs (like GPT-4o-mini or Gemini Flash) to apply directly. Each suggestion MUST include:
      - **Target File**: Exact file path.
      - **Reasoning**: A concise description of the issue and why the change is needed.
      - **Actionable SEARCH/REPLACE Block**: An exact search-and-replace block using standard markers (`<<<<<<< SEARCH`, `=======`, `>>>>>>> REPLACE`) containing precise code context, so another model can execute the edit without any complex planning or external search.

   STRICT RULES:
   - ONLY perform read-only operations. Do not modify the codebase.
   - This is an inquiry ONLY.
   - NO duplication of code. NO redundant comments. Minimal blank lines. Concise format."
3. Report the reviewer's findings directly to the user.
