---
title: 09 Pokemon Battle CLI Practica — scaffolding
date: 2026-05-16
tags: [programacion/python, build-things, pokemon-cli, teaching, practica]
type: proyecto
status: vivo
source: claude-code
---

# 09 · Pokemon Battle CLI PRACTICA

> Practica del juego de batalla Pokemon por terminal. Estructura
> montada, scaffolding con huecos `TODO`. Aqui es donde **tu tecleas**.
> El modelo (mismo juego ya funcionando) esta en
> `../09_pokemon_battle_cli/`.

## El patron: modelo + practica

Hay dos carpetas gemelas:

- **Modelo** (`../09_pokemon_battle_cli/`): el juego terminado. Solo lo
  **miras** cuando te atascas. No lo tocas.
- **Practica** (esta carpeta): el mismo juego con huecos. Aqui
  **escribes**. Tu objetivo es rellenar los `TODO` hasta que todos los
  tests pasen y el juego sea jugable.

No copies el modelo a ciegas: leelo, entiende por que funciona, y luego
escribe tu version aqui con tus dedos. Asi se aprende; copiando no.

## Las 4 categorias de scaffolding

| Cat | Estado | Que es | Archivos |
|---|---|---|---|
| **A — Setup/infra** | completo | Ya hecho, no se reescribe (no es pedagogico) | `scripts/setup.sh`, `pokemon/__init__.py`, `README.md`, `main.py` (cableado), `pokemon/ui.py`, `tests/run_tests.py`, `pokemon/data.py` (2 Pokemon completos + 8 marcados `TODO`) |
| **B — Skeleton + TODO** | por implementar | Firmas + docstrings + `raise NotImplementedError` + pistas. **Aqui escribes tu** | `pokemon/types.py`, `pokemon/move.py`, `pokemon/pokemon.py`, `pokemon/battle.py` |
| **C — Tests como spec** | completo (rojos hasta que B este hecho) | Identicos a los del modelo. Pasan de rojo a verde segun rellenas B | `tests/test_types.py`, `tests/test_move.py`, `tests/test_pokemon.py`, `tests/test_battle.py` |
| **D — Challenges** | completo | Retos opcionales para ir mas alla | seccion de challenges en las docs |

## Workflow (split-view)

```
  +---------------------------+---------------------------+
  |  IZQUIERDA: la PRACTICA   |  DERECHA: el MODELO        |
  |  esta carpeta             |  ../09_pokemon_battle_cli/ |
  |  AQUI ESCRIBES            |  AQUI SOLO MIRAS           |
  +---------------------------+---------------------------+
```

```bash
# 1 · preparar el ordenador (solo la primera vez)
bash scripts/setup.sh

# 2 · abrir en VS Code y poner las dos carpetas en split-view
code .

# 3 · iterar nivel a nivel (ver ../09_pokemon_battle_cli/PHASES.md):
#     a) lee la doc del nivel
#     b) rellena el TODO del fichero que indica
#     c) corre los tests:
python -m pytest -q
#        (plan B sin pytest:)
python tests/run_tests.py
#     d) cuando el "gate" del nivel esta verde -> siguiente nivel
```

## Orden recomendado

Sigue los niveles **0 -> 10** de
`../09_pokemon_battle_cli/PHASES.md`. Cada nivel introduce un concepto,
te dice que fichero rellenar y cual es su test-gate. No pases de nivel
con el gate en rojo.

Resumen del recorrido:

1. Niveles 0-1: entorno y variables (lees, todavia no escribes mucho).
2. Niveles 2-4: estructuras, condicionales/bucles, funciones.
3. Nivel 5-6: clases e imports/paquetes.
4. Nivel 7: `pokemon/types.py` (tabla de tipos).
5. Nivel 8: `pokemon/move.py` + formula de danio en `pokemon/pokemon.py`.
6. Nivel 9: `pokemon/battle.py` (bucle de batalla).
7. Nivel 10: juntar todo; `python main.py` debe dar una batalla
   completa de principio a fin.

## Criterio de terminado

Has terminado cuando se cumplen **las dos cosas**:

1. Todos los tests en verde:

   ```bash
   python -m pytest -q     # (o: python tests/run_tests.py)
   ```

2. El juego se juega entero sin errores:

   ```bash
   python main.py
   # eliges Pokemon, eliges movimientos por turnos,
   # y la batalla termina con un ganador.
   ```

## Workflow real de SWE

Esto replica como se trabaja de verdad en software: **lees codigo que ya
existe (el modelo), identificas que falta, y escribes la parte nueva que
encaja**. Casi nunca escribes desde cero: extiendes lo que hay. Esta
practica entrena exactamente eso desde el primer dia.

## Convenciones de la boveda

Este proyecto vive en `50_Areas/Programacion/Build_Things/`. Sigue las
convenciones de [[CLAUDE]] raiz.
