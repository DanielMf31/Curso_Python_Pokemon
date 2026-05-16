#!/usr/bin/env bash
#
# setup-macos.sh -- Configuracion para macOS (BEST-EFFORT, no es la via
#                    soportada principal; el curso esta pensado para
#                    Ubuntu/WSL). Usa Homebrew.
#
# Uso (desde Terminal, dentro de la carpeta del proyecto):
#     bash scripts/setup-macos.sh
#
set -euo pipefail

paso()  { echo ""; echo "==> $1"; }
ok()    { echo "    [OK] $1"; }
aviso() { echo "    [AVISO] $1"; }

paso "Comprobando que es macOS..."
if [ "$(uname -s)" != "Darwin" ]; then
    aviso "Esto NO es macOS. En Ubuntu/WSL usa scripts/setup.sh;"
    aviso "en Windows usa windows-setup.bat."
    exit 1
fi
ok "macOS detectado."

paso "Comprobando Homebrew..."
if ! command -v brew >/dev/null 2>&1; then
    aviso "Homebrew no esta instalado. Instalandolo..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # Anade brew al PATH en esta sesion (Apple Silicon e Intel).
    if [ -x /opt/homebrew/bin/brew ]; then eval "$(/opt/homebrew/bin/brew shellenv)"
    elif [ -x /usr/local/bin/brew ]; then eval "$(/usr/local/bin/brew shellenv)"; fi
fi
ok "Homebrew disponible."

paso "Instalando Python y git..."
brew install python git
ok "Python y git instalados."

paso "Instalando Visual Studio Code..."
if command -v code >/dev/null 2>&1; then
    ok "VS Code ya estaba instalado."
else
    brew install --cask visual-studio-code || \
        aviso "No se pudo instalar VS Code; instalalo a mano desde code.visualstudio.com"
fi

paso "Instalando extensiones de Python (si VS Code esta disponible)..."
if command -v code >/dev/null 2>&1; then
    code --install-extension ms-python.python --force || true
    code --install-extension ms-python.vscode-pylance --force || true
    ok "Extensiones procesadas."
else
    aviso "VS Code no disponible en PATH; salto extensiones."
fi

paso "Creando entorno virtual .venv e instalando pytest..."
if [ ! -d ".venv" ]; then python3 -m venv .venv; fi
.venv/bin/pip install --upgrade pip
.venv/bin/pip install pytest
ok "Entorno listo."

echo ""
echo "============================================================"
echo " SETUP macOS COMPLETADO (best-effort)"
echo " Siguiente:  code .   |   python main.py   |   python -m pytest -q"
echo " Empieza por: docs/00-empieza-aqui.md"
echo "============================================================"
