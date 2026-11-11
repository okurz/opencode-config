---
description: Adapt opencode's own configuration, commands, and agent guidelines.
---

Adapt opencode based on the following request: $ARGUMENTS

You are being asked to modify opencode's own environment. This includes:
- Main configuration: `opencode.json` (plugins, providers, models)
- Global agent instructions: `AGENTS.md`
- Command definitions: `commands/*.md`

STRICT RULES:
1.  Verify the current state of any file before applying modifications.
2.  Maintain consistency with existing settings and style.
3.  If adding or modifying a command, ensure it follows the Markdown + YAML frontmatter format.
4.  If modifying `opencode.json`, ensure it remains a valid JSON file.
5.  If modifying `AGENTS.md`, ensure it stays aligned with its original purpose as a source of global guidelines.
6.  Explain the changes being made and their purpose to the user.
7.  NEVER remove established constraints in `AGENTS.md` unless explicitly requested by the user.
8.  After modifications, verify the integrity of the updated files.
