---
title: 01 — Instalar Python y la terminal
date: 2026-05-16
tags: [programacion/python, build-things, pokemon-cli, teaching]
type: doc
status: vivo
source: claude-code
---

# Instalar Python y la terminal

Esta doc asume que **nunca has programado** y que estas en una maquina
con **Ubuntu** (un tipo de Linux). Vamos despacio. Al final tendras el
ordenador listo para escribir tu primer codigo. No hace falta entender
todo a la primera; basta con seguir los pasos.

## Por que importa

Antes de escribir codigo necesitas tres cosas: un sitio donde dar
ordenes al ordenador (la **terminal**), el lenguaje en el que vas a
programar (**Python**) y un sitio comodo para escribir el codigo (el
**editor**). Si esto no esta bien montado, nada del resto del proyecto
funcionara. Es como querer cocinar sin cocina.

## Schema / Modelo mental

Cuatro palabras nuevas. Aqui esta lo que significan y como se conectan:

```
   +-----------------------------------------------------+
   |  TU ORDENADOR (la maquina, con Ubuntu)              |
   |                                                     |
   |   +---------------------------------------------+   |
   |   |  TERMINAL                                   |   |
   |   |  Una ventana negra donde ESCRIBES ordenes   |   |
   |   |  con el teclado en vez de hacer clic.       |   |
   |   |                                             |   |
   |   |     escribes:  python main.py               |   |
   |   |          |                                  |   |
   |   |          v                                  |   |
   |   |   +-------------------------------------+   |   |
   |   |   |  PYTHON                             |   |   |
   |   |   |  El programa que entiende el        |   |   |
   |   |   |  lenguaje en el que programaras.    |   |   |
   |   |   |  Lee tu codigo y lo ejecuta.        |   |   |
   |   |   |          |                          |   |   |
   |   |   |          v                          |   |   |
   |   |   |   +-----------------------------+   |   |   |
   |   |   |   |  TU PROYECTO                |   |   |   |
   |   |   |   |  La carpeta con el juego.   |   |   |   |
   |   |   |   |  Lo escribes en el EDITOR   |   |   |   |
   |   |   |   |  (VS Code).                 |   |   |   |
   |   |   |   +-----------------------------+   |   |   |
   |   |   +-------------------------------------+   |   |
   |   +---------------------------------------------+   |
   +-----------------------------------------------------+
```

Definiciones en una frase:

- **Terminal**: ventana donde le das ordenes al ordenador escribiendo.
- **Python**: el lenguaje de programacion y el programa que lo ejecuta.
- **Editor (VS Code)**: el "Word" de los programadores; ahi escribes.
- **Entorno virtual (.venv)**: una caja aislada para que las
  herramientas de este proyecto no se mezclen con el resto del sistema.
  No te preocupes ahora por entenderlo del todo; `setup.sh` lo crea solo.

## Pasos

### Paso 1 — Abrir la terminal

Pulsa a la vez estas tres teclas:

```
Ctrl  +  Alt  +  T
```

Se abre una ventana (normalmente oscura) con texto y un cursor
parpadeando. Eso es la terminal. **Todo lo que pongamos "en la terminal"
se escribe ahi y se confirma pulsando Enter.**

### Paso 2 — Conseguir el proyecto

Si te han dado el proyecto en una carpeta (USB, descarga, etc.),
muevete a ella. Por ejemplo, si esta en tu carpeta personal dentro de
`pokemon_battle`:

```bash
cd ~/pokemon_battle/09_pokemon_battle_cli
```

`cd` significa "change directory" (cambiar de carpeta). El simbolo `~`
es un atajo para tu carpeta personal. Para ver donde estas:

```bash
pwd
```

Para listar lo que hay en la carpeta actual:

```bash
ls
```

Deberias ver, entre otras cosas, `main.py`, `scripts`, `docs`.

### Paso 3 — Ejecutar el script de preparacion

Este comando deja el ordenador listo (instala Python, el editor, etc.).
Escribelo tal cual:

```bash
bash scripts/setup.sh
```

Que va a pasar, paso a paso, mientras se ejecuta:

1. Comprueba que estas en Ubuntu/Debian.
2. **Te pedira tu contrasena** (la del usuario del ordenador). Es
   normal y seguro: la necesita para instalar programas. Al teclearla
   **no se ve nada en pantalla** (ni asteriscos); escribela "a ciegas"
   y pulsa Enter.
3. Actualiza la lista de programas disponibles.
4. Instala Python y utilidades.
5. Instala VS Code (el editor).
6. Instala las extensiones de Python para VS Code.
7. Crea la caja aislada `.venv` e instala la herramienta de tests.

Tarda unos minutos. Cuando termine veras un bloque grande que dice
`SETUP COMPLETADO` con los siguientes pasos.

### Paso 4 — Verificar que todo se instalo

Comprueba que Python esta:

```bash
python3 --version
```

Debe responder algo como `Python 3.10.12` (el numero puede variar).

Comprueba que VS Code esta:

```bash
code --version
```

Debe responder con unas lineas de version. Si responde
"command not found", mira la seccion "Si el script falla" al final.

### Paso 5 — Abrir el proyecto en VS Code

Estando dentro de la carpeta del proyecto:

```bash
code .
```

El punto `.` significa "la carpeta actual". Se abre VS Code mostrando
todos los ficheros del proyecto a la izquierda.

### Paso 6 — Ejecutar el juego

Dentro de VS Code abre una terminal con el menu
`Terminal -> New Terminal` y escribe:

```bash
python main.py
```

Si `python` no existe, prueba con `python3 main.py`. Veras el juego
arrancar en texto. (En la practica al principio dara errores: es lo
esperado, todavia no has rellenado el codigo.)

### Paso 7 — Correr los tests

```bash
python -m pytest -q
```

Esto te dice cuanto codigo funciona ya. En el modelo todo pasa; en la
practica casi todo falla hasta que lo rellenes. Eso es normal y bueno:
es tu lista de tareas.

## Sintaxis / comandos (al final)

| Comando                   | Que hace                                  |
|---------------------------|-------------------------------------------|
| `Ctrl + Alt + T`          | Abrir la terminal                         |
| `pwd`                     | Ver en que carpeta estoy                  |
| `ls`                      | Listar ficheros de la carpeta actual      |
| `cd carpeta`              | Entrar en una carpeta                     |
| `cd ..`                   | Subir a la carpeta de arriba              |
| `bash scripts/setup.sh`   | Preparar el ordenador (una sola vez)      |
| `python3 --version`       | Comprobar que Python esta instalado       |
| `code --version`          | Comprobar que VS Code esta instalado      |
| `code .`                  | Abrir la carpeta actual en VS Code        |
| `python main.py`          | Ejecutar el juego                         |
| `python -m pytest -q`     | Correr los tests                          |

## Gotchas / Anti-patterns

| Anti-patron                                  | Que hacer en su lugar                         |
|----------------------------------------------|-----------------------------------------------|
| Esperar ver la contrasena al escribirla      | No se ve; teclea a ciegas y pulsa Enter       |
| Usar `python` cuando no existe en el sistema | Prueba `python3` en su lugar                  |
| Ejecutar `setup.sh` fuera de la carpeta      | Haz `cd` a la carpeta del proyecto primero    |
| Cerrar la terminal a mitad del setup         | Dejalo terminar; tarda unos minutos           |
| Asustarse por tests en rojo en la practica   | Es lo esperado: son tu lista de tareas        |

## Si el script falla: pasos manuales

Si `bash scripts/setup.sh` da error, hazlo a mano, comando a comando:

```bash
# 1. Actualizar paquetes
sudo apt update

# 2. Instalar Python y utilidades
sudo apt install -y python3 python3-venv python3-pip git curl wget gpg

# 3. Instalar VS Code (repositorio oficial de Microsoft)
wget -qO- https://packages.microsoft.com/keys/microsoft.asc \
  | gpg --dearmor > /tmp/packages.microsoft.gpg
sudo install -D -o root -g root -m 644 /tmp/packages.microsoft.gpg \
  /usr/share/keyrings/packages.microsoft.gpg
echo "deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" \
  | sudo tee /etc/apt/sources.list.d/vscode.list
sudo apt update
sudo apt install -y code

# 3-bis. Si lo de arriba falla, alternativa con snap:
sudo snap install --classic code

# 4. Extensiones de Python para VS Code
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance

# 5. Crear la caja aislada e instalar pytest
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install pytest
```

## Tu turno

1. Abre la terminal con `Ctrl + Alt + T`.
2. Entra en la carpeta del proyecto con `cd`.
3. Ejecuta: `bash scripts/setup.sh`
4. Verifica con: `python3 --version` y `code --version`
5. Abre el proyecto: `code .`
6. Pasa a la siguiente doc: `docs/02-...` (variables).

## Conexiones

- Anterior: [[00-empieza-aqui]]
- Mapa de niveles: [[PHASES]]
- Script que ejecutas: `09_pokemon_battle_cli/scripts/setup.sh`
- Codigo que abriras pronto: `09_pokemon_battle_cli_practica/main.py`

## Resumen mental

> Para programar necesitas cuatro cosas y ya sabes que son: la
> **terminal** (ventana donde escribes ordenes, se abre con
> Ctrl+Alt+T), **Python** (el lenguaje que ejecuta tu codigo), el
> **editor** VS Code (donde escribes comodo) y el **entorno virtual**
> `.venv` (una caja aislada que crea el script por ti). El flujo es:
> abres terminal, entras a la carpeta del proyecto con `cd`, ejecutas
> `bash scripts/setup.sh` (te pedira la contrasena, que no se ve al
> teclear: es normal). El script instala todo. Verificas con
> `python3 --version` y `code --version`. Abres el proyecto con
> `code .`, ejecutas el juego con `python main.py` y miras tu progreso
> con `python -m pytest -q`. En la practica casi todo falla al
> principio: eso es bueno, es tu lista de tareas. Si el script falla,
> hay una seccion con los pasos manuales uno a uno.
