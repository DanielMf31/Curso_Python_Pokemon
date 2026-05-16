---
title: 04 — Condicionales y bucles
date: 2026-05-16
tags: [programacion/python, build-things, pokemon-cli, teaching]
type: doc
status: vivo
source: claude-code
---

# 04 — Condicionales y bucles: el cerebro y el motor del combate

## Por qué importa

Hasta ahora tienes datos guardados (variables, documento 02) y colecciones de datos (estructuras, documento 03). Pero un programa que solo guarda datos no *hace* nada. Un combate Pokémon **toma decisiones** ("¿le quedan PP a este movimiento? ¿está debilitado el rival? ¿qué multiplicador aplica este tipo?") y **repite acciones** ("turno tras turno hasta que un equipo caiga", "recorre los cuatro movimientos para mostrarlos").

Las decisiones son los **condicionales** (`if`/`elif`/`else`). La repetición son los **bucles** (`while` y `for`). Estas dos herramientas son el cerebro y el motor de `pokemon/battle.py`: el bucle `while` que mantiene viva la batalla, y los `if` que deciden quién gana cada interacción. Sin esto, el paquete `pokemon/` sería un catálogo estático de datos, no un juego.

## Schema / Modelo mental

Un turno de combate es un árbol de decisiones encadenado dentro de un bucle que se repite hasta el final:

```
  ┌─────────────────── while: nadie debilitado ───────────────────┐
  │                                                               │
  │   El jugador elige un movimiento                              │
  │            │                                                  │
  │            ▼                                                   │
  │     ¿el movimiento tiene PP?  ──── No ──► pedir otro (continue)│
  │            │ Sí                                                │
  │            ▼                                                   │
  │     calcular daño (mira el tipo: súper / poco / neutro)        │
  │            │                                                   │
  │            ▼                                                   │
  │     el defensor recibe daño                                    │
  │            │                                                   │
  │            ▼                                                   │
  │     ¿defensor debilitado?  ──── Sí ──► fin (break)             │
  │            │ No                                                │
  │            ▼                                                   │
  │     turno del rival (misma lógica)                             │
  │            │                                                   │
  └────────────┘  ◄── vuelve arriba si nadie cayó                 │
               │                                                  │
               ▼                                                  │
        anunciar ganador  ◄──────────────────────────────────────┘
```

Reglas mentales:

1. **`if` pregunta una vez; `while` pregunta cada vuelta.** El `if` decide en un punto; el `while` mantiene el combate vivo mientras se cumpla una condición.
2. **`for` recorre una colección conocida.** Los movimientos de un Pokémon, el equipo: número fijo de elementos, los visitas todos.
3. **`break` corta el bucle; `continue` salta a la siguiente vuelta.** Un Pokémon que cae rompe el `while`; un movimiento sin PP hace que vuelvas a pedir sin gastar el turno.
4. **La condición siempre es un `bool`** (documento 02): el resultado de una comparación o de `is_fainted()`.

## Condicionales: tomar decisiones

### if / elif / else

`if` ejecuta un bloque **solo si** una condición es `True`. `elif` ("else if") prueba otra condición si la anterior falló. `else` es el caso por defecto cuando ninguna se cumplió.

```python
if pokemon.hp <= 0:
    print(f"{pokemon.name} se debilitó")
elif pokemon.hp < pokemon.max_hp * 0.25:
    print(f"¡{pokemon.name} está en peligro!")
else:
    print(f"{pokemon.name} sigue en forma")
```

Python evalúa de arriba abajo y entra en **el primer** bloque cuya condición sea `True`; el resto se ignora aunque también fueran ciertas. El orden importa: si `hp <= 0` también es menor que el 25%, gana el primero porque está antes.

La **indentación** (los espacios al principio de la línea) no es decorativa en Python: es lo que marca qué líneas están *dentro* del `if`. Cuatro espacios por nivel. Si te desalineas, el código hace algo distinto o ni arranca.

### Comparaciones

Las condiciones se construyen comparando valores. El resultado siempre es un `bool`:

```python
pokemon.hp == 0       # ¿es exactamente igual a 0?
pokemon.hp != 0       # ¿es distinto de 0?
pokemon.hp <= 0       # ¿menor o igual que 0?  (debilitado)
move.pp > 0           # ¿le quedan usos?
attack_type == "fire" # ¿el tipo es Fuego?
```

Cuidado clásico: `==` compara, `=` asigna. `if hp = 0` es un error de sintaxis; lo que quieres es `if hp == 0`.

### and / or / not

Para combinar varias condiciones:

- `and`: verdadero solo si **ambas** lo son.
- `or`: verdadero si **al menos una** lo es.
- `not`: invierte (`not True` es `False`).

```python
# El movimiento es usable si tiene PP Y el atacante no está debilitado
if move.pp > 0 and not attacker.is_fainted():
    use_move(move)

# La batalla termina si CUALQUIERA de los dos cae
if attacker.is_fainted() or defender.is_fainted():
    end_battle()
```

`not attacker.is_fainted()` se lee literalmente: "el atacante NO está debilitado". Combinar `and`/`or`/`not` con los métodos `bool` del proyecto (`is_fainted()`, `has_pp()`) es como se expresa toda la lógica de reglas del combate.

## Bucles: repetir acciones

### while: repetir mientras se cumpla algo

`while` ejecuta su bloque una y otra vez **mientras** la condición sea `True`. Es el motor de la batalla: el combate continúa mientras ningún equipo esté completamente debilitado.

```python
while not player.is_fainted() and not rival.is_fainted():
    player_turn()
    if rival.is_fainted():
        break
    rival_turn()

announce_winner()
```

Antes de cada vuelta, Python re-evalúa la condición. En cuanto uno de los dos se debilita, la condición pasa a `False` y el bucle termina, llegando a `announce_winner()`.

El peligro del `while` es el **bucle infinito**: si la condición nunca pasa a `False`, el programa se cuelga. Por eso *dentro* del bucle algo tiene que mover la situación hacia el final — aquí, el HP que baja con cada turno hasta que alguien cae.

### for: recorrer una colección

`for` recorre los elementos de una lista (o cualquier estructura iterable) uno a uno. Lo usas para mostrar los movimientos disponibles o para revisar el equipo:

```python
for move in pokemon.moves:
    print(f"- {move.name} ({move.pp}/{move.max_pp} PP)")
```

En cada vuelta, `move` toma el valor del siguiente elemento de `pokemon.moves`, hasta agotarlos. No tienes que llevar tú la cuenta de índices: `for` lo hace por ti. A diferencia de `while`, un `for` sobre una lista finita siempre termina solo.

### range: repetir un número fijo de veces

`range(n)` genera los números `0, 1, ..., n-1`. Útil cuando necesitas el número de turno o repetir N veces:

```python
for turn_number in range(1, 4):     # 1, 2, 3
    print(f"--- Turno {turn_number} ---")
```

`range(1, 4)` empieza en 1 y termina **antes** de 4 (el final es exclusivo, igual que los índices empezaban en 0).

### break y continue

Dentro de cualquier bucle:

- `break`: sale del bucle **inmediatamente**, sin más vueltas.
- `continue`: abandona la vuelta actual y salta directamente a la siguiente.

```python
while True:
    move = ask_player_for_move()
    if not move.has_pp():
        print("Sin PP. Elige otro movimiento.")
        continue                 # vuelve a pedir, NO gasta turno
    if defender.is_fainted():
        break                    # el rival cayó: fin del combate
    resolve(move)
```

`continue` es exactamente "este intento no vale, repite la pregunta". `break` es "se acabó, sal de aquí". Juntos modelan los dos finales de una vuelta de combate: reintentar o terminar.

## Sintaxis Python (resumen de referencia)

```python
# CONDICIONAL
if pokemon.hp <= 0:
    print("debilitado")
elif pokemon.hp < pokemon.max_hp * 0.25:
    print("peligro")
else:
    print("ok")

# Operadores: ==  !=  <  <=  >  >=   and  or  not
if move.pp > 0 and not attacker.is_fainted():
    ...

# WHILE
while not a.is_fainted() and not b.is_fainted():
    do_turn()

# FOR sobre lista
for move in pokemon.moves:
    print(move.name)

# FOR con range
for n in range(1, 4):       # 1, 2, 3
    print(n)

# break / continue
while True:
    if done:   break
    if skip:   continue
```

## Gotchas / Anti-patterns

| Anti-pattern | Qué pasa | Cómo hacerlo bien |
|---|---|---|
| `if hp = 0:` | Error: `=` asigna, no compara | `if hp == 0:` |
| Indentar con espacios irregulares | `IndentationError` o bloque equivocado | 4 espacios consistentes por nivel |
| `while hp > 0:` sin bajar `hp` dentro | Bucle infinito, el programa se cuelga | Asegura que algo mueve la condición hacia `False` |
| Orden de `if`/`elif` mal puesto | Entra en un caso menos específico antes | Pon las condiciones más estrictas primero |
| `if move.pp > 0 and < attacker...` | Error: cada lado de `and` debe ser una condición completa | `move.pp > 0 and not attacker.is_fainted()` |
| `for i in range(4): moves[i]` | Verboso y propenso a `IndexError` | `for move in moves:` directamente |
| `continue` donde querías `break` (o al revés) | Reintenta cuando debía terminar (o corta de más) | `break` = salir; `continue` = siguiente vuelta |
| Comparar con `==` cosas que deben ser `bool` | `if is_fainted() == True` redundante | `if pokemon.is_fainted():` directamente |

## Tu turno

Ahora sí implementas lógica. Dos tareas en el paquete `pokemon/`:

1. **`is_fainted()` en `pokemon/pokemon.py`.** Es un método que devuelve un `bool`: `True` cuando el Pokémon ya no puede combatir, `False` si sigue en pie. La condición es una sola comparación sobre `self.hp`. Piensa: ¿debilitado es `hp == 0` o `hp <= 0`? El daño puede dejar el HP en negativo, así que elige la comparación que cubra ambos casos.

2. **El bucle `while` de `pokemon/battle.py`.** El combate debe repetirse mientras *ninguno* de los dos contendientes esté debilitado, y terminar en cuanto uno caiga para anunciar al ganador. Combina `while`, `not`, `and` y un `break` cuando proceda.

Verifica la primera tarea con la batería de pruebas de Pokémon, que es la especificación del comportamiento esperado de `is_fainted()`:

```
python -m pytest tests/test_pokemon.py -q
```

Lee el test antes de implementar: te dice con qué valores de HP debe devolver `True` y con cuáles `False`. Tu trabajo es escribir el `if`/comparación que haga pasar esos casos.

## Conexiones

- [[02-variables-y-tipos]] — toda condición evalúa a un `bool`, el tipo sí/no del doc 02
- [[03-estructuras-de-datos]] — `for` recorre las listas; `in` aparece dentro de `if`
- [[05-funciones]] — `is_fainted()` y `has_pp()` empaquetan estas condiciones en funciones reutilizables
- Ficheros futuros: `pokemon/pokemon.py` (`is_fainted()`), `pokemon/move.py` (`has_pp()`), `pokemon/battle.py` (bucle `while` del combate)

## Resumen mental

> Los condicionales toman decisiones y los bucles repiten acciones: juntos son el cerebro y el motor del combate. `if`/`elif`/`else` evalúa de arriba abajo y entra en el primer bloque cuya condición sea `True`, así que el orden importa y la indentación de cuatro espacios define qué está dentro. Las condiciones se construyen con comparaciones (`==`, `!=`, `<=`, `>`...) combinadas con `and`, `or`, `not`, y siempre producen un `bool`; recuerda que `==` compara y `=` asigna. El bucle `while` mantiene la batalla viva mientras ninguno esté debilitado, con el riesgo de bucle infinito si nada empuja la condición hacia `False` (aquí, el HP que baja cada turno). El bucle `for` recorre colecciones finitas como los movimientos o el equipo sin que lleves índices a mano, y `range` repite un número fijo de veces. Dentro de un bucle, `break` sale del todo y `continue` salta a la siguiente vuelta: reintentar un movimiento sin PP frente a terminar cuando un Pokémon cae.
