"""Convierte los [[wikilinks]] de Obsidian a enlaces Markdown normales.

Se ejecuta en CI (GitHub Actions) ANTES de construir la web, sobre la
copia efimera del repo. No modifica tu copia local ni la boveda.

Reglas:
  [[fichero|etiqueta]]  -> [etiqueta](fichero.md)   si fichero.md existe
  [[fichero]]           -> [fichero](fichero.md)    si fichero.md existe
  Si el destino NO existe (p.ej. notas privadas de la boveda que no se
  publican), se sustituye por solo el texto, sin enlace roto.

Uso:  python scripts/wikilinks_to_md.py <carpeta_docs>
"""

import os
import re
import sys

WIKILINK = re.compile(r"\[\[([^\]|]+?)(?:\|([^\]]+?))?\]\]")


def build_index(docs_dir):
    """Mapa: nombre-de-fichero-sin-extension -> ruta relativa a docs_dir."""
    index = {}
    for root, _dirs, files in os.walk(docs_dir):
        for name in files:
            if name.endswith(".md"):
                stem = name[:-3]
                rel = os.path.relpath(os.path.join(root, name), docs_dir)
                index[stem] = rel.replace(os.sep, "/")
    return index


def convert_file(path, index):
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()

    def repl(match):
        target = match.group(1).strip()
        label = (match.group(2) or target).strip()
        # El target puede venir como "carpeta/fichero" o con alias raro;
        # nos quedamos con el nombre base para buscarlo en el indice.
        stem = os.path.basename(target)
        if stem in index:
            return f"[{label}]({index[stem]})"
        # Destino no publicado: dejamos solo el texto (sin enlace roto).
        return label

    new_text = WIKILINK.sub(repl, text)
    if new_text != text:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new_text)


def main():
    if len(sys.argv) != 2:
        print("Uso: python scripts/wikilinks_to_md.py <carpeta_docs>")
        return 1
    docs_dir = sys.argv[1]
    index = build_index(docs_dir)
    for root, _dirs, files in os.walk(docs_dir):
        for name in files:
            if name.endswith(".md"):
                convert_file(os.path.join(root, name), index)
    print(f"Wikilinks convertidos en {docs_dir} ({len(index)} docs indexados).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
