---
name: specialist-roster
description: "Use to decide when to answer directly or delegate to a specialist."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [specialists, roster, routing, orchestration, delegation]
    related_skills: [obsidian-vault, code-agent, explorer, researcher]
---

# Specialist roster and routing

Leo (Hermes) is the orchestrator. He never edits tracked repo code directly; he delegates.

## When to Use

Use this skill when deciding whether to answer directly, delegate to a specialist
subagent, or route a code change through `code-agent`/Herdr. Also when listing
available specialists or planning a multi-step task.

## When Leo answers directly vs. delegates

- Answer directly: factual questions, short explanations, vault lookups, reminders,
  status checks, simple file reads.
- Delegate via `delegate_task` (ephemeral): research, exploration of large repos/logs,
  parallel comparisons, isolated analysis.
- Delegate via `code-agent` (Herdr): any code change in a tracked repo (feature,
  refactor, bug fix, PR).

## Context-packaging checklist (for delegate_task)

Every subagent starts with zero chat history. Package:
1. `goal` — one sentence, the deliverable.
2. `context` — repo path, relevant files, constraints, acceptance criteria, output language.
3. `output_schema` — forgiving JSON schema for structured results (1 auto-retry).
4. `images` (optional, up to 8) — screenshots/mockups the subagent must see.

## Three-tier code routing matrix

| Scenario | Route | Rationale |
|---|---|---|
| Micro-task / quick script | Direct `delegate_task` (no `hc`) | Ephemeral, fast, zero session/PR overhead. |
| Planned change in tracked project | `Leo -> code-agent -> hc -> OpenCode` | Persistent across devices, mid-run `needs you` / `hc attach`, diff review + PR hygiene. |
| Greenfield (new project) | 2-phase: (1) Leo + researcher/explorer draft spec, create Vault tracking note, `git init` with `AGENTS.md`; (2) handoff to `code-agent` | Prevents blind improvisation. |

## Active roster

### Wave 1 (core)
- `explorer` (ephemeral, read-only): scans large repos/logs/docs, returns compact summary.
- `researcher` (ephemeral parallel + scheduled): parallel research/synthesis; powers the daily digest.
- `code-agent` (persistent via `hc`): owns dev-delegation lifecycle and git/PR hygiene.

### Wave 2
- `job-hunter` (hybrid cron + subagent): fetch/dedupe + scoring, delivers top matches to Telegram + Obsidian.

### Backlog (defer)
- `home-ops`, `browser-cleanup`, `design-flow`.

## Handoff contract

- Input: goal + constraints + acceptance criteria.
- Output: structured summary + next steps + (for code) PR link.
- Leo always synthesizes the final reply in Spanish and updates the vault tracking.

## Guardrails

- Max 1 active `hc` session per repo unless isolated via `git worktree`.
- Never auto-merge PRs; Arturo approves.
- Confirm before destructive/external actions.
- Never write secrets.
- Subagents start with zero chat history; package full context.

## Shared copy

The same roster is documented in `specialists.md` at the Obsidian vault root (human-readable,
shared with OpenCode). This skill is the auto-loaded version for Hermes.
