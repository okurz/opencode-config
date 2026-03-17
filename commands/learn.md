---
description: Capture a learning or optimization topic and update project or global opencode config, agents, and commands.
---

Adapt opencode and project configurations based on the following learning or optimization topic: $ARGUMENTS

You are tasked with analyzing the provided learning and incorporating it appropriately into the opencode environment. Consider updating any of the following based on the context:
1. **Local Context:** Project-specific `AGENTS.md` or local guidelines.
2. **Global Guidelines:** `~/.config/opencode/AGENTS.md` (e.g., under "Added Memories" or general guidelines).
3. **Global Config:** `~/.config/opencode/opencode.json` (for model, provider, or plugin configurations).
4. **Commands:** `~/.config/opencode/commands/*.md` (for new or updated commands).

**STRICT RULES:**
1. **Analyze Scope:** Determine if the learning applies locally to the current project or globally across all projects. Ask the user if ambiguous.
2. **Verify State:** Always read the current state of a file before applying modifications.
3. **Format Compliance:**
   - Command files must follow the Markdown + YAML frontmatter format.
   - `opencode.json` must remain a valid JSON file.
   - Updates to `AGENTS.md` (local or global) must not remove established constraints unless explicitly requested.
4. **Explain Changes:** Clearly explain the changes being made and their purpose to the user.
5. **Verify Integrity:** After modifications, verify the syntax and integrity of the updated files.
