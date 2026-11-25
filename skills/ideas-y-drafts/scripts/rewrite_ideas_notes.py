#!/usr/bin/env python3
"""Reescribe notas de Apple Notes › carpeta 'Ideas' (delete + recreate).

Uso: python3 rewrite_ideas_notes.py notas.json [carpeta]

notas.json es una lista de:
  {"name": "Título",
   "estado": "en curso",
   "paras": ["Qué es", "texto...", "", ...],
   "olds": ["nombres viejos a borrar"],      # opcional
   "headings": ["Qué es", ...]}              # opcional; default HEADINGS_DEFAULT

Un para == "" es línea en blanco; un para que está en headings sale en <b>.
La primera línea de la nota es <b>Estado: <estado></b>.
Verifica al final listando nombres y largos vía JXA (no reportar OK sin esa salida).
"""
import json
import subprocess
import sys

HEADINGS_DEFAULT = {
    "Qué es", "Por qué", "Por qué importa", "Cómo", "Cómo funciona", "Formato",
    "Fuentes", "Fuentes de ideas", "Stack", "Stack candidato", "Pipeline",
    "Primer paso", "Primer paso concreto", "Abierto", "Cuidado", "Plan", "Riesgos",
    "Nicho", "Objetivo", "Preparación", "Estrategia", "Requisitos", "Flujo",
}


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def html_body(estado, paras, headings):
    pieces = ["<div><b>Estado:</b> %s</div><div><br></div>" % estado]
    for p in paras:
        if p == "":
            pieces.append("<div><br></div>")
        elif p in headings:
            pieces.append("<div><b>%s</b></div>" % esc(p))
        else:
            pieces.append("<div>%s</div>" % esc(p))
    return '"%s"' % esc("".join(pieces))


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: rewrite_ideas_notes.py notas.json [carpeta]")
    data = json.load(open(sys.argv[1]))
    folder = sys.argv[2] if len(sys.argv) > 2 else "Ideas"
    lines = ['tell application "Notes"']
    for note in data:
        olds = sorted(set(note.get("olds", []) + [note["name"]]))
        for old in olds:
            lines += ["  try",
                      '    delete (every note of folder "%s" whose name is "%s")'
                      % (esc(folder), esc(old)),
                      "  end try"]
        heads = set(note.get("headings", HEADINGS_DEFAULT))
        lines.append('  make new note at folder "%s" with properties {name:"%s", body:%s}'
                     % (esc(folder), esc(note["name"]),
                        html_body(note["estado"], note["paras"], heads)))
    lines.append("end tell")
    path = "/Users/arturomendivil/.hermes/cache/scratch/rewrite_ideas.applescript"
    open(path, "w").write("\n".join(lines))
    r = subprocess.run(["osascript", path], capture_output=True, text=True)
    print("rewrite rc:", r.returncode, r.stderr.strip()[:300])
    jxa = ('const N=Application("Notes"); JSON.stringify(N.folders.byName("%s")'
           '.notes().map(n=>({name:n.name(), len:n.plaintext().length})))' % esc(folder))
    r2 = subprocess.run(["osascript", "-l", "JavaScript", "-e", jxa],
                        capture_output=True, text=True)
    print(r2.stdout.strip()[:3000])


if __name__ == "__main__":
    main()
