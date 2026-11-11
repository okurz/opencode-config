---
name: customize-opencode
description: Use when editing opencode's own configuration (opencode.jsonc, AGENTS.md, commands, skills, agents, prompts, review files) or the mirrored pi prompts and skills.
---

# Editing opencode's own configuration

## Layout

- `opencode.jsonc`: providers, plugins, permissions, agents. JSONC comments start with `//`.
- `AGENTS.md`: global constraints and agent guidelines, shared with pi through a symlink.
- `commands/<name>.md`: slash prompts; frontmatter `description`, body is the prompt with `$ARGUMENTS`.
- `skills/<name>/SKILL.md`: frontmatter `name` (must equal the directory) and `description` starting with "Use when …". Reusable rules live here; commands stay thin procedures that reference them.
- `agents/<name>.md`: subagents; `prompts/*.txt`: prompts referenced by `agent` entries in `opencode.jsonc`.
- `review-checklist.md`, `review-protocol.md`, `review-learnings.md`: review rules referenced by command prompts.

## Mirroring to pi

`~/.pi/agent/prompts/*.md` mirror `~/.config/opencode/commands/*.md` and `~/.pi/agent/skills/*/SKILL.md` mirror `~/.config/opencode/skills/*/SKILL.md` as the same file. Edit only the opencode side, verify each mirror, and link any missing one:

```
for f in ~/.config/opencode/commands/*.md; do n=$(basename $f); cmp -s $f ~/.pi/agent/prompts/$n || ln -f $f ~/.pi/agent/prompts/$n; done
for f in ~/.config/opencode/skills/*/SKILL.md; do n=$(basename $(dirname $f)); d=~/.pi/agent/skills/$n; mkdir -p $d; cmp -s $f $d/SKILL.md || ln -f $f $d/SKILL.md; done
```

Never edit a `~/.pi/agent` copy as an independent file.

## Validation

- Frontmatter: parse the `---` block with python `yaml.safe_load`; skills need `name` equal to their directory, commands a non-empty `description`.
- `opencode.jsonc`: drop lines whose stripped content starts with `//`, then `json.loads`.
- Skill references (`Load … the <name> skill`) must resolve to an existing `skills/<name>/SKILL.md`; check `grep -rho 'the [a-z-]* skill' ~/.config/opencode/commands | sort -u` against `ls ~/.config/opencode/skills`.
- `~/.config/opencode` and `~/bin` are git repos: commit with the `git-workflow` skill, then run `gitlint`.

## Constraints

Preserve existing `AGENTS.md` constraints unless asked to remove them, never delete config files, and keep commands free of rules duplicated in skills.
