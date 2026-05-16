#!/usr/bin/env bash
#
# bootstrap.sh — Instalador de UN SOLO PASO para el "Curso Python Pokemon".
#
# Para quien no sabe nada de programacion ni de git:
#   1. Entra a la pagina del curso.
#   2. Descarga este fichero (bootstrap.sh) con el navegador.
#   3. Abre una terminal (Ctrl+Alt+T) y escribe:
#
#        bash ~/Descargas/bootstrap.sh
#
#   ...y ya esta. Esto descarga el proyecto e instala todo lo necesario
#   (Python, VS Code, el entorno) en una Ubuntu recien instalada o en
#   Ubuntu dentro de WSL (Windows).
#
# No hace falta saber usar git ni GitHub: este script se encarga.
# ---------------------------------------------------------------------------

set -euo pipefail

REPO_URL="https://github.com/DanielMf31/Curso_Python_Pokemon.git"
# Version a instalar. Por defecto "main". Puedes fijar un tag estable:
#   bash bootstrap.sh v1.0
REF="${1:-main}"
DEST="$HOME/Curso_Python_Pokemon"

# Este instalador es para Ubuntu/Debian (o Ubuntu dentro de WSL).
if ! command -v apt-get >/dev/null 2>&1; then
    echo "Este instalador es para Ubuntu/Debian (o WSL con Ubuntu)."
    echo ""
    echo "  - Windows: descarga y doble clic en  windows-setup.bat"
    echo "  - macOS:   bash scripts/setup-macos.sh"
    echo ""
    echo "Mas info: docs/01-instalar-python-y-terminal.md"
    exit 1
fi

echo ""
echo "==> Paso 1/3: instalando git (necesario para descargar el proyecto)"
sudo apt-get update -y
sudo apt-get install -y git

echo ""
if [ -d "$DEST/.git" ]; then
    echo "==> Paso 2/3: ya existe en $DEST, actualizando"
    git -C "$DEST" fetch --all --tags --prune
    git -C "$DEST" checkout "$REF"
    git -C "$DEST" pull --ff-only origin "$REF" 2>/dev/null || true
else
    echo "==> Paso 2/3: descargando el proyecto en $DEST"
    git clone "$REPO_URL" "$DEST"
    ( cd "$DEST" && git checkout "$REF" ) 2>/dev/null || true
fi

echo ""
echo "==> Paso 3/3: configurando el entorno (Python + VS Code + venv)"
# Entramos en la carpeta de PRACTICA (donde vas a escribir tu codigo).
# setup.sh crea el entorno virtual .venv en esta carpeta.
cd "$DEST/09_pokemon_battle_cli_practica"
bash scripts/setup.sh

echo ""
echo "==========================================================="
echo " LISTO. El proyecto esta en: $DEST"
echo ""
echo " Abrelo en VS Code con:"
echo "     code \"$DEST\""
echo ""
echo " Y empieza leyendo:"
echo "     09_pokemon_battle_cli/docs/00-empieza-aqui.md"
echo "==========================================================="
