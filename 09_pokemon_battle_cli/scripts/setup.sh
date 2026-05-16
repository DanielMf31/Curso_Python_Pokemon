#!/usr/bin/env bash
#
# setup.sh — Prepara una maquina Ubuntu virgen para el proyecto
#            "Pokemon Battle CLI".
#
# Que hace, en orden:
#   1. Comprueba que estas en Ubuntu o Debian.
#   2. Actualiza la lista de paquetes del sistema.
#   3. Instala Python, herramientas de Python y utilidades base.
#   4. Instala Visual Studio Code (editor de codigo) desde el
#      repositorio oficial de Microsoft. Si falla, prueba con snap.
#   5. Instala las extensiones de Python para VS Code.
#   6. Crea un entorno virtual de Python (.venv) e instala pytest.
#
# Como ejecutarlo (desde una terminal, dentro de la carpeta del proyecto):
#
#     bash scripts/setup.sh
#
# No necesitas saber programar para correr esto. Solo copia el comando.

# "set -e" significa: si cualquier comando falla, el script se detiene
# inmediatamente en lugar de seguir y dejar todo a medias.
set -e

# ---------------------------------------------------------------------------
# Pequenas funciones para imprimir mensajes con un formato consistente.
# ---------------------------------------------------------------------------
paso() {
    echo ""
    echo "==> $1"
}

ok() {
    echo "    [OK] $1"
}

aviso() {
    echo "    [AVISO] $1"
}

# ---------------------------------------------------------------------------
# 1. Comprobar que el sistema operativo es Ubuntu o Debian.
# ---------------------------------------------------------------------------
paso "Comprobando el sistema operativo..."

if [ ! -f /etc/os-release ]; then
    echo "No encuentro /etc/os-release. Este script es para Ubuntu o Debian."
    exit 1
fi

# Leemos el fichero que describe la distribucion de Linux instalada.
. /etc/os-release

if [ "$ID" != "ubuntu" ] && [ "$ID" != "debian" ] \
   && [[ "$ID_LIKE" != *"ubuntu"* ]] && [[ "$ID_LIKE" != *"debian"* ]]; then
    echo "Este script esta pensado para Ubuntu o Debian."
    echo "Detectado: $PRETTY_NAME"
    echo "Puedes seguir los pasos manuales en docs/01-instalar-python-y-terminal.md"
    exit 1
fi

ok "Sistema detectado: $PRETTY_NAME"

# ---------------------------------------------------------------------------
# 2. Actualizar la lista de paquetes disponibles.
# ---------------------------------------------------------------------------
paso "Actualizando la lista de paquetes (sudo apt update)..."
echo "    (Te pedira tu contrasena de usuario. Es normal.)"
sudo apt update
ok "Lista de paquetes actualizada."

# ---------------------------------------------------------------------------
# 3. Instalar Python y utilidades base.
# ---------------------------------------------------------------------------
paso "Instalando Python y herramientas base..."
sudo apt install -y \
    python3 \
    python3-venv \
    python3-pip \
    git \
    curl \
    wget \
    gpg
ok "Python y utilidades instaladas."

# ---------------------------------------------------------------------------
# 4. Instalar Visual Studio Code (el editor donde escribiras el codigo).
# ---------------------------------------------------------------------------
paso "Instalando Visual Studio Code..."

if command -v code >/dev/null 2>&1; then
    ok "VS Code ya estaba instalado. Saltando."
else
    # Intento principal: repositorio oficial de Microsoft.
    # Esto es lo recomendado porque recibe actualizaciones automaticas.
    instalado_code="no"

    if wget -qO- https://packages.microsoft.com/keys/microsoft.asc \
         | gpg --dearmor > /tmp/packages.microsoft.gpg 2>/dev/null; then

        sudo install -D -o root -g root -m 644 \
            /tmp/packages.microsoft.gpg \
            /usr/share/keyrings/packages.microsoft.gpg

        echo "deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" \
            | sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null

        rm -f /tmp/packages.microsoft.gpg

        if sudo apt update && sudo apt install -y code; then
            instalado_code="si"
            ok "VS Code instalado desde el repositorio de Microsoft."
        fi
    fi

    # Plan B: si lo anterior fallo, probamos con snap.
    if [ "$instalado_code" != "si" ]; then
        aviso "Repositorio de Microsoft fallo. Probando con snap..."
        if command -v snap >/dev/null 2>&1; then
            sudo snap install --classic code
            instalado_code="si"
            ok "VS Code instalado mediante snap."
        else
            aviso "No se pudo instalar VS Code automaticamente."
            aviso "Instalalo a mano siguiendo docs/01-instalar-python-y-terminal.md"
        fi
    fi
fi

# ---------------------------------------------------------------------------
# 5. Instalar las extensiones de Python para VS Code.
# ---------------------------------------------------------------------------
if command -v code >/dev/null 2>&1; then
    paso "Instalando extensiones de Python para VS Code..."
    code --install-extension ms-python.python --force || \
        aviso "No se pudo instalar la extension ms-python.python"
    code --install-extension ms-python.vscode-pylance --force || \
        aviso "No se pudo instalar la extension ms-python.vscode-pylance"
    ok "Extensiones de Python procesadas."
else
    aviso "VS Code no esta disponible; salto la instalacion de extensiones."
fi

# ---------------------------------------------------------------------------
# 6. Crear el entorno virtual de Python e instalar pytest.
# ---------------------------------------------------------------------------
paso "Creando el entorno virtual de Python (.venv)..."

if [ -d ".venv" ]; then
    ok "La carpeta .venv ya existia. La reutilizo."
else
    python3 -m venv .venv
    ok "Entorno virtual creado en ./.venv"
fi

paso "Instalando pytest dentro del entorno virtual..."
.venv/bin/pip install --upgrade pip
.venv/bin/pip install pytest
ok "pytest instalado."

# ---------------------------------------------------------------------------
# Bloque final: que hacer ahora.
# ---------------------------------------------------------------------------
echo ""
echo "============================================================"
echo " SETUP COMPLETADO"
echo "============================================================"
echo ""
echo " SIGUIENTES PASOS:"
echo ""
echo " 1. Abrir el proyecto en VS Code:"
echo ""
echo "        code ."
echo ""
echo " 2. Ejecutar el juego:"
echo ""
echo "        python main.py"
echo ""
echo "    (Si 'python' no funciona, usa 'python3 main.py'.)"
echo ""
echo " 3. Correr los tests (para comprobar tu progreso):"
echo ""
echo "        python -m pytest -q"
echo ""
echo "    Si pytest no funciona, usa el plan B sin pytest:"
echo ""
echo "        python tests/run_tests.py"
echo ""
echo " Empieza leyendo:  docs/00-empieza-aqui.md"
echo "============================================================"
echo ""
