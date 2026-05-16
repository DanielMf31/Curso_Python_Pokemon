---
title: 09 Pokemon Battle CLI — modelo
date: 2026-05-16
tags: [programacion/python, build-things, pokemon-cli, teaching]
type: proyecto
status: vivo
source: claude-code
---

# 09 · Pokemon Battle CLI (modelo)

> Juego de batalla Pokemon por terminal, en Python puro (solo libreria
> estandar). Este es el **modelo**: el codigo completo y funcionando.
> Pensado para aprender a programar desde **cero absoluto**.

## Schema (1 minuto)

```
   data.py           types.py
   (10 Pokemon)      (tabla de ventajas)
       |                  |
       v                  v
   +---------+        +--------+
   | Pokemon |  usa-> |  Move  |
   |  hp,lvl |        | power  |
   +----+----+        +----+---+
        |                  |
        +--------+---------+
                 v
            +---------+
            | Battle  |  turnos, danio, KO
            +----+----+
                 |
                 v
            +---------+
            |   ui.py |  texto en la TERMINAL
            +---------+
                 |
                 v
              main.py  (arranca el juego)
```

El jugador elige movimientos escribiendo en la terminal; `Battle`
calcula el danio usando la tabla de tipos y la formula; `ui.py` lo
muestra como texto. No hay graficos: todo es entrada/salida de texto.

## Quick start

```bash
# 1 · preparar el ordenador (solo la primera vez)
bash scripts/setup.sh

# 2 · jugar
python main.py

# 3 · correr los tests
python -m pytest -q
#    (plan B sin pytest:)
python tests/run_tests.py
```

## Estructura

```
09_pokemon_battle_cli/
  main.py              <- arranca el juego
  scripts/
    setup.sh           <- prepara la maquina (Python, VS Code, venv)
  pokemon/
    __init__.py        <- marca la carpeta como paquete importable
    types.py           <- los 6 tipos y la tabla de ventajas
    move.py            <- clase Move (un ataque)
    pokemon.py          <- clase Pokemon (hp, nivel, ataques)
    data.py            <- los 10 Pokemon predefinidos
    battle.py          <- logica de la batalla (turnos, danio)
    ui.py              <- todo lo que se imprime/lee por terminal
  tests/
    test_types.py
    test_move.py
    test_pokemon.py
    test_battle.py
    run_tests.py       <- corre los tests sin necesitar pytest
  docs/
    00-empieza-aqui.md
    01-instalar-python-y-terminal.md
    ...                <- una doc por nivel (hasta la 12)
  PHASES.md            <- mapa de los 11 niveles (0 -> 10)
```

Tipos del juego: Normal, Fire, Water, Grass, Electric, Rock.
Pokemon: Charmander, Squirtle, Bulbasaur, Pikachu, Geodude, Rattata,
Charizard, Blastoise, Venusaur, Raichu.

## Roadmap

El proyecto se aprende en **11 niveles**, del 0 (preparar entorno) al 10
(juntar todo en un juego jugable). Cada nivel introduce un concepto de
Python, te dice que fichero implementar y tiene un "gate": un test que
debe ponerse verde antes de pasar al siguiente nivel.

- Mapa completo de niveles: [[PHASES]]
- Por donde empezar: [[00-empieza-aqui]]

## Para quien es

Para alguien que **no ha programado nunca**. No se asume ningun
conocimiento previo: ni de terminal, ni de Python, ni de programacion.
Si sabes encender el ordenador, puedes empezar. Aprenderas escribiendo
codigo de verdad y comprobandolo con tests, no viendo videos.

## Convenciones de la boveda

Este proyecto vive en `50_Areas/Programacion/Build_Things/`. Sigue las
convenciones de [[CLAUDE]] raiz.
