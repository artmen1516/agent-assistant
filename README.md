# agent-assistant

Shared skills, rules, subagents, and conventions for AI agents (Hermes, OpenCode, Claude Code,
Codex, ...).

Install a skill with:

```bash
npx skills add artmen1516/agent-assistant
```

Or install a single skill:

```bash
npx skills add artmen1516/agent-assistant --skill obsidian-vault
```

## Layout

- `skills/` - one folder per skill, each with a `SKILL.md` (npx skills compatible).
- `rules/` - shared rules and conventions for agents.
- `subagents/` - reusable subagent prompts/definitions (planned).

## Skills

- `obsidian-vault` - how to read/write the shared Obsidian vault (notes, ideas, projects, tracking).
- `ideas-y-drafts` - capture, refine, and track ideas across sessions (now backed by the Obsidian vault).
- `hermes-service-maintenance` - maintain Hermes gateway/dashboard launchd services on macOS.

## Rules

- `rules/english-in-vault.md` - vault content is in English unless told otherwise.
- `rules/vault-agent-protocol.md` - how agents update the vault.

## License

MIT
