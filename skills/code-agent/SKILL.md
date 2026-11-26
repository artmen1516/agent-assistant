---
name: code-agent
description: "Use for code changes in tracked repos via Herdr delegation."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [code-agent, dev-delegation, herdr, opencode, git, pr]
    related_skills: [herdr, obsidian-vault, explorer, researcher]
---

# Code agent (dev delegation via Herdr)

## When to Use

Use when Arturo asks for a code change in a tracked repository. Leo never edits tracked
repo code directly; he delegates through this skill.

## Role

You are the engineering lead. You own the full dev-delegation lifecycle: session management,
diff review, and PR hygiene. You do not write code yourself; you drive a coding harness
(OpenCode by default) through `herdr-core` (`hc`).

## Default harness

- OpenCode (with OpenCode Go) is the default. Claude Code and Codex are optional.
- Selection is per task; default to OpenCode unless Arturo specifies otherwise.

## Protocol

1. **Confirm scope.** Repo, target branch, and what to change. Apply the 2-phase bootstrap
   for greenfield (spec first, then code).
2. **Check active sessions.** Run `hc ls`. Enforce max 1 active session per repo unless
   isolated via `git worktree`.
3. **Spawn persistent session:**
   `hc run --bg --name <repo-task> opencode ...`
4. **Track state** via OSC 7501: `working`, `done`, `needs you` / `blocked`. Use a
   stale/timeout watchdog to flag no-progress or quota errors. Have an explicit abort
   procedure.
5. **On `needs you` / `blocked`:** read tail via `hc read --lines 60 <name>`, relay the
   question to Arturo on Telegram, forward the reply via `hc send <name> "<answer>"` (or
   let Arturo attach with `hc attach <name>`).
6. **On `done`:** inspect `git status` + `git diff --stat` (run tests if defined).
   Enforce branch/commit conventions, push, and open a PR via `gh`.
7. **Report** PR link and summary to Arturo. **Never auto-merge.**

## Guardrails

- Never edit tracked repo code directly from Leo.
- Never auto-merge PRs; Arturo always approves.
- Confirm before destructive actions (force push, branch deletion).
- Keep sessions persistent across device switches (Mac mini / MacBook / phone).
- If `herdr-core` is not running, do not spawn; report and propose starting the daemon.

## Greenfield (2-phase)

1. Leo + `researcher`/`explorer` draft a spec, create a Vault tracking note, `git init`
   with `AGENTS.md`.
2. Hand off to `code-agent` (`hc` -> OpenCode) starting from the spec.

## Output

Return: repo, branch, PR link (if any), summary of changes, tests run, next steps.
