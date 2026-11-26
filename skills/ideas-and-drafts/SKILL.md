---
name: ideas-and-drafts
description: "Save, recall, or refine ideas across sessions."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
prerequisites:
  commands: [python3]
metadata:
  hermes:
    tags: [notes, ideas, drafts, reminders, cross-session]
    related_skills: [obsidian, apple-notes]
---

# Ideas and drafts across sessions

## When to Use

Use when Arturo wants to capture, recall, or refine an idea or draft across sessions. Backed by the Obsidian vault `ideas/`. Do not use for code changes or project tracking (see `worker-code-agent` / vault projects).

**Single source of truth: Obsidian vault › `ideas/`** (one note per idea, in English). Migrated
from Apple Notes › `Ideas` on 2026-11-25. Viewable on iPhone/iPad via Obsidian; no need to maintain
two systems. Reminders were retired on 2026-11-11 by Arturo's decision: do not create
reminders for ideas. Apple Notes › `Ideas` remains as archive/legacy: do not write new ideas there.

Each idea note carries YAML frontmatter with `status: Idea | Exploring | Planned | Done | Archived`.
(Idea statuses only — `In progress` and `Blocked` belong to projects, not ideas.)
Only `Exploring` and `Planned` ideas enter the daily digest; the rest is library and generates no noise.

## Save an idea → note in Notes

- Before creating, list existing names to avoid duplicates; the user may not remember whether
  the note already exists — always check, never assume it doesn't:
  `osascript -l JavaScript -e 'const N=Application("Notes"); JSON.stringify(N.folders.byName("Ideas").notes().map(n=>n.name()))'`
- To write or REWRITE notes use `scripts/rewrite_ideas_notes.py` (JSON → generated AppleScript,
  delete + recreate, final verification). Editing the body in place via AppleScript is
  fragile; recreating with the same name is reliable.
- When recreating, include in `olds` ALL variants of the old name (with and without accents, renamed
  titles) — otherwise duplicate notes with contradictory states remain and the digest double-counts.
- Verify afterwards with the name listing and `plaintext` length; never report created based only
  on the command's OK.

## Save a long draft → Apple Notes

```bash
osascript -e 'tell application "Notes" to make new note at folder "Ideas" with properties {name:"Title", body:"text" & linefeed & "more text"}'
```

- The `Ideas` folder already exists in Notes (created and verified).
- Notes `body` is interpreted as **HTML**: for multiple lines you must send
  `<div>paragraph</div>` per line (and `<div><br></div>` for the space). Joining with
  `& linefeed &` does NOT work: Notes collapses the breaks into a single paragraph.
- One note per idea, with headings in `<b>` (`Qué es`, `Cómo`, `Primer paso`,
  `Abierto`) — so it reads on iPhone without opening the editor.
- Read back: the note's `plaintext`; delete only by exact name and confirm the count.
- `memo` also works now, but creating a note opens `$EDITOR`; AppleScript accepts the body.

## Recall ("what do I have pending")

```bash
python3 ~/.hermes/scripts/ideas-notes.py        # only in progress / pending + first step
python3 ~/.hermes/scripts/ideas-notes.py --all  # all, including idea/done
```

Reads Notes via JXA (`osascript -l JavaScript`) and returns JSON: do not split names by commas,
titles contain commas ("nxnative (nativo, no emulador)") and the count breaks.
Silence = nothing active.

## Split a dump of ideas into notes

When the user asks to refine a note with many loose ideas: *one note per idea*, with
fixed sections `Qué es · Por qué · Cómo · Primer paso · Abierto`. Research what can be researched
(repos, APIs, requirements) before writing, and always close with a first step that fits in
one session. The original note is moved to the `Archivo` folder renamed, never deleted.

## Refine notes with the user's observations

When Arturo sends loose observations about an idea, they go FIRST into the notes, not into
building: his explicit instruction is to refine ideas until they are ready and only then
implement. Rules:

- Read the current note before writing; if the user doubts whether a note already exists, check
  the name listing before creating a new one.
- Verify against real sources what the note claims about third parties (platform fees, APIs and
  their real limits, what applies on which OS): `web_search` + `web_extract`, and write the
  verified data with its source, not the assumption. If a source is degraded or changed, note it
  in the note with what it returns today.
- Mark inside the note what was decided and when: sections `X (decidido <fecha>)` and
  `Estado real en disco (<fecha>)` with concrete data (paths, commits, measured counts). That
  distinguishes a maintained note from a stale one.
- Always close with an executable `Primer paso` in one session and `Abierto` with what remains
  to decide; that is the criterion for "ready" vs "draft".

- To build the vacancy monitoring, see project `job-search` (migrated from idea
  `remote-job-search-monitoring-report`) and start from `references/fuentes-trabajo-remoto.md`
  (verified endpoints and geography filter) plus `references/job-search-criteria.md`
  (roles, preferences, compensation floors, validation rule).
- Salary floors: never commit a number without market data. Validate with Salary.com (US state),
  Glassdoor/Built In/Levels.fyi (US city/total comp), Glassdoor.ca/Payscale.ca (BC), and
  Talentosy (MX gross monthly). 100k USD was too low for California; raised to $130k base.

## Close an idea

Set the idea's `status` to `Done` (idea fully fleshed out) or `Archived` (dropped or
promoted to a project, with `project: [[projects/<name>]]`). It leaves the digest and the
file stays as history.

## Automatic reminder

Cron `dc2b488fca30` ("Ideas (Notes) daily digest"): daily **8:00 am** local time, `no_agent=True`,
script `ideas-notes.py`, delivered to `telegram:6282750660`.

- It is a cron created from a CLI session: it does **not** deliver in that session, hence Telegram.
- With no pending items the script stays silent and nothing is sent; `failure_deliver=local` keeps a
  network failure from reaching chat.
- Change time/channel: `cronjob_manage` action=update with `job_id=dc2b488fca30`.

## Operational pitfalls

- **Notes is shared, mutable state.** Other Hermes sessions (or the user on iPhone)
  may edit the same note between your turn and the next; what we've observed on this machine is that
  `Ideas` notes changed between sessions (renamed titles, rewritten first steps) without
  notice. Before writing, read the current note and the name listing; after writing, verify with
  listing + `plaintext`. Do not recreate blindly: if the name already exists with new content,
  integrate instead of overwriting.
- **`Estado:` must be the first line** for `ideas-notes.py` to detect it (regex
  `Estado:\\s*([^\\n·]+)`); if buried, the note won't enter the digest.
- **Names with commas break the split by ", "** in osascript; always use JXA with `JSON.stringify`.

## Legacy: markdown folders

`~/Notas/Ideas/` (format with frontmatter `estado:`) still exists as a portable
alternative, but **it is no longer the source of truth** and the reminder no longer reads it. Useful
only if the user explicitly asks for `.md` files (e.g. to open them as an Obsidian vault).

## The Obsidian vault (`HermesVault`) — source of truth (since 2026-11-25)

A real vault registered in Obsidian: `HermesVault`. Resolve the path via
`~/Library/Application Support/obsidian/obsidian.json` (currently the Obsidian app container
`iCloud~md~obsidian/Documents/HermesVault`, NOT iCloud Drive `com~apple~CloudDocs`).
It already has structure (`00-inbox/`, `ideas/`, `projects/`, `daily/`, `log/`, `templates/`,
`attachments/`), templates, Dataview + Notion Bases plugins active and two Bases
(`tracking.base` with table + kanban by `status`, `ideas.base`), plus a README with the
frontmatter convention for agents. Resolve the path by reading
`~/Library/Application Support/obsidian/obsidian.json`, never by scanning home.

Migration completed on 2026-11-25: the 16 Apple Notes › `Ideas` notes were migrated to
the vault's `ideas/` (15 notes after deduplicating a duplicate), translated to English, with frontmatter
`status / next / due / blockers / owner / tags`. Apple Notes › `Ideas` remains as archive/legacy:
do not write new ideas there. The digest (`ideas-notes.py`) now reads the vault.

Current rules:
- The vault › `ideas/` is the only source of truth for ideas. Do not write ideas on both sides.
- Migrating more notes = one note per idea in `ideas/`, with frontmatter `status / next / due / blockers /
owner / tags`, respecting `status: Archived` instead of deleting.
- The digest reads the vault (script `~/.hermes/scripts/ideas-notes.py`); update the script if the
  frontmatter structure changes.

## Notion — access status

`ntn` (official CLI) installed and working on this Mac, but without `NOTION_API_KEY` in
`~/.hermes/.env` there is no access. The user must paste the token themselves: secure secret
entry is not supported over messaging, so don't ask for the key in chat — give them the command
`echo 'NOTION_API_KEY=...' >> ~/.hermes/.env` and verify afterwards with `ntn api v1/users`.

## Measured alternatives (in case something stops working)

- **Apple Notes** (`memo`): `memo notes` hung >180s waiting for Automation permission, and
  creating a note opens `$EDITOR` (doesn't accept content as an argument). Only if the user asks
  and has already approved permissions on screen.
- **iCloud Drive**: listing `~/Library/Mobile Documents/com~apple~CloudDocs` also hung
  (TCC/materialization). Test before promising sync to iPhone.
- **Obsidian**: no installation required. `~/Notas` can be opened as a vault whenever he wants;
  Hermes works at the file level.
