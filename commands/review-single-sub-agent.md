---
description: Perform a critical review of the last commit using a sub-agent
---

Perform a critical review of the last commit.

STRICT RULES:
1. You MUST use the `Task` tool to launch a `general` sub-agent to perform
   this review.
2. Provide the sub-agent with the following prompt: "Pretend to be a code
   reviewer of the last commit. Provide a critical review focusing on
   long-term, sustainable maintainability.

   ### Protocol:
   1. **Context Gathering**: Start by retrieving the last commit using `git log -p -1`.
   2. **Critical Analysis**: Analyze the changes for:
      - **Correctness & Security**: Logic errors, bugs, or security vulnerabilities.
      - **Maintainability**: Is the code sustainable for the long term?
      - **Duplication**: Ensure there is ZERO code duplication.
      - **Conciseness**: Is the code brief, concise, and self-explanatory?
      - **Programming Style**: Prioritize a functional style over Object-Oriented, and Object-Oriented over Procedural.
      - **Consistency**: Inconsistencies with the rest of the codebase.
    3. **Feedback**: Provide a detailed, critical report of your findings. For every identified issue, you MUST provide an **Actionable Suggestion Block** optimized for cheaper, faster LLMs (like GPT-4o-mini or Gemini Flash) to apply directly. Each suggestion MUST include:
       - **Target File**: Exact file path.
       - **Reasoning**: A concise description of the issue and why the change is needed.
       - **Actionable SEARCH/REPLACE Block**: An exact search-and-replace block using standard markers (`<<<<<<< SEARCH`, `=======`, `>>>>>>> REPLACE`) containing precise code context, so another model can execute the edit without any complex planning or external search.

   STRICT RULES:
   - Only read-only operations. Do not modify the codebase."
3. Do NOT run the git commands or perform the analysis in the main session.
4. Report the sub-agent's findings directly to the user.
