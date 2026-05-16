---
title: Curso Python con Pokemon
date: 2026-05-16
tags: [programacion/python, teaching, pokemon-cli]
type: doc
status: vivo
source: claude-code
---

# Curso de Python desde cero, con Pokemon

Aprende a programar en Python **sin saber nada de programacion**,
construyendo paso a paso una **batalla Pokemon que se juega en la
terminal**: tipos y debilidades, movimientos, PP, dano y combate por
turnos.

No necesitas saber usar git, GitHub ni configurar nada.

## Instalacion en un solo paso (Ubuntu)

1. Descarga el instalador:
   **[bootstrap.sh](https://raw.githubusercontent.com/DanielMf31/Curso_Python_Pokemon/main/scripts/bootstrap.sh)**
   (clic derecho -> "Guardar enlace como...").
2. Abre una terminal: tecla `Ctrl` + `Alt` + `T`.
3. Escribe esto y pulsa Enter:

        bash ~/Descargas/bootstrap.sh

Eso descarga el proyecto e instala Python, VS Code y todo lo necesario
en una Ubuntu recien instalada. Cuando termine, te dira como abrirlo.

!!! note "Y si no confias en ejecutar un script a ciegas?"
    Bien pensado. Abre `bootstrap.sh` con un editor de texto y lee lo
    que hace antes de ejecutarlo: son ~50 lineas comentadas en espanol.
    Eso tambien es aprender.

## Como funciona el curso

Hay **dos carpetas**:

- `09_pokemon_battle_cli/` — el **modelo**: el juego completo y
  funcionando. Tu referencia para mirar **solo si te atascas**.
- `09_pokemon_battle_cli_practica/` — la **practica**: la misma
  estructura pero con huecos marcados con `TODO`. Aqui es donde tu
  escribes el codigo.

Abres las dos a la vez en VS Code, lees la teoria aqui, e implementas
en la practica hasta que los tests se pongan en verde.

Empieza por **[Empieza aqui](00-empieza-aqui.md)**.

## Mapa del curso

| Nivel | Tema |
|---|---|
| 01 | Instalar Python y la terminal |
| 02 | Variables y tipos |
| 03 | Estructuras de datos |
| 04 | Condicionales y bucles |
| 05 | Funciones |
| 06 | Clases y objetos |
| 07 | Imports y paquetes |
| 08 | La tabla de tipos |
| 09 | La formula de dano |
| 10 | El bucle de batalla |
| 11 | Juntandolo todo |
| 12 | Extender el proyecto |

Cuando lo tengas todo en verde, en **[Retos](challenges/challenges.md)**
hay extensiones opcionales (guardar partida, equipos, IA mejor...).
