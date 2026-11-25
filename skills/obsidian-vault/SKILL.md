---
name: obsidian-vault
description: "Use when reading or writing the shared Obsidian vault."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
prerequisites:
  commands: [python3]
metadata:
  hermes:
    tags: [obsidian, vault, notes, ideas, projects, tracking, shared-memory]
    related_skills: [ideas-y-drafts, apple-notes, apple-reminders]
---

# Shared Obsidian vault

## When to Use

Use this skill when reading or writing the shared Obsidian vault: capturing ideas, updating
project status, logging progress, or answering "what's pending". Also use when the user mentions
the vault, Obsidian, or HermesVault.

Single source of truth for notes, ideas and project tracking, shared between Hermes, OpenCode,
herdr -> OpenCode, and Arturo (Mac mini, MacBook, iPhone, iPad).

## Location (resolve, never scan the home dir)

Read `~/Library/Application Support/obsidian/obsidian.json` and take the path of the only vault
entry. Current path:
`/Users/arturomendivil/Library/Mobile Documents/com~apple~CloudDocs/Obsidian/HermesVault`

Obsidian app need not be running: agents read/write the markdown files directly. iCloud syncs
at OS level.

## Structure

- `00-inbox/` - quick capture; process and move to `ideas/` or `projects/`.
- `ideas/` - one note per idea.
- `projects/` - one note per project.
- `daily/` - daily notes `YYYY-MM-DD.md`, link Apple Calendar events.
- `log/` - append-only decisions/progress (`YYYY-MM.md`).
- `templates/` - note templates.
- `attachments/` - images/files.
- `tracking.base` / `ideas.base` - Bases views over the notes above.

## Language

All vault content is in English unless Arturo says otherwise. Apple Notes ideas were migrated
into `ideas/` in English on 2026-11-25.

## Frontmatter (every idea/project note)

```yaml
---
status: Idea | Exploring | Planned | In progress | Blocked | Done | Archived
next: "<first actionable step, or empty>"
due: ""
blockers: ""
owner: Arturo
tags: [idea, <1-3 topic tags>]
---
```

## Agent protocol

1. One note per idea/project; filename = readable English title (kebab-case).
2. Read the note before writing; integrate, do not blindly overwrite (shared, mutable state).
3. Update frontmatter (status, next, due, blockers) before closing a task.
4. Append a dated entry to the note's `## Log` (link commit/PR if applicable).
5. Append global decisions to `log/YYYY-MM.md`.
6. Never delete notes; archive with `status: Archived`.
7. Quick capture goes to `00-inbox/`, process later.

## Boundaries with Apple apps

- Ideas, notes, project tracking -> vault.
- Reminders and calendar -> Apple Reminders / Apple Calendar (do not migrate those; link from daily notes).
- Apple Notes "Ideas" folder is legacy/archive after migration; do not write new ideas there.

## Sync and access

- Vault lives in iCloud Drive (file-level sync) -> readable on iPhone/iPad/MacBook via Obsidian app.
- Mark the folder "Keep Downloaded" in Finder on each Mac so iCloud does not evict files
  (evicted/dataless files cannot be read by the CLI -> "Resource deadlock avoided").
- Remote access to the Mac mini: Tailscale (`mac-mini-m4.iguana-piano.ts.net`) for SSH/screen share;
  Hermes dashboard at `https://mac-mini-m4.iguana-piano.ts.net`.

## Pitfalls

- iCloud eviction: files can become `dataless`; if a read fails with "Resource deadlock avoided",
  open the vault in the Obsidian app to materialize, or mark "Keep Downloaded".
- Folder renames/moves in iCloud cause conflict copies ("Obsidian 2"). Avoid restructuring;
  prefer stable paths. If a conflict copy appears, move its contents into the canonical vault and
  delete the copy.
- Empty folders may not sync; recreate if missing.
- Two sources diverge: write ideas only in the vault, not in Apple Notes.
