#!/usr/bin/env python3
"""Rewrite notes in Apple Notes › folder 'Ideas' (delete + recreate).

Usage: python3 rewrite_ideas_notes.py notes.json [folder]

notes.json is a list of:
  {"name": "Title",
   "estado": "en curso",
   "paras": ["Qué es", "text...", "", ...],
   "olds": ["old names to delete"],      # optional
   "headings": ["Qué es", ...]}              # optional; default HEADINGS_DEFAULT

A para == "" is a blank line; a para that is in headings is rendered in <b>.
The first line of the note is <b>Estado: <estado></b>.
Verify at the end by listing names and lengths via JXA (do not report OK without that output).
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
        sys.exit("usage: rewrite_ideas_notes.py notas.json [folder]")
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
