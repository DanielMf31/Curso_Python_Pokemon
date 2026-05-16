---
title: 03 — Estructuras de datos
date: 2026-05-16
tags: [programacion/python, build-things, pokemon-cli, teaching]
type: doc
status: vivo
source: claude-code
---

# 03 — Estructuras de datos: cuando una variable no basta

## Por qué importa

En el documento anterior una variable guardaba **un** valor: un nombre, un HP, un booleano. Pero un combate Pokémon está lleno de **colecciones** de valores. Charmander no tiene un movimiento, tiene una lista de hasta cuatro. La Pokédex no guarda un Pokémon, guarda diez, y necesitas buscar cualquiera por su nombre. La tabla de tipos relaciona cada tipo atacante con cómo afecta a cada tipo defensor: una rejilla entera de multiplicadores.

Si solo conocieras variables sueltas tendrías que escribir `move1`, `move2`, `move3`, `move4` y duplicar código sin parar. Las **estructuras de datos** resuelven esto: te dejan guardar muchos valores juntos bajo un solo nombre y acceder a ellos de forma ordenada. Elegir la estructura correcta —lista, diccionario, tupla o conjunto— es la mitad de un buen diseño. La otra mitad es saber recorrerlas, que es el documento 04.

Este documento explica las cuatro estructuras que aparecen en `pokemon/data.py` (la Pokédex) y `pokemon/types.py` (la tabla de tipos).

## Schema / Modelo mental

Las dos estructuras centrales del proyecto son **lista** y **diccionario**. La diferencia clave: cómo encuentras un elemento.

```
  LISTA  ── orden por POSICIÓN (índice numérico, empieza en 0)
  ┌───────┬────────┬────────────┬───────────┐
  │   0   │   1    │     2      │     3     │   índice
  ├───────┼────────┼────────────┼───────────┤
  │ Ember │ Scratch│ Tail Whip  │  Growl    │   valor
  └───────┴────────┴────────────┴───────────┘
       moves[0] == "Ember"        moves[2] == "Tail Whip"

  DICCIONARIO  ── orden por CLAVE (la clave la eliges tú, suele ser texto)
  ┌─────────────┬──────────────────────────────────┐
  │   clave     │             valor                │
  ├─────────────┼──────────────────────────────────┤
  │ "Pikachu"   │  {hp: 35, attack: 55, ...}       │
  │ "Charmander"│  {hp: 39, attack: 52, ...}       │
  │ "Squirtle"  │  {hp: 44, attack: 48, ...}       │
  └─────────────┴──────────────────────────────────┘
       POKEDEX["Pikachu"]  ──►  los datos de Pikachu
```

Reglas mentales:

1. **Lista = secuencia ordenada que indexas por número.** Útil cuando el orden importa o cuando recorres todo (los movimientos de un Pokémon, el equipo).
2. **Diccionario = mapa de clave → valor.** Útil cuando quieres *buscar algo por su nombre* sin recorrer todo (la Pokédex por nombre, la tabla de tipos por tipo).
3. **Tupla = lista que no cambia.** Para agrupar cosas que van juntas y no deben modificarse, como el par `(attacker, defender)` de un turno.
4. **Conjunto = bolsa sin duplicados ni orden.** Aparece poco aquí; sirve para "¿qué tipos distintos hay en el equipo?".

## list — secuencia ordenada

Una lista guarda varios valores en orden, entre corchetes `[]`, separados por comas. Los movimientos de un Pokémon son una lista; el equipo del jugador es una lista de Pokémon.

```python
moves = ["Ember", "Scratch", "Tail Whip", "Growl"]
team = ["Charmander", "Pikachu", "Squirtle"]
```

### Indexado: acceder por posición

Cada elemento tiene un número de posición llamado **índice**, y **empieza en 0**, no en 1. Esto descoloca a todo principiante: el primer movimiento es `moves[0]`, no `moves[1]`.

```python
moves[0]    # "Ember"      (el primero)
moves[1]    # "Scratch"
moves[3]    # "Growl"      (el cuarto y último)
moves[-1]   # "Growl"      (índice negativo: cuenta desde el final)
```

### len: cuántos elementos hay

```python
len(moves)   # 4
len(team)    # 3
```

Esto importa para validar: un Pokémon no puede tener más de 4 movimientos, y la batalla termina cuando un equipo se queda sin Pokémon en pie.

### append: añadir al final

```python
moves = ["Ember"]
moves.append("Scratch")
moves.append("Growl")
# moves ahora es ["Ember", "Scratch", "Growl"]
```

`append` modifica la lista existente; no devuelve una nueva. Así se construye la lista de movimientos de un Pokémon al crearlo.

### in: ¿está este valor?

```python
"Ember" in moves      # True
"Surf" in moves       # False
```

Devuelve un `bool`, así que encaja directamente en un `if` (documento 04).

### Iterar: recorrer todos

```python
for move in moves:
    print(move)
# Ember
# Scratch
# Growl
```

Esto es exactamente lo que hace la interfaz cuando lista los movimientos disponibles para que el jugador elija. El detalle del `for` está en el documento 04; aquí basta saber que una lista se recorre de principio a fin en orden.

## dict — mapa de clave a valor

Un diccionario asocia cada **clave** con un **valor**. Se escribe entre llaves `{}`, con pares `clave: valor` separados por comas. Es la estructura de la **Pokédex**: la clave es el nombre del Pokémon, el valor son sus datos.

```python
POKEDEX = {
    "Charmander": {"type": "Fire",  "hp": 39, "attack": 52, "defense": 43},
    "Squirtle":   {"type": "Water", "hp": 44, "attack": 48, "defense": 65},
    "Pikachu":    {"type": "Electric", "hp": 35, "attack": 55, "defense": 40},
}
```

### Acceso por clave

En vez de un número de posición, usas la clave entre corchetes:

```python
POKEDEX["Charmander"]              # {"type": "Fire", "hp": 39, ...}
POKEDEX["Charmander"]["hp"]        # 39
POKEDEX["Charmander"]["type"]      # "Fire"
```

Esto es buscar por nombre sin recorrer nada: vas directo. Por eso `data.py` usa un diccionario para la Pokédex y no una lista — el juego pregunta "dame los datos de *Pikachu*", no "dame el quinto Pokémon".

### `in` sobre claves y acceso seguro

```python
"Pikachu" in POKEDEX        # True   (¿existe esa clave?)
"Mewtwo" in POKEDEX         # False
POKEDEX.get("Mewtwo")       # None   (no existe, pero no rompe)
```

`POKEDEX["Mewtwo"]` con una clave que no existe **lanza un error** y detiene el programa. `.get(...)` devuelve `None` en su lugar, útil cuando no estás seguro de que la clave exista.

### Diccionario de diccionarios: la tabla de tipos

La estructura más rica del proyecto está en `pokemon/types.py`. `TYPE_CHART` es un diccionario cuyos valores son a su vez diccionarios. La clave externa es el **tipo atacante**; la clave interna es el **tipo defensor**; el valor es el **multiplicador de daño**.

```python
TYPE_CHART = {
    "fire":  {"grass": 2.0, "water": 0.5, "fire": 0.5},
    "water": {"fire": 2.0, "grass": 0.5, "water": 0.5},
    "grass": {"water": 2.0, "fire": 0.5, "grass": 0.5},
    # ...
}
```

Para saber cuánto daño hace Fuego contra Planta, encadenas dos accesos por clave:

```python
TYPE_CHART["fire"]["grass"]   # 2.0  -> súper efectivo
TYPE_CHART["fire"]["water"]   # 0.5  -> poco efectivo
```

Visualmente, lo segundo es entrar en la fila `"fire"` y luego en la columna `"grass"`:

```
              defensor
            fire  water  grass
attacker ┌───────────────────────┐
  fire    │ 0.5   0.5    2.0     │ ◄── TYPE_CHART["fire"] es esta fila
  water   │ 2.0   0.5    0.5     │
  grass   │ 0.5   2.0    0.5     │
          └───────────────────────┘
                          ▲
              TYPE_CHART["fire"]["grass"] == 2.0
```

Cuando un par tipo-atacante / tipo-defensor **no está** en la tabla (combinaciones neutras), el multiplicador por defecto es `1.0`. La función `effectiveness()` del documento 05 encapsula exactamente esa lógica: mira la tabla, y si no encuentra la combinación, devuelve `1.0`.

## tuple — agrupación fija

Una tupla es como una lista pero **no se puede modificar** después de crearla. Se escribe con paréntesis `()`. Sirve para agrupar cosas que van juntas y forman una unidad, como los dos participantes de un turno:

```python
turn = ("Charmander", "Squirtle")   # (atacante, defensor)
attacker = turn[0]                  # "Charmander"
defender = turn[1]                  # "Squirtle"
```

Se indexa igual que una lista (`turn[0]`), pero `turn[0] = "Pikachu"` daría error: una tupla es inmutable. Esa inmutabilidad es una garantía: si pasas un par `(attacker, defender)` por el código, nadie puede cambiarlo a medias por accidente.

## set — colección sin duplicados (mención)

Un conjunto guarda valores **sin orden y sin repetidos**, con llaves `{}` (pero sin pares clave:valor). Apenas se usa en este proyecto; conviene conocerlo para una pregunta como "¿qué tipos distintos tiene mi equipo?":

```python
team_types = {"Fire", "Water", "Fire", "Electric"}
# team_types == {"Fire", "Water", "Electric"}  -> el "Fire" repetido se descarta
```

Es la herramienta natural cuando solo te importa *qué cosas distintas hay*, no cuántas ni en qué orden.

## Sintaxis Python (resumen de referencia)

```python
# LISTA
moves = ["Ember", "Scratch"]
moves[0]                 # "Ember"   (índice desde 0)
len(moves)               # 2
moves.append("Growl")    # añade al final
"Ember" in moves         # True
for m in moves: ...      # recorrer

# DICCIONARIO
POKEDEX = {"Pikachu": {"hp": 35}}
POKEDEX["Pikachu"]            # {"hp": 35}
POKEDEX["Pikachu"]["hp"]      # 35
"Pikachu" in POKEDEX          # True (busca en claves)
POKEDEX.get("Mewtwo")         # None (no rompe si falta)
TYPE_CHART["fire"]["grass"]   # 2.0 (dict de dicts)

# TUPLA
turn = ("Charmander", "Squirtle")
turn[0]                  # "Charmander" (no se puede reasignar)

# CONJUNTO
types = {"Fire", "Water", "Fire"}   # -> {"Fire", "Water"}
```

## Gotchas / Anti-patterns

| Anti-pattern | Qué pasa | Cómo hacerlo bien |
|---|---|---|
| `moves[1]` esperando el primero | El primero es `moves[0]`; los índices empiezan en 0 | `moves[0]` para el primero |
| `moves[4]` con 4 elementos | `IndexError`: el último es `moves[3]` | El último válido es `moves[len(moves)-1]` o `moves[-1]` |
| `POKEDEX["Mewtwo"]` sin comprobar | `KeyError` y el programa muere | `if "Mewtwo" in POKEDEX:` o `.get(...)` |
| `new = moves.append("X")` | `append` devuelve `None`, no la lista | `moves.append("X")` y sigue usando `moves` |
| `turn[0] = "Pikachu"` (tupla) | `TypeError`: las tuplas son inmutables | Usa una lista si necesitas modificar |
| Buscar en la Pokédex recorriendo una lista | Lento y verboso | Usa un `dict` y accede por clave directa |
| Olvidar el `1.0` por defecto en la tabla de tipos | `KeyError` en combinaciones neutras | `effectiveness()` devuelve `1.0` si falta la clave |

## Tu turno

No implementas nada todavía: la tarea es **leer** y rastrear con el dedo cómo el código usa estas estructuras. Abre `pokemon/data.py` y localiza la Pokédex (un `dict` con los 10 Pokémon: Charmander, Squirtle, Bulbasaur, Pikachu, Geodude, Rattata, Charizard, Blastoise, Venusaur, Raichu). Para cada uno, anota: ¿la clave es el nombre? ¿el valor es otro `dict`? ¿qué claves internas tiene (type, hp, attack, defense)?

Luego abre `pokemon/types.py` y localiza `TYPE_CHART`. Sin ejecutar nada, predice en papel el valor de:

- `TYPE_CHART["water"]["fire"]`
- `TYPE_CHART["grass"]["water"]`
- la efectividad de `"normal"` contra `"rock"` (¿está en la tabla? si no, ¿cuál es el valor por defecto?)

Comprueba que tu lectura de la tabla es correcta ejecutando solo las pruebas de tipos:

```
python -m pytest tests/test_types.py -q
```

Estas pruebas son la **especificación** de cómo debe comportarse `effectiveness()`. Léelas: te dicen exactamente qué multiplicador se espera para cada combinación. Es normal que fallen ahora; las harás pasar en el documento 05 al implementar `effectiveness()`.

## Conexiones

- [[02-variables-y-tipos]] — una estructura de datos contiene valores de los tipos del doc 02
- [[04-condicionales-y-bucles]] — `for` para recorrer listas, `in` dentro de `if`
- [[05-funciones]] — `effectiveness()` encapsula el acceso a `TYPE_CHART` con default `1.0`
- Ficheros futuros: `pokemon/data.py` (`POKEDEX` como `dict`), `pokemon/types.py` (`TYPE_CHART` como `dict` de `dict`s), `pokemon/pokemon.py` (`moves` como `list`)

## Resumen mental

> Cuando una sola variable no basta, usas una estructura de datos. Una lista guarda valores en orden y los indexas por posición empezando en cero: los movimientos de un Pokémon y el equipo son listas; `len()` cuenta, `append()` añade, `in` comprueba pertenencia, y se recorren con `for`. Un diccionario mapea clave a valor y permite buscar directamente sin recorrer: la Pokédex usa el nombre como clave y los datos del Pokémon como valor, y la tabla de tipos es un diccionario de diccionarios donde `TYPE_CHART["fire"]["grass"]` da el multiplicador de Fuego contra Planta. Acceder con una clave inexistente lanza `KeyError`; por eso `effectiveness()` devuelve `1.0` por defecto en combinaciones neutras. Una tupla es una lista inmutable, ideal para agrupar el par `(attacker, defender)` de un turno. Un conjunto guarda elementos únicos sin orden, útil para "qué tipos distintos hay". Elegir bien lista vs diccionario —recorrer vs buscar por nombre— es media batalla de diseño ganada.
