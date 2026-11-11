---
description: Create a thorough plan in the tasks/ directory using an @explore sub-agent for research
---

Create a detailed execution plan for the following request: $ARGUMENTS

STRICT RULES:
1. First, you MUST use the `Task` tool to launch an `explore` sub-agent with "very thorough" thoroughness to research the codebase and identify relevant files, patterns, and logic related to the request.
2. Use the findings from the sub-agent to inform the creation of the plan.
3. SAVE the final plan as a markdown file in the 'tasks/' directory.
4. Do NOT stage (git add) or commit the new file.
5. Only perform safe file operations and read-only 'git' operations.
