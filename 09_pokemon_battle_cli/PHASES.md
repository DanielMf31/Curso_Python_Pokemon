---
title: 09 Pokemon Battle CLI — PHASES (mapa de niveles)
date: 2026-05-16
tags: [programacion/python, build-things, pokemon-cli, teaching]
type: doc
status: vivo
source: claude-code
---

# PHASES — mapa de los 11 niveles

Aprendes el proyecto en **11 niveles**, del 0 al 10. Cada nivel:

1. Introduce **un concepto** de Python nuevo (de menos a mas).
2. Te dice **que fichero(s)** implementar en la carpeta de practica.
3. Tiene un **gate**: un test que debe ponerse **verde** antes de pasar
   al siguiente nivel.

> Regla inquebrantable: **no se pasa de nivel sin el gate en verde.**
> Si el test falla, ese concepto aun no esta dominado. Quedate ahi.

Como correr el gate de cada nivel:

```bash
python -m pytest -q                 # todos los tests
python -m pytest tests/test_types.py -q   # solo uno (ejemplo)
python tests/run_tests.py           # plan B sin pytest
```

## Tabla de niveles

| Nivel | Concepto que aprendes | Doc | Fichero(s) que implementas | Gate (test que debe estar verde) |
|---|---|---|---|---|
| 0 | Entorno: terminal, Python, editor, venv | `docs/01-instalar-python-y-terminal.md` | (nada de codigo) Preparar la maquina | `python3 --version` y `code --version` responden bien |
| 1 | Variables y tipos basicos (texto, numeros) | `docs/02-variables.md` | Lectura guiada sobre `pokemon/data.py` | Leer y entender; sin test (se valida en niveles siguientes) |
| 2 | Estructuras de datos (listas, diccionarios) | `docs/03-estructuras.md` | Completar entradas de datos en `pokemon/data.py` | `python -c "from pokemon.data import POKEDEX; print(len(POKEDEX))"` da 10 |
| 3 | Condicionales y bucles (`if`, `for`, `while`) | `docs/04-condicionales-bucles.md` | Logica de recorrido en `pokemon/data.py` (busqueda) | `tests/test_pokemon.py` (parte de lookup) verde |
| 4 | Funciones (definir, parametros, `return`) | `docs/05-funciones.md` | Funciones auxiliares en `pokemon/move.py` | `tests/test_move.py` verde |
| 5 | Clases y objetos (atributos, metodos) | `docs/06-clases.md` | Clase `Pokemon` en `pokemon/pokemon.py` | `tests/test_pokemon.py` verde |
| 6 | Imports y paquetes (`__init__.py`, `from ... import`) | `docs/07-imports-paquetes.md` | Conectar imports entre `pokemon/*.py` | `python -c "import pokemon"` sin error |
| 7 | Tabla de tipos (datos + acceso) | `docs/08-tabla-tipos.md` | `pokemon/types.py` (los 6 tipos + ventajas) | `tests/test_types.py` verde |
| 8 | Formula de danio (aritmetica + multiplicadores) | `docs/09-formula-danio.md` | Calculo de danio en `pokemon/pokemon.py` / `pokemon/move.py` | `tests/test_pokemon.py` (parte de danio) verde |
| 9 | Bucle de batalla (estado, turnos, fin) | `docs/10-bucle-batalla.md` | `pokemon/battle.py` (turnos hasta KO) | `tests/test_battle.py` verde |
| 10 | Juntar todo (programa jugable end-to-end) | `docs/11-juntar-todo.md` | Cableado final en `main.py` (usa `pokemon/ui.py`) | **Todos** los tests verdes **y** `python main.py` da una batalla completa |

## Tipos y Pokemon del juego (referencia)

- **Tipos (6):** Normal, Fire, Water, Grass, Electric, Rock.
- **Pokemon (10):** Charmander (Fire), Squirtle (Water),
  Bulbasaur (Grass), Pikachu (Electric), Geodude (Rock),
  Rattata (Normal), Charizard (Fire), Blastoise (Water),
  Venusaur (Grass), Raichu (Electric).

## Estado de salida (lo que significa cada resultado)

| Resultado del gate | Que significa | Que hacer |
|---|---|---|
| `passed` (verde) | El concepto del nivel funciona | Pasa al siguiente nivel |
| `failed` (rojo) | Aun falta o esta mal | Lee el error, corrige, vuelve a correr |
| `error` al importar | Falta un fichero o un import | Revisa la doc del nivel 6 (imports) |

## Conexiones

- Empieza aqui: [[00-empieza-aqui]]
- Entorno: [[01-instalar-python-y-terminal]]
- Donde tecleas: `09_pokemon_battle_cli_practica/pokemon/`
- Referencia (modelo): `09_pokemon_battle_cli/pokemon/`
