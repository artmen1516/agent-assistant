# vault-agent-protocol

How agents (Hermes, OpenCode, herdr) operate the shared Obsidian vault.

1. One note per idea/project; filename = readable English title (kebab-case).
2. Read the note before writing; integrate, do not blindly overwrite (shared, mutable state).
3. Update frontmatter (status, next, due, blockers) before closing a task.
4. Append a dated entry to the note's `## Log`.
5. Append global decisions to `log/YYYY-MM.md`.
6. Never delete notes; archive with `status: Archived`.
7. Quick capture goes to `00-inbox/`, process later.
8. Reminders and calendar stay in Apple Reminders / Apple Calendar (link from daily notes).
9. Resolve the vault path via `~/Library/Application Support/obsidian/obsidian.json`.
