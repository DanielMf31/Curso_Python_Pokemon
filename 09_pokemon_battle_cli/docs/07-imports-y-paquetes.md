---
title: 07 — Imports y paquetes
date: 2026-05-16
tags: [programacion/python, programacion/oop, build-things, pokemon-cli, teaching]
type: doc
status: vivo
source: claude-code
---

# 07 — Imports y paquetes: por qué el código vive en varios ficheros

## Por qué importa

Podrías meter `Move`, `Pokemon`, los 10 Pokémon, la lógica de batalla y la interfaz de texto en un único `main.py` de 800 líneas. Funcionaría. Pero abrirlo sería desesperante: para tocar el daño de un movimiento tendrías que rebuscar entre la pantalla de menús; para añadir un Pokémon, scrollear entre la lógica de turnos. Todo está enredado con todo.

Dividir el proyecto en ficheros pequeños, cada uno con una responsabilidad, hace que puedas razonar sobre una pieza sin tener el resto en la cabeza. Pero en cuanto partes el código, aparece un problema nuevo: `battle.py` necesita la clase `Pokemon`, que ahora vive en *otro* fichero. ¿Cómo accede a ella? La respuesta son los **imports**, y para que funcionen Python necesita que esa colección de ficheros esté organizada como un **paquete**.

Este doc cierra el bloque de fundamentos: ya tienes las clases (doc 06), ahora aprendes a colocarlas en ficheros y a conectarlas.

## Schema / Modelo mental

Tres palabras, tres niveles, sin mezclarlas:

```
   PAQUETE   = carpeta con un fichero __init__.py dentro
   MÓDULO    = un fichero .py individual
   IMPORT    = traer un nombre (clase, función, módulo) desde otro fichero
```

Así está estructurado el proyecto, con las flechas indicando "quién importa de quién":

```
Proyecto_raíz/
│
├── main.py  ───────────────┐  (punto de entrada; se ejecuta con: python main.py)
│                            │
├── pokemon/   ◄── PAQUETE   │
│   ├── __init__.py          │  ← convierte la carpeta en paquete
│   ├── types.py             │     (Normal, Fire, Water, Grass, Electric, Rock)
│   ├── move.py        ◄── MÓDULO  (clase Move)
│   ├── pokemon.py     ◄── MÓDULO  (clase Pokemon)
│   ├── data.py              │     (los 10 Pokémon concretos)
│   ├── battle.py            │     (lógica de combate)
│   └── ui.py                │     (interfaz de texto)
│
└── tests/
    ├── test_move.py
    └── test_pokemon.py

   Dependencias (──► significa "importa de"):

   pokemon.py  ──►  move.py            (un Pokémon tiene una list[Move])
   data.py     ──►  pokemon.py, move.py, types.py
   battle.py   ──►  types.py, pokemon.py
   ui.py       ──►  pokemon.py
   main.py     ──►  data.py, battle.py, ui.py
```

Lee las flechas como dependencias: `main.py` no sabe qué es un `Move`; solo conoce `data.py` (de dónde saca los Pokémon ya montados) y `battle.py` (que pelea). Cada módulo conoce solo lo que necesita. Eso es el beneficio: capas.

## Por qué `__init__.py` convierte una carpeta en paquete

Una carpeta con ficheros `.py` sueltos es solo eso: una carpeta. Python no la trata como una unidad importable hasta que ve un fichero llamado `__init__.py` dentro. Ese fichero es la **señal** "esta carpeta es un paquete; se puede hacer `import pokemon`".

`__init__.py` puede estar **vacío** (y entonces solo cumple su función de marcador), o puede contener código que se ejecuta la primera vez que alguien importa el paquete. Un uso típico es **reexportar** los nombres principales para que la gente escriba imports más cortos:

```python
# pokemon/__init__.py
from pokemon.move import Move
from pokemon.pokemon import Pokemon
```

Con eso, otro fichero puede hacer `from pokemon import Pokemon` directamente, en vez del más largo `from pokemon.pokemon import Pokemon`. El `__init__.py` actúa como la "recepción" del paquete: decide qué se ve desde fuera.

## Las tres formas de importar

Las tres que vas a usar en este proyecto, de la más amplia a la más concreta:

```python
# 1) Importar el módulo entero. Accedes a su contenido con prefijo.
import pokemon.data
charmander = pokemon.data.STARTERS[0]      # hay que escribir el camino completo

# 2) Importar un nombre concreto desde un módulo. Lo usas directo.
from pokemon.move import Move
fire_punch = Move("Fire Punch", "Fire", 75, 100, 15, 15)

# 3) Importar un módulo desde el paquete (lo usas con su nombre corto).
from pokemon import data
charmander = data.STARTERS[0]
```

Forma 2 es la que más usarás: trae exactamente el nombre que necesitas (`Move`, `Pokemon`) y lo dejas listo para usar sin prefijos. Forma 3 es cómoda cuando quieres todo lo de un módulo bajo un nombre corto (`data.algo`, `data.otra_cosa`). Forma 1 es la más verbosa y se usa menos.

Aplicado al proyecto, los imports reales se verán así:

```python
# pokemon/pokemon.py
from pokemon.move import Move          # Pokemon usa Move en sus type hints / moves

# pokemon/battle.py
from pokemon.types import TYPE_CHART   # o como se llame la tabla de tipos
from pokemon.pokemon import Pokemon

# main.py
from pokemon import data
from pokemon.battle import Battle
```

## Cómo y desde dónde se ejecuta

Esto es la fuente nº 1 de confusión con paquetes. Los imports tipo `from pokemon.move import Move` solo funcionan si Python sabe dónde está la carpeta `pokemon/`. Y eso depende de **desde qué directorio lanzas el programa**.

La regla para este proyecto: ejecuta siempre desde la **raíz** (la carpeta que contiene tanto `main.py` como la carpeta `pokemon/`):

```
python main.py
```

Estando en la raíz, Python añade esa carpeta a su ruta de búsqueda. Ve la carpeta `pokemon/`, encuentra su `__init__.py`, y `from pokemon.move import Move` resuelve. Si en cambio te metes *dentro* de `pokemon/` y lanzas `python battle.py`, Python ya no ve el paquete `pokemon` desde fuera y los `from pokemon...` revientan con `ModuleNotFoundError`.

Para los tests, lo mismo: lanza pytest desde la raíz, no desde dentro de `tests/`.

## Sintaxis Python (al final)

```python
import modulo                       # trae el módulo entero  → usar: modulo.cosa
import paquete.modulo               # módulo dentro de paquete → paquete.modulo.cosa
from modulo import Nombre           # trae solo Nombre        → usar: Nombre
from paquete.modulo import Nombre   # idem, desde un paquete
from paquete import modulo          # trae un módulo del paquete → modulo.cosa
from paquete import A, B, C         # varios nombres a la vez
```

Un fichero `.py` se vuelve **paquete-able** poniendo `__init__.py` en su carpeta. El `__init__.py` puede estar vacío o reexportar:

```python
# pokemon/__init__.py
from pokemon.move import Move
from pokemon.pokemon import Pokemon
# ahora desde fuera vale: from pokemon import Move, Pokemon
```

Ejecutar el programa, siempre desde la raíz del proyecto:

```
python main.py
```

## Gotchas / Anti-patterns

| Error | Síntoma | Causa / Fix |
|---|---|---|
| Ejecutar desde la carpeta equivocada | `ModuleNotFoundError: No module named 'pokemon'` | Lanza `python main.py` desde la **raíz**, no desde dentro de `pokemon/` |
| Falta `__init__.py` | `ModuleNotFoundError` o la carpeta no se importa | Asegura que `pokemon/__init__.py` existe (aunque sea vacío) |
| Import circular | `ImportError: cannot import name X (most likely due to a circular import)` | A importa B y B importa A. Rompe el ciclo: mueve lo común a un módulo de más abajo (p. ej. `types.py`) |
| `pokemon.py` choca con el paquete `pokemon/` | Imports ambiguos, comportamiento raro | Por eso la clase va en `pokemon/pokemon.py` (módulo *dentro* del paquete), no en un `pokemon.py` suelto en la raíz |
| `from pokemon import *` | Nombres invisibles, colisiones | Importa explícito lo que usas: `from pokemon.move import Move` |
| Editar import pero no guardar el fichero | El error persiste pese al "arreglo" | Guarda y vuelve a lanzar |

Sobre el **import circular**, el caso a vigilar en este proyecto: si `pokemon.py` importa de `battle.py` y `battle.py` importa de `pokemon.py`, tienes un ciclo. La estructura está diseñada para que las flechas vayan en una sola dirección (`battle.py ──► pokemon.py ──► move.py`, nunca de vuelta). Mantén esa dirección y no habrá ciclos.

## Tu turno

1. Completa **`pokemon/__init__.py`** con las reexportaciones de los nombres principales del paquete (al menos `Move` y `Pokemon`, más lo que el resto de módulos necesite exponer).
2. Asegúrate de que los imports entre módulos siguen la dirección del diagrama (sin ciclos).
3. Verifica que el programa arranca sin errores de import lanzando, **desde la raíz**:

```
python main.py
```

No debe lanzar `ImportError` ni `ModuleNotFoundError`.

Y la batería de tests completa, también desde la raíz:

```
python -m pytest -q
```

Si no tienes pytest, fallback del proyecto: `python run_tests.py`.

## Conexiones

- [[06-clases-y-objetos]] — define `Move` y `Pokemon`, las clases que aquí aprendemos a colocar en módulos e importar.
- [[MOC_Programacion]] — punto de entrada del área.
- Ruta futura: `pokemon/__init__.py` (reexportaciones del paquete), `pokemon/move.py`, `pokemon/pokemon.py`, `pokemon/types.py`, `pokemon/data.py`, `pokemon/battle.py`, `pokemon/ui.py`, `main.py` (raíz).
- Tests: `tests/test_move.py`, `tests/test_pokemon.py` (lánzalos desde la raíz).

## Resumen mental

> Partir el código en ficheros pequeños hace cada pieza razonable por separado, pero obliga a conectarlas con **imports**. Tres conceptos sin mezclar: **paquete** = carpeta con `__init__.py`; **módulo** = un fichero `.py`; **import** = traer un nombre desde otro fichero. La carpeta `pokemon/` es un paquete porque tiene `__init__.py`; ese fichero puede estar vacío o reexportar (`from pokemon.move import Move`) para que desde fuera valga `from pokemon import Move`. Tres formas de importar: `import pokemon.data` (camino completo), `from pokemon.move import Move` (la más usada, nombre directo), `from pokemon import data` (módulo con nombre corto). Las dependencias del proyecto van en una sola dirección (`main ──► data,battle`; `battle ──► types,pokemon`; `pokemon ──► move`) para evitar imports circulares. Ejecuta siempre `python main.py` desde la **raíz**: desde otra carpeta sale `ModuleNotFoundError`. Tests: pytest desde la raíz, o `python run_tests.py` como fallback.
