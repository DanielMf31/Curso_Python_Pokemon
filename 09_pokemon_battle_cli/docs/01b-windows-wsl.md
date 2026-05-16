---
title: 01b — Windows: instalar el entorno con WSL
date: 2026-05-16
tags: [programacion/python, build-things, pokemon-cli, teaching, windows]
type: doc
status: vivo
source: claude-code
---

# 01b — Windows: instalar el entorno con WSL

## Por que importa

El curso usa Linux (terminal + Python + VS Code). Si tu ordenador es
Windows, **no necesitas borrar nada ni instalar una maquina virtual
pesada**: Windows trae **WSL** (Windows Subsystem for Linux), que te da
un Ubuntu real dentro de Windows con un solo comando. Saltarte este
paso, o intentar hacer el curso en CMD de Windows, te dara errores
constantes porque los comandos del curso son de Linux.

## Schema / Modelo mental

```
   Tu PC con Windows
   ┌─────────────────────────────────────────────┐
   │  Windows                                     │
   │    ├── VS Code (se instala AQUI, en Windows) │
   │    │        │  extension "WSL"               │
   │    │        ▼                                │
   │    └── WSL2 ──> Ubuntu (Linux real)          │
   │                   └── el proyecto + Python   │
   └─────────────────────────────────────────────┘

   Escribes en VS Code (Windows) -> el codigo corre en Ubuntu (WSL)
```

Idea clave: **VS Code vive en Windows; el codigo y Python viven en
Ubuntu/WSL.** Se conectan con la extension "WSL" de VS Code.

## Pasos

1. Descarga del curso el fichero **`windows-setup.bat`** (y la carpeta
   `scripts/` si descargas el ZIP del repo).
2. **Doble clic en `windows-setup.bat`**. Acepta el aviso de
   administrador (es necesario para instalar WSL). Se instala WSL2 +
   Ubuntu solos.
3. **Reinicia** el ordenador si te lo pide.
4. Menu Inicio -> escribe **`Ubuntu`** -> abrelo. La primera vez te
   pide crear usuario y contrasena de Linux.
5. Dentro de esa ventana de Ubuntu, pega:

        curl -fsSL https://raw.githubusercontent.com/DanielMf31/Curso_Python_Pokemon/main/scripts/bootstrap.sh | bash

6. Instala **VS Code en Windows** (https://code.visualstudio.com) y,
   dentro de VS Code, la extension **"WSL"** (de Microsoft). Luego,
   desde la terminal de Ubuntu:  `code .`

## Gotchas / Anti-patterns

| Problema | Causa | Solucion |
|---|---|---|
| Error de "virtualizacion" al instalar WSL | Virtualizacion desactivada en BIOS | Entra a la BIOS, activa Intel VT-x / AMD-V, reintenta |
| `wsl --install` no existe | Windows muy antiguo | Actualiza Windows (10 2004+ u 11) |
| Al escribir la contrasena no se ve nada | Es lo normal en Linux | Escribela igualmente y pulsa Enter |
| Hago el curso en CMD/PowerShell y todo falla | No es Linux | Trabaja SIEMPRE dentro de la terminal de **Ubuntu** |
| `code .` no abre nada | Falta la extension "WSL" | Instala VS Code en Windows + extension "WSL" |

## Tu turno

Tras el paso 5, el `bootstrap.sh` deja el proyecto en
`~/Curso_Python_Pokemon`. Continua en
[00 Empieza aqui](00-empieza-aqui.md) y luego
[01 Instalar Python y terminal](01-instalar-python-y-terminal.md)
(la parte de terminal/venv aplica igual dentro de Ubuntu/WSL).

## Conexiones

- [Inicio](index.md) · [00 Empieza aqui](00-empieza-aqui.md) ·
  [01 Instalar Python y terminal](01-instalar-python-y-terminal.md)
- Scripts: `windows-setup.bat`, `scripts/windows-setup.ps1`,
  `scripts/bootstrap.sh`

## Resumen mental

> En Windows no hace falta VM pesada ni borrar nada: WSL2 da un Ubuntu
> real dentro de Windows. Doble clic en `windows-setup.bat` (admin) ->
> instala WSL2+Ubuntu -> reinicia -> abre "Ubuntu" del menu Inicio ->
> crea usuario/contrasena (no se ve al teclear, normal) -> pega el
> comando `curl ... | bash` que descarga el curso e instala Python y
> entorno. VS Code se instala en Windows con la extension "WSL"; el
> codigo corre en Ubuntu, tu escribes desde VS Code. Trabaja SIEMPRE
> dentro de la terminal de Ubuntu, nunca en CMD. Gotchas tipicos:
> virtualizacion en BIOS, Windows desactualizado, y que la contrasena
> de Linux no se ve mientras la tecleas.
