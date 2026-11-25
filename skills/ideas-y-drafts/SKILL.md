---
name: ideas-y-drafts
description: "Use when guardar, recordar o refinar ideas entre sesiones."
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

# Ideas y drafts entre sesiones

**Fuente de verdad única: vault de Obsidian › `ideas/`** (una nota por idea, en inglés). Migrado
desde Apple Notes › `Ideas` el 2026-11-25. Se ve en iPhone/iPad vía Obsidian y no hay que mantener
dos sistemas. Los Recordatorios se retiraron el 2026-11-11 por decisión de Arturo: no crear
recordatorios para ideas. Apple Notes › `Ideas` queda como archivo/legado: no escribir ideas nuevas ahí.

Cada nota lleva en la primera línea `Estado: en curso | pendiente | idea | hecha | descartada`.
Sólo las `en curso` y `pendiente` entran al digest diario; el resto es biblioteca y no genera ruido.

## Guardar una idea → nota en Notes

- Antes de crear, listar los nombres existentes para no duplicar; el usuario puede no recordar si
  la nota ya existe — comprobar siempre, nunca asumir que no:
  `osascript -l JavaScript -e 'const N=Application("Notes"); JSON.stringify(N.folders.byName("Ideas").notes().map(n=>n.name()))'`
- Para escribir o REESCRIBIR notas usa `scripts/rewrite_ideas_notes.py` (JSON → AppleScript
  generado, delete + recreate, verificación final). Editar el body in-place vía AppleScript es
  frágil; recrear con el mismo nombre es lo confiable.
- Al recrear, incluir en `olds` TODAS las variantes de nombre viejo (con y sin acentos, títulos
  renombrados) — si no, quedan notas duplicadas con estados contradictorios y el digest cuenta doble.
- Verificar después con el listado de nombres y largo del `plaintext`; nunca reportar creado solo
  por el OK del comando.

## Guardar un draft largo → Apple Notes

```bash
osascript -e 'tell application "Notes" to make new note at folder "Ideas" with properties {name:"Título", body:"texto" & linefeed & "más texto"}'
```

- La carpeta `Ideas` ya existe en Notes (creada y verificada).
- `body` de Notes se interpreta como **HTML**: para varias líneas hay que mandar
  `<div>párrafo</div>` por línea (y `<div><br></div>` para el espacio). Unir con
  `& linefeed &` NO sirve: Notes colapsa los saltos y deja un solo párrafo.
- Un nota por idea, con encabezados en `<b>` (`Qué es`, `Cómo`, `Primer paso`,
  `Abierto`) — así se lee en iPhone sin abrir el editor.
- Leer de vuelta: `plaintext` de la nota; borrar solo por nombre exacto y confirmar el conteo.
- `memo` también funciona ahora, pero crear nota abre `$EDITOR`; AppleScript acepta el cuerpo.

## Recordar ("qué tengo pendiente")

```bash
python3 ~/.hermes/scripts/ideas-notes.py        # solo en curso / pendientes + primer paso
python3 ~/.hermes/scripts/ideas-notes.py --all  # todas, incluidas idea/hechas
```

Lee Notes vía JXA (`osascript -l JavaScript`) y regresa JSON: no partir nombres por comas,
hay títulos con coma ("nxnative (nativo, no emulador)") y se rompe el conteo.
Silencio = no hay nada activo.

## Partir un dump de ideas en notas

Cuando el usuario pide refinar una nota con muchas ideas sueltas: *una nota por idea*, con
secciones fijas `Qué es · Por qué · Cómo · Primer paso · Abierto`. Investigar lo investigable
(repos, APIs, requisitos) antes de escribir, y cerrar siempre con un primer paso que quepa en
una sesión. La nota original se mueve a la carpeta `Archivo` renombrada, nunca se borra.

## Refinar notas con observaciones del usuario

Cuando Arturo manda observaciones sueltas sobre una idea, van PRIMERO a las notas, no a
construir: su instrucción explícita es refinar las ideas hasta que estén listas y recién después
implementar. Reglas:

- Leer la nota actual antes de escribir; si el usuario duda de si ya existe una nota, checar el
  listado de nombres antes de crear una nueva.
- Verificar contra fuentes reales lo que la nota afirma de terceros (fees de plataformas, APIs y
  sus límites reales, qué aplica en qué OS): `web_search` + `web_extract`, y escribir el dato
  verificado con su fuente, no la suposición. Si una fuente está degradada o cambió, anotarlo en
  la nota con lo que devuelve hoy.
- Marcar dentro de la nota qué quedó decidido y cuándo: secciones `X (decidido <fecha>)` y
  `Estado real en disco (<fecha>)` con datos concretos (paths, commits, conteos medidos). Eso
  distingue una nota mantenida de una al aire.
- Cerrar siempre con `Primer paso` ejecutable en una sesión y `Abierto` con lo que falta decidir;
  ese es el criterio de «lista» vs «en borrador».

- Para armar el monitoreo de vacantes (idea `Búsqueda de trabajo remoto`), partir de
  `references/fuentes-trabajo-remoto.md` — endpoints verificados y filtro de geografía.

## Cerrar una idea

Editar sólo la línea `Estado:` de la nota (`hecha` o `descartada`): sale del digest y el archivo
se queda como historial.

## Recordatorio automático

Cron `dc2b488fca30` ("Ideas (Notes) digest diario"): diario **8:00 am** hora local, `no_agent=True`,
script `ideas-notes.py`, entrega a `telegram:6282750660`.

- Es un cron creado desde sesión CLI: **no** entrega en esa sesión, por eso va a Telegram.
- Sin pendientes el script calla y no se manda nada; `failure_deliver=local` evita que un
  fallo de red llegue al chat.
- Cambiar hora/canal: `cronjob_manage` action=update con `job_id=dc2b488fca30`.

## Pitfalls operativos

- **Notes es estado compartido y mutable.** Otras sesiones de Hermes (o el usuario en iPhone)
  pueden editar la misma nota entre tu turno y el siguiente; lo observado en esta máquina es que
  notas de `Ideas` cambiaron entre sesiones (títulos renombrados, primeros pasos reescritos) sin
  avisar. Antes de escribir, leer la nota actual y el listado de nombres; después de escribir,
  verificar con listado + `plaintext`. No recrear a ciegas: si el nombre ya existe con contenido
  nuevo, integrar en vez de sobrescribir.
- **`Estado:` debe ser la primera línea** para que `ideas-notes.py` lo detecte (regex
  `Estado:\s*([^\n·]+)`); si queda enterrado, la nota no entra al digest.
- **Los nombres con coma rompen el split por ", "** de osascript; usar JXA con `JSON.stringify`
  siempre.

## Legado: carpetas markdown

`~/Notas/Ideas/` (formato con frontmatter `estado:`) sigue existiendo como alternativa
portable, pero **ya no es la fuente de verdad** y el recordatorio ya no la lee. Sirve solo si
el usuario pide explícitamente archivos `.md` (por ejemplo para abrirlos como vault de Obsidian).

## El vault de Obsidian (`HermesVault`) — fuente de verdad (desde 2026-11-25)

Existe un vault real registrado en Obsidian: `HermesVault` en
iCloud Drive, ruta `/Users/arturomendivil/Library/Mobile Documents/com~apple~CloudDocs/HermesVault`.
Ya trae estructura (`00-inbox/`, `ideas/`, `projects/`, `daily/`, `log/`, `templates/`,
`attachments/`), plantillas, plugins Dataview + Notion Bases activos y dos Bases
(`tracking.base` con tabla + kanban por `status`, `ideas.base`), más un README con la convención
de frontmatter para agentes. Resolver la ruta leyendo
`~/Library/Application Support/obsidian/obsidian.json`, nunca escaneando el home.

Migración completada el 2026-11-25: las 16 notas de Apple Notes › `Ideas` se migraron a
`ideas/` del vault (15 notas tras deduplicar un duplicado), traducidas a inglés, con frontmatter
`status / next / due / blockers / owner / tags`. Apple Notes › `Ideas` queda como archivo/legado:
no escribir ideas nuevas ahí. El digest (`ideas-notes.py`) ahora lee el vault.

Reglas vigentes:
- El vault › `ideas/` es la única fuente de verdad para ideas. No escribir ideas en los dos lados.
- Migrar más notas = una nota por idea en `ideas/`, con frontmatter `status / next / due / blockers /
owner / tags`, respetando `status: Archived` en vez de borrar.
- El digest lee el vault (script `~/.hermes/scripts/ideas-notes.py`); actualizar el script si cambia
  la estructura de frontmatter.

## Notion — estado del acceso

`ntn` (CLI oficial) instalado y funcionando en esta Mac, pero sin `NOTION_API_KEY` en
`~/.hermes/.env` no hay acceso. El token lo tiene que pegar el usuario él mismo: por mensajería no
se soporta entrada segura de secretos, así que no pedirle la clave en el chat — darle el comando
`echo 'NOTION_API_KEY=...' >> ~/.hermes/.env` y verificar después con `ntn api v1/users`.

## Alternativas medidas (por si algo deja de funcionar)

- **Apple Notes** (`memo`): `memo notes` se colgó >180s esperando permiso de Automatización, y
  crear nota abre `$EDITOR` (no acepta el contenido como argumento). Solo si el usuario lo pide
  y ya aprobó permisos en pantalla.
- **iCloud Drive**: listar `~/Library/Mobile Documents/com~apple~CloudDocs` también se colgó
  (TCC/materialización). Probar antes de prometer sync a iPhone.
- **Obsidian**: no requiere instalación. `~/Notas` se puede abrir como vault cuando él quiera;
  Hermes trabaja al nivel de archivos.
