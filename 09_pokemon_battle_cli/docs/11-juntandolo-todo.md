---
title: 11 — Juntándolo todo
date: 2026-05-16
tags: [programacion/python, build-things, pokemon-cli, teaching]
type: doc
status: vivo
source: claude-code
---
# 11 — Juntándolo todo

## Por qué importa

Tienes la tabla de tipos, la fórmula de daño y el bucle de batalla. Cada pieza pasa sus tests por separado. Pero un jugador no ejecuta tests: ejecuta `python main.py` y espera ver una batalla. Este documento construye el **punto de entrada** que ata todas las piezas: elegir dos Pokémon, montar la batalla, correrla, anunciar el ganador. Es poco código, pero es donde el proyecto pasa de "componentes correctos" a "programa que se juega".

## Schema / Modelo mental (diagrama ASCII)

Recorrido completo de los datos, desde la definición estática hasta lo que se ve en la terminal:

```
  data.py                pokemon.py / move.py        battle.py            ui.py        terminal
+-----------+           +--------------------+     +------------+      +---------+   +----------+
| 10 Pokémon|           | objetos Pokemon    |     | Battle     |      | mostrar |   | el       |
| definidos |---crea--->| con sus Move       |---->| .run()     |<---->| menús,  |-->| usuario  |
| (stats,   |           | (hp, attack,       |     | bucle de   | pide | leer    |   | ve y     |
|  movs)    |           |  defense, moves)   |     | turnos     | mov. | input   |   | juega    |
+-----------+           +--------------------+     +-----+------+      +---------+   +----------+
                                                         |
                                                         v
                                                  devuelve ganador
                                                         |
                                                         v
                                              main.py imprime el resultado
```

`main.py` es el director de orquesta: no contiene reglas del juego (esas están en `battle.py` y `types.py`), solo decide el orden de las llamadas.

## Qué hace `main.py`, paso a paso

1. **Importar los datos**: traer los 10 Pokémon definidos en `data.py`. Son los objetos ya construidos con sus stats y movimientos.
2. **Elegir dos Pokémon**: uno para el jugador, otro para el rival. Puede ser elección del usuario (vía `ui.py`) o una selección fija/aleatoria para empezar — lo esencial es acabar con dos objetos `Pokemon` distintos.
3. **Crear la batalla**: instanciar `Battle(player, rival)`.
4. **Correr la batalla**: llamar al método que ejecuta el bucle. Devuelve el Pokémon ganador.
5. **Mostrar el resultado**: imprimir quién ganó (directamente o vía una función de `ui.py`).

Ese es todo el trabajo de `main.py`. Si te encuentras escribiendo fórmulas de daño o tablas de tipos aquí, algo se ha colado del sitio equivocado.

## El patrón `if __name__ == "__main__"`

Un archivo Python puede usarse de dos maneras: ejecutarlo directamente (`python main.py`) o importarlo desde otro archivo. Queremos que la batalla arranque solo en el primer caso, no si alguien hace `import main` (por ejemplo, un test). El idioma estándar para eso:

```python
def main():
    ...  # los 5 pasos

if __name__ == "__main__":
    main()
```

Cuando ejecutas el archivo directamente, Python pone la variable especial `__name__` a `"__main__"` y la condición se cumple. Si el archivo se importa, `__name__` vale el nombre del módulo y la batalla NO arranca sola. Esto mantiene el archivo importable sin efectos secundarios.

## Sintaxis Python (al final)

```python
import random

from pokemon.data import ALL_POKEMON          # los 10 Pokémon de data.py
from pokemon.battle import Battle
from pokemon import ui


def main():
    # 1-2. elegir dos Pokémon (aquí: jugador elige, rival al azar)
    player = ui.choose_pokemon(ALL_POKEMON)
    rival = random.choice([p for p in ALL_POKEMON if p is not player])

    # 3. crear la batalla
    battle = Battle(player, rival)

    # 4. correrla
    winner = battle.run()

    # 5. mostrar resultado
    ui.announce_winner(winner)


if __name__ == "__main__":
    main()
```

Notas:
- Los nombres exactos (`ALL_POKEMON`, `ui.choose_pokemon`, `ui.announce_winner`) dependen de cómo definiste `data.py` y `ui.py`; ajústalos a tu implementación. La **estructura** (5 pasos, en orden) es lo invariante.
- `random.choice([p for p in ALL_POKEMON if p is not player])` elige rival distinto del jugador con una comprensión de lista que excluye el ya elegido.
- `main.py` solo orquesta. Toda regla vive en los módulos; toda E/S vive en `ui.py`.

## Gotchas / Anti-patterns (tabla)

| Anti-pattern | Síntoma | Fix |
|---|---|---|
| Lógica de daño/tipos dentro de `main.py` | `main.py` crece, se duplica lógica | Reglas en `battle.py`/`types.py`; `main` solo orquesta |
| `main()` se ejecuta al importar | Tests que hacen `import main` lanzan una batalla | Proteger con `if __name__ == "__main__"` |
| Rival puede ser el mismo objeto que el jugador | Un Pokémon "se pelea consigo mismo" | Excluir al jugador al elegir rival |
| `print` desperdigado por todos los módulos | Imposible cambiar la presentación; difícil de testear | Concentrar la E/S en `ui.py` |
| Imports relativos rotos al ejecutar | `ModuleNotFoundError` según desde dónde lanzas | Ejecutar desde la raíz del proyecto; imports `pokemon.x` |
| `main.py` mezcla `input()` directo | Acopla el flujo a teclado, no testeable | Delegar la entrada a `ui.py` |

## Tu turno

Completa `main.py` con los 5 pasos (importar `data`, elegir 2 Pokémon, crear `Battle`, correrla, mostrar ganador) bajo el guard `if __name__ == "__main__"`.

Comprobaciones de "proyecto terminado":

```
python -m pytest -q
```

Toda la suite (test_types, test_move, test_pokemon, test_battle) debe salir **verde**. Después:

```
python main.py
```

Debe arrancar, dejarte elegir/ver los Pokémon, jugar turnos completos hasta que uno se desmaye, y anunciar el ganador sin lanzar excepciones.

Checklist proyecto terminado:

- [ ] `pokemon/types.py`: `TYPE_CHART` + `effectiveness()` -> `test_types.py` verde
- [ ] `pokemon/move.py`: `Move` con `name, type, power, accuracy, pp, max_pp` -> `test_move.py` verde
- [ ] `pokemon/pokemon.py`: `Pokemon` con `take_damage`, `is_fainted`, `hp = max_hp` inicial -> `test_pokemon.py` verde
- [ ] `pokemon/data.py`: 10 Pokémon definidos
- [ ] `pokemon/battle.py`: `calculate_damage()` + clase `Battle` con el bucle -> `test_battle.py` verde
- [ ] `pokemon/ui.py`: menús y lectura de input separados de la lógica
- [ ] `main.py`: orquesta los 5 pasos bajo el guard `__main__`
- [ ] `python -m pytest -q` -> toda la suite verde
- [ ] `python main.py` -> una batalla completa sin errores

## Conexiones

- [[08-la-tabla-de-tipos]] — `pokemon/types.py`, primera pieza del recorrido de datos.
- [[09-la-formula-de-dano]] — `calculate_damage` en `pokemon/battle.py`.
- [[10-el-bucle-de-batalla]] — clase `Battle`, cuyo ganador `main.py` muestra.
- Rutas futuras: `main.py`, `pokemon/data.py`, `pokemon/ui.py`, `pokemon/battle.py`.
- Tests: `tests/test_types.py`, `tests/test_move.py`, `tests/test_pokemon.py`, `tests/test_battle.py`, `tests/run_tests.py`.

## Resumen mental

> `main.py` es el punto de entrada que ata todas las piezas; no contiene reglas del juego, solo orquesta cinco pasos: (1) importar los 10 Pokémon de `data.py`, (2) elegir dos objetos `Pokemon` distintos (jugador vía `ui.py`, rival con `random.choice` excluyendo al jugador), (3) crear `Battle(player, rival)`, (4) llamar a `run()` que devuelve el ganador, (5) mostrar el resultado vía `ui.py`. Todo va envuelto en `if __name__ == "__main__": main()` para que el archivo sea importable sin lanzar una batalla (clave para los tests). Reglas de arquitectura: la lógica vive en `types.py`/`battle.py`, la E/S en `ui.py`, `main.py` solo decide el orden de llamadas — si escribes una fórmula aquí, está en el sitio equivocado. Anti-patterns: `main()` ejecutándose al importar, rival = jugador, `print`/`input` desperdigados. Proyecto terminado = `python -m pytest -q` toda la suite verde (types, move, pokemon, battle) Y `python main.py` corre una batalla completa hasta el desmayo y anuncia ganador sin excepciones.
