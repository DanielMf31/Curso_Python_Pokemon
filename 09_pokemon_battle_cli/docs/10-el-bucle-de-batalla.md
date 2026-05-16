---
title: 10 — El bucle de batalla
date: 2026-05-16
tags: [programacion/python, build-things, pokemon-cli, teaching]
type: doc
status: vivo
source: claude-code
---
# 10 — El bucle de batalla

## Por qué importa

Hasta ahora tenemos piezas sueltas: una tabla de tipos y una función que calcula el daño de un golpe. Pero un golpe no es una batalla. Una batalla es: dos Pokémon, turnos que se alternan, alguien elige movimiento, se aplica daño, se comprueba si alguien cayó, y se repite hasta que uno se queda sin vida. Ese "se repite hasta que" es un **bucle**, y este documento construye exactamente esa lógica.

Es la pieza que convierte cálculos en juego. También es donde aparece la diferencia entre el jugador (que **decide** su movimiento) y el rival (que lo elige **al azar**).

## Schema / Modelo mental (diagrama ASCII)

Un turno es una pequeña máquina de estados. La batalla entera es ese turno repetido hasta que alguien se desmaya.

```
                 +-------------------------------+
                 |        INICIO DEL TURNO        |
                 +---------------+----------------+
                                 |
                                 v
                 +-------------------------------+
                 | El jugador elige movimiento   |
                 |  (input por teclado, ui.py)   |
                 +---------------+----------------+
                                 |
                                 v
                 +-------------------------------+
                 | player ataca a rival          |
                 | dmg = calculate_damage(...)   |
                 | rival.take_damage(dmg)        |
                 +---------------+----------------+
                                 |
                                 v
                       rival.is_fainted() ?
                        SI -> GANA EL JUGADOR  (fin)
                        NO -> sigue
                                 |
                                 v
                 +-------------------------------+
                 | El rival elige movimiento     |
                 |  random.choice(rival.moves)   |
                 +---------------+----------------+
                                 |
                                 v
                 +-------------------------------+
                 | rival ataca a player          |
                 | dmg = calculate_damage(...)   |
                 | player.take_damage(dmg)       |
                 +---------------+----------------+
                                 |
                                 v
                       player.is_fainted() ?
                        SI -> GANA EL RIVAL  (fin)
                        NO -> volver a INICIO DEL TURNO
```

La condición que mantiene vivo el bucle es: "ninguno de los dos se ha desmayado todavía". En cuanto uno cae, salimos y declaramos ganador.

## Las piezas de apoyo: `Pokemon` y sus métodos

El bucle se apoya en dos comportamientos del objeto `Pokemon`:

- `pokemon.take_damage(n)` -> resta `n` puntos de vida al Pokémon. Es la única forma de aplicar daño; el bucle calcula con `calculate_damage` y entrega el número a `take_damage`.
- `pokemon.is_fainted()` -> devuelve `True` si su vida llegó a 0 (o menos). Es la pregunta de "¿se acabó para este Pokémon?".

El bucle nunca toca la vida directamente; siempre pasa por estos métodos. Eso mantiene la regla "el Pokémon gestiona su propia vida" en un solo sitio.

## Jugador vs rival: la única diferencia real

El esqueleto del turno es idéntico para ambos: elegir movimiento, calcular daño, aplicarlo, comprobar desmayo. Lo único que cambia es **cómo se elige el movimiento**:

- **Jugador**: le preguntamos. La función de `ui.py` muestra los movimientos disponibles y lee por teclado cuál quiere. Devuelve un objeto `Move`.
- **Rival**: no le preguntamos a nadie. `random.choice(rival.moves)` saca uno de su lista al azar. Es un rival "tonto" pero suficiente para el juego.

Mantén esa frontera limpia: la entrada por teclado vive en `ui.py`, no dentro del bucle. El bucle solo dice "necesito un movimiento del jugador" y delega.

## El orden del turno y por qué importa el chequeo intermedio

El jugador ataca primero. **Antes** de dejar atacar al rival, comprobamos si el rival se desmayó. Si no hiciéramos ese chequeo intermedio, un rival ya derrotado todavía podría devolver el golpe — el jugador ganaría pero recibiría daño de un Pokémon "muerto". Por eso hay **dos comprobaciones de desmayo por turno**, una después de cada ataque, no una sola al final.

## Sintaxis Python (al final)

```python
import random


class Battle:
    def __init__(self, player, rival):
        self.player = player
        self.rival = rival

    def run(self):
        while not self.player.is_fainted() and not self.rival.is_fainted():
            # --- turno del jugador ---
            move = choose_player_move(self.player)      # de ui.py
            dmg = calculate_damage(self.player, self.rival, move)
            self.rival.take_damage(dmg)
            if self.rival.is_fainted():
                break

            # --- turno del rival ---
            rival_move = random.choice(self.rival.moves)
            dmg = calculate_damage(self.rival, self.player, rival_move)
            self.player.take_damage(dmg)
            if self.player.is_fainted():
                break

        # --- declarar ganador ---
        if self.rival.is_fainted():
            return self.player
        return self.rival
```

Conceptos de sintaxis:
- `while not A and not B:` -> "sigue mientras NINGUNO de los dos se haya desmayado". Equivale a "para en cuanto uno caiga".
- `break` -> sale del `while` inmediatamente. Lo usamos en el chequeo intermedio para no dejar contraatacar a un Pokémon ya vencido.
- `random.choice(lista)` -> devuelve un elemento al azar de una lista (la usamos sobre `rival.moves`).
- El método `run` **devuelve** el Pokémon ganador en vez de imprimirlo; quién lo muestre es decisión de quien llama (lo verás en el último documento).

La condición del `while` y los `break` parecen redundantes, pero no lo son: el `while` evita entrar a un turno si la batalla ya acabó; los `break` cortan a mitad de turno cuando el primero de los dos ataques ya decidió el combate.

## Gotchas / Anti-patterns (tabla)

| Anti-pattern | Síntoma | Fix |
|---|---|---|
| Un solo chequeo de desmayo al final del turno | Un Pokémon ya derrotado devuelve el golpe | Comprobar `is_fainted()` después de CADA ataque, con `break` |
| `while True:` sin condición de salida clara | Bucle infinito si olvidas el `break` | `while not p.is_fainted() and not r.is_fainted()` como red de seguridad |
| Restar vida con `pokemon.hp -= dmg` directo | La regla de "vida no baja de 0 / desmayo" se duplica o se olvida | Siempre `pokemon.take_damage(dmg)` |
| Pedir input por teclado dentro de `Battle` | Imposible testear; mezcla lógica con UI | La entrada vive en `ui.py`; el bucle solo la invoca |
| `random.choice(rival)` en vez de `rival.moves` | Error: eliges sobre el Pokémon, no sus movimientos | `random.choice(rival.moves)` |
| Aplicar daño al atacante en vez de al defensor | El que pega se hace daño a sí mismo | `defender.take_damage(...)`, atacante y defensor bien ordenados |
| Imprimir el ganador dentro de `run()` | Lógica acoplada a la consola, no reutilizable | `run()` devuelve el ganador; el caller lo muestra |

## Tu turno

Implementa la lógica de `Battle` en `pokemon/battle.py`: el constructor con los dos Pokémon y el método que corre el bucle hasta KO, alterna turnos (jugador primero, vía la función de `ui.py`; rival con `random.choice`), aplica daño con `take_damage()`, comprueba `is_fainted()` tras cada ataque y devuelve el Pokémon ganador.

Comando de test exacto:

```
python -m pytest tests/test_battle.py -q
```

(Los tests fijan la semilla del azar y simulan la entrada del jugador, así que el resultado del bucle es determinista y comprobable.)

## Conexiones

- [[08-la-tabla-de-tipos]] — vía `calculate_damage`, cada ataque consulta la tabla.
- [[09-la-formula-de-dano]] — el bucle llama a `calculate_damage()` y entrega el resultado a `take_damage()`.
- [[11-juntandolo-todo]] — `main.py` crea un `Battle`, lo corre y muestra el ganador que `run()` devuelve.
- Ruta futura: `pokemon/battle.py` (clase `Battle`), `pokemon/ui.py` (elección del jugador), `pokemon/pokemon.py` (`take_damage`, `is_fainted`).
- Test: `tests/test_battle.py`.

## Resumen mental

> El bucle de batalla convierte cálculos sueltos en juego. Un turno es una máquina de estados: el jugador elige movimiento (input vía `ui.py`), se calcula daño con `calculate_damage`, se aplica con `rival.take_damage(dmg)`, se comprueba `rival.is_fainted()`; si no cayó, el rival elige al azar con `random.choice(rival.moves)`, ataca, y se comprueba `player.is_fainted()`. La batalla es ese turno dentro de un `while not player.is_fainted() and not rival.is_fainted()`. Clave: hay DOS chequeos de desmayo por turno (uno tras cada ataque, con `break`), no uno al final — si no, un Pokémon ya vencido contraataca. La única diferencia jugador/rival es cómo se elige el movimiento: preguntar vs `random.choice`. Reglas de higiene: nunca tocar `hp` directo (siempre `take_damage`), la entrada por teclado vive en `ui.py` no en `Battle` (testeabilidad), y `run()` devuelve el ganador en vez de imprimirlo (desacoplar lógica de consola). El `while` y los `break` se complementan: el `while` evita entrar a turno con la batalla ya acabada, los `break` cortan a mitad de turno.
