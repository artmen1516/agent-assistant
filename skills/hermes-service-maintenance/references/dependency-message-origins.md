# De dónde sale cada mensaje de dependencias

Mapa mensaje → origen → qué lo dispara → qué hacer. Sirve para responder "¿por qué me sale esto?"
sin adivinar ni instalar paquetes de más. En la instalación Homebrew los catálogos están en
`/opt/homebrew/opt/hermes-agent/share/hermes-agent/locales/` y el código en
`…/libexec/lib/python3.X/site-packages/`.

| Mensaje que ve el usuario | Origen | Disparador | Acción |
|---|---|---|---|
| `Faltan dependencias de voz (PyNaCl / davey). Ejecuta: …` (clave `channel_deps_missing`) | catálogo `es.yaml` | canal con voz (llamadas) activado y `nacl`/`davey` ausentes en el venv del keg | instalar PyNaCl y davey en el venv del keg con el mismo `uv pip install --python /opt/homebrew/opt/hermes-agent/libexec/bin/python …` del resto de extras; sin voz en canales no aplica |
| `The {surface} can't start: {what} are missing from this install. Run `hermes pm install`.` | `hermes_cli/main_dep_hints.py :: missing_optional_deps_message` | sólo dashboard, vía `_require_dashboard_web_deps()`, cuando `fastapi`/`uvicorn` no importan | instalar las web deps o entrar por CLI/gateway; el dashboard no arranca sin ellas |
| `hermes: no dependency environment is committed for this install; run 'hermes pm repair'` | `pm/environments.py`, recuperación temprana (`hermes_cli/_early_recovery.py`) | hueco PM del paquete Homebrew (keg sin `venv/`/`uv.lock`) | es el bug del lanzador PM: ver la sección correspondiente del SKILL.md, no `hermes pm repair` |
| `install out of sync (ffmpeg/npm/ripgrep: not installed or outdated) — this unknown-managed install must rebuild the artifact to fix` | `hermes gateway status` / `pm.install.drift()` | el keg no declara `install-stamp.json` | declarar la instalación como externa/sellada |
| `Plugin <key> declares Python dependencies that are not installed: … run hermes pm repair, then restart Hermes` | `hermes_cli/plugins_loader.py :: _warn_python_dependencies` (`logger.warning`, no pantalla) | manifest de plugin con `python_dependencies` no instaladas | revisar `plugins_entries` del plugin; el aviso sólo va al log |
| `Missing dependency: install with 'python3 -m pip install …'` | scripts de skills (p. ej. `productivity/pdf`) | utilidad de terceros ausente | no es Hermes: se instala en el intérprete que use el script, no en el venv del keg |
| `⚠ a2a (system dependency not met)` / `browser-cdp` / `feishu_*` en `hermes doctor` | gating de tools | falta binario, servicio o key de esa tool | es por-tool y opcional: no explica un aviso de arranque |

## Cómo confirmar en vez de suponer

- La cadena literal del aviso en `es.yaml` / `es.tui.yaml` da la clave; la clave da el módulo.
- `grep -rn "<fragmento del texto>" <site-packages>` localiza el `print`/`logger` que lo emite y
  dice si es pantalla o sólo log.
- Si el mensaje sale en la TUI pero no en `hermes -z`, es de arranque: reproducción en pty (ver
  SKILL.md, paso 3), nunca conclusión por ausencia en los logs.
