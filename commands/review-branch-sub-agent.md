---
description: Perform a critical review of all commits in the branch based on origin/HEAD using a sub-agent
---

Perform a critical review of all commits in the current branch based on origin/HEAD.

STRICT RULES:
1. You MUST use the `Task` tool to launch a `general` sub-agent to perform
   this review.
2. Provide the sub-agent with the following prompt: "Pretend to be a code
   reviewer of a pull request including all commits in the current branch
   based on origin/HEAD. Provide a critical review focusing on long-term,
   sustainable maintainability.

   ### Protocol:
   1. **Context Gathering**: Start by retrieving all commits using `git log -p origin/HEAD`.
   2. **Critical Analysis**: Analyze the changes for:
      - **Correctness & Security**: Logic errors, bugs, or security vulnerabilities.
      - **Maintainability**: Is the code sustainable for the long term?
      - **Duplication**: Ensure there is ZERO code duplication.
      - **Conciseness**: Is the code brief, concise, and self-explanatory?
      - **Programming Style**: Prioritize a functional style over Object-Oriented, and Object-Oriented over Procedural.
      - **Consistency**: Inconsistencies with the rest of the codebase.
   3. **Feedback**: Provide a detailed, critical report of your findings. Be firm and thorough in your assessment.

   STRICT RULES:
   - Only read-only operations. Do not modify the codebase."
3. Do NOT run the git commands or perform the analysis in the main session.
4. Report the sub-agent's findings directly to the user.
