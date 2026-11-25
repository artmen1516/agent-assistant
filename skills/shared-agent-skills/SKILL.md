---
name: shared-agent-skills
description: "Manage shared skills across agents and npx skills."
version: 1.0.0
author: Arturo Mendivil (artmen1516), Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [skills, shared, npx-skills, agents, versioning]
    related_skills: [hermes-agent-skill-authoring, obsidian-vault]
---

# Shared agent skills

## When to Use

- User wants skills shared across agents (Hermes, OpenCode, Claude Code, Codex, ...).
- User wants to version/publish skills via a git repo and install with `npx skills add`.
- User asks where global skills should live or how to configure Hermes to read them.
- Don't use for: authoring in-repo skills for the hermes-agent package (see hermes-agent-skill-authoring).

## Layout convention

- Global (user-level) skills live in `~/.agents/skills/<name>/SKILL.md` (the `npx skills` standard).
- Hermes reads them via `skills.external_dirs: ["~/.agents/skills"]` in `~/.hermes/config.yaml`.
- New skills created by Hermes land in `skills.create_dir` (set to `~/.agents/skills` to keep one home).
- A git repo holds the publishable copy; `npx skills add <repo>` installs into `~/.agents/skills/`.

## Repo structure (for npx skills discovery)

```
repo/
  skills/<name>/SKILL.md     # one folder per skill; npx skills add discovers these
  rules/                    # shared rules/conventions (not installed as skills)
  subagents/                # reusable subagent prompts (planned)
  README.md
```

Verified: `npx skills add <path-or-repo> --list` discovers skills under `skills/`.

## Procedure: add a skill to the shared repo

1. Create/edit the skill in `~/.agents/skills/<name>/` (Hermes writes here when create_dir is set).
2. Copy the skill folder into the repo: `cp -r ~/.agents/skills/<name> ~/github/agent-assistant/skills/<name>`.
3. Remove from `~/.hermes/skills/` if duplicated there (to avoid two copies).
4. Update the repo `README.md` skills list.
5. Commit and push.
6. Verify with `npx skills add <repo> --list`.

## Procedure: rename a GitHub repo

`gh repo rename <new-name> --yes` from inside the clone; the remote URL updates automatically.
Rename the local directory to match for clarity.

## Pitfalls

- Folder renames/moves in iCloud cause conflict copies ("Obsidian 2"); avoid restructuring synced folders.
- Keep `~/.hermes/skills/` and `~/.agents/skills/` in sync: a skill in both shows up twice in Hermes.
- `npx skills add` with a local path installs into the project's `.agents/skills/` (creates an `agent/` or `.agents/` dir) — remove that artifact before committing.
- The `npx skills` discovery looks under `skills/` by default; use `--full-depth` to scan deeper.
- Description must be <= 60 chars for Hermes's skill index; npx skills has no such limit but keep it short.
