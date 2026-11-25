# agent-skills

Shared skills and rules for AI agents (Hermes, OpenCode, Claude Code, Codex, ...).

Install a skill with:

```bash
npx skills add artmen1516/agent-skills
```

Or install a single skill:

```bash
npx skills add artmen1516/agent-skills --skill obsidian-vault
```

## Layout

- `skills/` - one folder per skill, each with a `SKILL.md` (npx skills compatible).
- `rules/` - shared rules and conventions for agents.

## Skills

- `obsidian-vault` - how to read/write the shared Obsidian vault (notes, ideas, projects, tracking).

## Rules

- `rules/english-in-vault.md` - vault content is in English unless told otherwise.
- `rules/vault-agent-protocol.md` - how agents update the vault.

## License

MIT
