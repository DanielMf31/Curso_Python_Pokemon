---
title: 09 — La fórmula de daño
date: 2026-05-16
tags: [programacion/python, build-things, pokemon-cli, teaching]
type: doc
status: vivo
source: claude-code
---
# 09 — La fórmula de daño

## Por qué importa

Cuando un Pokémon usa un movimiento contra otro, ¿cuántos puntos de vida quita? Esa única pregunta es donde se juntan todas las estadísticas: el nivel del atacante, la potencia del movimiento, el ataque del que pega, la defensa del que recibe, la ventaja de tipos (del documento anterior), un poco de azar, y la posibilidad de fallar el golpe.

Si esta función está mal, todo el juego se siente injusto: golpes que matan de uno, ataques que no hacen nada. Por eso la tratamos despacio, término a término. No hay que inventar nada: la fórmula está fijada en el CANON del proyecto. Nuestro trabajo es **entender qué hace cada parte** y traducirla fielmente.

## Schema / Modelo mental (diagrama ASCII)

La función es una tubería: entran tres cosas (atacante, defensor, movimiento), pasan por una serie de pasos, y sale un número entero de daño.

```
  ENTRADA                 PROCESO                          SALIDA
+-----------+
| attacker  |---+
| defender  |---+--> [1] tirada de precisión
| move      |---+         randint(1,100) > accuracy ?
+-----------+              |              |
                          SI -> FALLO    NO -> sigue
                          (daño 0)        |
                                          v
                       [2] base = formula(level, power,
                                          attack, defense)
                                          |
                                          v
                       [3] mult = effectiveness(move.type,
                                                defender.type)
                                          |
                                          v
                       [4] variance = uniform(0.85, 1.0)
                                          |
                                          v
                       [5] damage = max(1,
                            int(base * mult * variance))   --> int >= 1
```

Cinco pasos en orden. Si el paso 1 dice "fallo", la tubería se corta ahí. Si no, los pasos 2 a 5 calculan el número final.

## Paso 1 — ¿Acierta el golpe?

Cada movimiento tiene una `accuracy` (precisión), un número de 1 a 100. Un movimiento con `accuracy = 90` acierta el 90% de las veces.

Para decidir si acierta, tiramos un "dado" de 1 a 100 con `random.randint(1, 100)`. Comparamos:

```
si  randint(1,100) > accuracy   -> el golpe FALLA  (daño = 0)
si  randint(1,100) <= accuracy  -> el golpe acierta, seguimos
```

Intuición: si `accuracy = 90`, fallamos solo cuando el dado saca 91, 92, ..., 100 (10 valores de 100 = 10% de fallo). Cuanto mayor la precisión, menos números provocan fallo.

## Paso 2 — El daño base

Aquí está la fórmula del CANON, literal:

```
base = (((2 * level / 5 + 2) * move.power * (attacker.attack / defender.defense)) / 50) + 2
```

No es magia; cada trozo tiene sentido si lo lees de dentro hacia afuera:

- `2 * level / 5 + 2` -> el **nivel** del atacante. A más nivel, más grande este factor: los Pokémon fuertes pegan más fuerte aunque usen el mismo ataque.
- `* move.power` -> la **potencia del movimiento**. Un movimiento de potencia 90 hace tres veces más que uno de potencia 30.
- `* (attacker.attack / defender.defense)` -> el **duelo de stats**. Si mi ataque es alto y tu defensa baja, este cociente es grande (te hago mucho). Si tu defensa es enorme, el cociente baja (te hago poco). Es un ratio: lo que importa no es el número absoluto sino la proporción atacante/defensor.
- `/ 50 + 2` -> constantes de calibración que escalan el resultado a un rango razonable de puntos de vida. No tienen "significado" de juego, solo ajustan la magnitud.

El resultado `base` es un número decimal (puede ser `34.7`). Todavía no es el daño final.

## Paso 3 — La ventaja de tipos

Aquí enganchamos con el documento anterior:

```
mult = effectiveness(move.type, defender.type)
```

`mult` será `2.0`, `0.5` o `1.0`. Multiplica el `base`: súper efectivo dobla, poco efectivo parte por la mitad, neutral no cambia nada. Nota el orden de argumentos: **tipo del movimiento** primero, **tipo del Pokémon que recibe** después.

## Paso 4 — La varianza (el azar fino)

En Pokémon dos golpes idénticos no hacen exactamente el mismo daño; hay un pequeño ruido. Lo modelamos con:

```
variance = random.uniform(0.85, 1.0)
```

`uniform` devuelve un decimal al azar entre 0.85 y 1.0 (p.ej. `0.92`). Multiplicado por el resto, hace que el daño final sea entre el 85% y el 100% del cálculo "limpio". Nunca sube por encima del 100%: solo resta un poco, de forma impredecible.

## Paso 5 — Redondear y poner un suelo

```
damage = max(1, int(base * mult * variance))
```

Dos cosas pasan aquí:

- `int(...)` trunca el decimal a entero (los puntos de vida son enteros; `int(7.9)` es `7`, no redondea, recorta).
- `max(1, ...)` garantiza que el daño sea **al menos 1**. Sin esto, un ataque flojo contra una defensa enorme podría dar `int(0.4)` = `0`, y un golpe que conecta y no hace nada se siente roto. El suelo de 1 es una decisión de diseño: si acertaste, algo duele.

Importante: el suelo de 1 solo aplica cuando el golpe **acertó**. Un fallo (paso 1) devuelve 0, no 1.

## Sintaxis Python (al final)

```python
import random

def calculate_damage(attacker, defender, move) -> int:
    # paso 1: precisión
    if random.randint(1, 100) > move.accuracy:
        return 0  # fallo

    # paso 2: daño base
    base = (
        ((2 * attacker.level / 5 + 2) * move.power
         * (attacker.attack / defender.defense)) / 50
    ) + 2

    # paso 3: ventaja de tipos
    mult = effectiveness(move.type, defender.type)

    # paso 4: varianza
    variance = random.uniform(0.85, 1.0)

    # paso 5: redondeo + suelo
    damage = max(1, int(base * mult * variance))
    return damage
```

Funciones usadas:
- `random.randint(1, 100)` -> entero al azar entre 1 y 100, **ambos incluidos**.
- `random.uniform(0.85, 1.0)` -> decimal al azar en `[0.85, 1.0]`.
- `int(x)` -> trunca hacia cero (no redondea).
- `max(1, x)` -> el mayor entre 1 y x; aquí actúa de suelo.

Decisión de retorno: devolvemos el daño, no lo aplicamos. Quién recibe el golpe lo decide el bucle de batalla (siguiente documento). Esta función solo calcula.

## Gotchas / Anti-patterns (tabla)

| Anti-pattern | Síntoma | Fix |
|---|---|---|
| `random.randint(1, 100)` "1 a 99" | Crees que excluye el 100; precisión mal calibrada | `randint` incluye ambos extremos |
| Comparar `>= accuracy` para fallar | El golpe falla un caso de más/menos | El CANON dice `> accuracy` es fallo |
| `round(...)` en vez de `int(...)` | Daño 1 punto distinto al esperado, tests rojos | `int()` trunca, es lo que fija el CANON |
| Olvidar `max(1, ...)` | Golpes que aciertan y hacen 0 | Suelo de 1 obligatorio tras acertar |
| Aplicar `max(1, ...)` también al fallo | Un fallo hace 1 de daño en vez de 0 | El fallo retorna 0 antes de cualquier cálculo |
| `effectiveness(defender.type, move.type)` | Multiplicador invertido | Orden: `(move.type, defender.type)` |
| Llamar a `random` dos veces para la misma tirada | Decides fallo con un dado y daño con otro distinto | Una sola `randint` para la precisión |
| `attacker.defense / defender.attack` | Ratio de stats invertido | `attacker.attack / defender.defense` |

## Tu turno

Implementa `calculate_damage(attacker, defender, move)` en `pokemon/battle.py`, siguiendo los cinco pasos en orden exacto. Importa `effectiveness` desde `pokemon.types` y `random` (solo stdlib).

Comando de test exacto:

```
python -m pytest tests/test_battle.py -q
```

El test fija la semilla del azar (`random.seed(...)`) antes de llamar, así que aunque uses `random`, el resultado es **determinista** y comprobable. Si tu orden de llamadas a `random` no coincide con el del CANON, los números no cuadrarán: respeta el orden (primero la tirada de precisión, después la varianza).

## Conexiones

- [[08-la-tabla-de-tipos]] — `calculate_damage` llama a `effectiveness()` para el término `mult`.
- [[10-el-bucle-de-batalla]] — el bucle llama a `calculate_damage()` cada turno y aplica el resultado con `take_damage()`.
- Ruta futura: `pokemon/battle.py` (función `calculate_damage`).
- Test: `tests/test_battle.py`.

## Resumen mental

> `calculate_damage(attacker, defender, move)` devuelve cuánto daño hace un golpe, en cinco pasos ordenados. Paso 1: tirada de precisión con `random.randint(1,100)`; si supera `move.accuracy`, el golpe falla y retorna 0. Paso 2: daño base con la fórmula del CANON `(((2*level/5+2)*power*(attack/defense))/50)+2` — nivel y potencia escalan hacia arriba, el ratio ataque/defensa premia pegar fuerte contra defensa baja. Paso 3: multiplicador de tipos vía `effectiveness(move.type, defender.type)` (2.0/0.5/1.0). Paso 4: `random.uniform(0.85,1.0)` añade ruido que solo resta (85-100%). Paso 5: `max(1, int(base*mult*variance))` — `int` trunca, `max(1,...)` garantiza mínimo 1 si acertó. El fallo retorna 0 ANTES de cualquier cálculo; el suelo de 1 no aplica al fallo. Cuidados clave: `randint` incluye ambos extremos, `> accuracy` es fallo, `int` no `round`, orden de argumentos en `effectiveness`, una sola tirada para la precisión. La función solo calcula; aplicar el daño es trabajo del bucle de batalla. Los tests fijan la semilla para que el azar sea determinista.
