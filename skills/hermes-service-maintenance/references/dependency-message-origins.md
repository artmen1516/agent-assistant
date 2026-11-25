# Where each dependency message comes from

Message → origin → what triggers it → what to do. Used to answer "why am I seeing this?"
without guessing or installing extra packages. In the Homebrew install the catalogs are in
`/opt/homebrew/opt/hermes-agent/share/hermes-agent/locales/` and the code in
`…/libexec/lib/python3.X/site-packages/`.

| Message the user sees | Origin | Trigger | Action |
|---|---|---|---|
| `Faltan dependencias de voz (PyNaCl / davey). Ejecuta: …` (key `channel_deps_missing`) | catalog `es.yaml` | voice channel (calls) enabled and `nacl`/`davey` missing in the keg's venv | install PyNaCl and davey in the keg's venv with the same `uv pip install --python /opt/homebrew/opt/hermes-agent/libexec/bin/python …` used for the rest of the extras; doesn't apply if no voice in channels |
| `The {surface} can't start: {what} are missing from this install. Run `hermes pm install`.` | `hermes_cli/main_dep_hints.py :: missing_optional_deps_message` | dashboard only, via `_require_dashboard_web_deps()`, when `fastapi`/`uvicorn` don't import | install the web deps or enter via CLI/gateway; the dashboard won't start without them |
| `hermes: no dependency environment is committed for this install; run 'hermes pm repair'` | `pm/environments.py`, early recovery (`hermes_cli/_early_recovery.py`) | PM gap in the Homebrew package (keg without `venv/`/`uv.lock`) | it's the PM launcher bug: see the corresponding section of SKILL.md, not `hermes pm repair` |
| `install out of sync (ffmpeg/npm/ripgrep: not installed or outdated) — this unknown-managed install must rebuild the artifact to fix` | `hermes gateway status` / `pm.install.drift()` | the keg declares no `install-stamp.json` | declare the installation as external/sealed |
| `Plugin <key> declares Python dependencies that are not installed: … run hermes pm repair, then restart Hermes` | `hermes_cli/plugins_loader.py :: _warn_python_dependencies` (`logger.warning`, not screen) | plugin manifest with `python_dependencies` not installed | review the plugin's `plugins_entries`; the notice only goes to the log |
| `Missing dependency: install with 'python3 -m pip install …'` | skill scripts (e.g. `productivity/pdf`) | third-party utility missing | not Hermes: install in the interpreter the script uses, not in the keg's venv |
| `⚠ a2a (system dependency not met)` / `browser-cdp` / `feishu_*` in `hermes doctor` | tool gating | missing binary, service or key for that tool | per-tool and optional: doesn't explain a startup notice |

## How to confirm instead of assuming

- The literal string of the notice in `es.yaml` / `es.tui.yaml` gives the key; the key gives the module.
- `grep -rn "<fragment of the text>" <site-packages>` locates the `print`/`logger` that emits it and
  says whether it's screen or log only.
- If the message appears in the TUI but not in `hermes -z`, it's a startup notice: reproduce in a pty
  (see SKILL.md, step 3), never conclude from its absence in the logs.
