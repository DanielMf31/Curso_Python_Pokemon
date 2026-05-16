---
title: 02 — Variables y tipos
date: 2026-05-16
tags: [programacion/python, build-things, pokemon-cli, teaching]
type: doc
status: vivo
source: claude-code
---

# 02 — Variables y tipos: cajas con etiqueta para guardar el estado del combate

## Por qué importa

Un combate Pokémon es, en el fondo, un montón de datos que cambian con el tiempo: los puntos de salud de Charmander bajan, los PP de un movimiento se gastan, un Pokémon pasa de "en pie" a "debilitado". Antes de poder escribir una sola línea de lógica de batalla necesitas un sitio donde **guardar** esos datos y un nombre para **referirte** a ellos. Eso es una variable.

Y no todos los datos son iguales. El nombre "Pikachu" es texto. Sus 35 puntos de salud son un número entero. El multiplicador de un ataque súper efectivo, `2.0`, es un número con decimales. La respuesta a "¿está debilitado?" es sí o no. Cada uno de esos es un **tipo** distinto, y Python trata cada tipo con reglas diferentes. Confundirlos es la primera fuente de bugs de cualquier principiante: sumar texto cuando querías sumar números, comparar `"35"` con `35` y que no sean iguales.

Este documento es la base de todo el paquete `pokemon/`. Cada atributo de `Move` y `Pokemon` que implementarás más adelante es una variable con un tipo concreto.

## Schema / Modelo mental

Piensa en una variable como una **caja con una etiqueta pegada**. La etiqueta es el nombre. Dentro hay un valor. El tipo describe **qué clase de cosa** vive dentro de la caja.

```
   nombre (etiqueta)         valor (contenido)        tipo (qué clase de cosa)
  ┌─────────────────┐
  │  pokemon_name   │──────► "Pikachu"          ───►  str   (texto)
  └─────────────────┘
  ┌─────────────────┐
  │       hp        │──────►  35                ───►  int   (entero)
  └─────────────────┘
  ┌─────────────────┐
  │   multiplier    │──────►  2.0               ───►  float (decimal)
  └─────────────────┘
  ┌─────────────────┐
  │    fainted      │──────►  False             ───►  bool  (sí / no)
  └─────────────────┘
```

Reglas mentales:

1. **El nombre no es el valor.** `hp` es la etiqueta; `35` es lo que hay dentro. Puedes vaciar la caja y meter otra cosa (reasignar).
2. **El tipo viaja con el valor, no con la etiqueta.** Python mira lo que hay *dentro* de la caja para saber el tipo, no el nombre.
3. **Cada tipo tiene sus propias reglas.** Con `int` puedes restar daño. Con `str` puedes pegar nombres. Mezclarlos sin convertir explota.

## Qué es una variable

Una variable conecta un nombre con un valor. Cuando escribes:

```python
pokemon_name = "Pikachu"
```

Le estás diciendo a Python: "crea una caja, ponle la etiqueta `pokemon_name`, y mete dentro el texto `Pikachu`". A partir de ese momento, cada vez que escribas `pokemon_name`, Python va a la caja, mira qué hay dentro y usa ese valor.

El símbolo `=` **no es** "igual" como en matemáticas. Es una flecha que va de derecha a izquierda: "calcula lo de la derecha y guárdalo con el nombre de la izquierda". Lee `hp = 35` como "*hp recibe 35*".

## Los cuatro tipos que necesitas para el combate

### int — números enteros

Un `int` es un número sin parte decimal. Todo lo que se cuenta de uno en uno en un combate es un `int`:

```python
max_hp = 39        # los puntos de salud máximos de Charmander
attack = 52        # su estadística de ataque
power = 40         # la potencia de Ascuas
pp = 25            # cuántas veces se puede usar el movimiento
level = 5          # el nivel del Pokémon
```

Con enteros puedes hacer aritmética normal: sumar, restar, multiplicar.

```python
damage = 12
hp = 39
hp = hp - damage   # hp ahora vale 27
```

Esa última línea es el corazón del método `take_damage` que implementarás en `Pokemon`: coger el `hp` actual, restarle el daño, y volver a guardarlo en la misma variable.

### float — números con decimales

Un `float` tiene parte decimal. En este proyecto los `float` aparecen casi exclusivamente como **multiplicadores de efectividad de tipo**: cuando Agua ataca a Fuego es súper efectivo y el daño se multiplica por `2.0`; cuando Fuego ataca a Agua es poco efectivo y se multiplica por `0.5`.

```python
super_effective = 2.0
not_very_effective = 0.5
neutral = 1.0
```

Fíjate que `2.0` y `2` no son lo mismo para Python: el primero es `float`, el segundo es `int`. Da igual para hacer cuentas (el resultado de mezclarlos será `float`), pero el tipo es distinto.

### str — texto (cadenas de caracteres)

Un `str` (de *string*) es texto: una secuencia de caracteres entre comillas. Sirve para nombres y mensajes:

```python
pokemon_name = "Charmander"
move_name = "Ember"
type_name = "Fire"
```

Da igual usar comillas dobles `"..."` o simples `'...'`, mientras abras y cierres con las mismas. Lo importante: `"35"` con comillas es **texto**, no el número 35. Parecen iguales en pantalla pero Python los trata como cosas totalmente distintas, y esa confusión es un bug clásico.

Con texto puedes **concatenar** (pegar) usando `+`, pero solo texto con texto:

```python
first = "Char"
second = "mander"
full = first + second   # "Charmander"
```

### bool — verdadero o falso

Un `bool` (de *booleano*) solo puede valer una de dos cosas: `True` o `False` (con mayúscula inicial, sin comillas). Responde preguntas de sí/no sobre el estado del combate:

```python
fainted = False        # ¿el Pokémon está debilitado?
has_pp = True          # ¿le quedan usos al movimiento?
is_super_effective = True
```

Los `bool` son la materia prima de los `if` y los `while` que verás en el documento 04. El método `is_fainted()` de `Pokemon` devolverá un `bool`: `True` si el HP llegó a 0, `False` si sigue en pie.

## Asignar y reasignar

Crear la variable por primera vez es **asignar**. Cambiar lo que hay dentro después es **reasignar**. La etiqueta no cambia; el contenido sí:

```python
hp = 39        # asignación: la caja "hp" nace con 39 dentro
hp = 27        # reasignación: tiramos el 39, metemos 27
hp = hp - 10   # reasignación usando el valor anterior: hp pasa a 17
```

La última línea merece detenerse. Python primero **lee** el valor actual de la derecha (`hp - 10`, o sea `27 - 10 = 17`), y *después* guarda ese resultado en la caja `hp`. Por eso una variable puede "actualizarse a sí misma". Esto es exactamente lo que pasa cuando un Pokémon recibe daño turno tras turno.

## Saber qué tipo tiene algo: `type()`

Si alguna vez dudas de qué hay dentro de una caja, `type()` te lo dice:

```python
print(type(35))          # <class 'int'>
print(type(2.0))         # <class 'float'>
print(type("Pikachu"))   # <class 'str'>
print(type(False))       # <class 'bool'>
```

Es una herramienta de diagnóstico, sobre todo cuando un cálculo da un resultado raro y sospechas que un valor es texto cuando debería ser número.

## Convertir entre tipos

A veces tienes un valor de un tipo y lo necesitas en otro. Las funciones de conversión llevan el nombre del tipo destino:

```python
int("40")     # 40   -> texto a entero
str(35)       # "35" -> entero a texto
float(2)      # 2.0  -> entero a decimal
int(2.0)      # 2    -> decimal a entero (descarta decimales, NO redondea)
```

Conviertes texto a número cuando lees algo que el usuario escribió por teclado (siempre llega como `str`). Conviertes número a texto cuando quieres meterlo en un mensaje. Cuidado con `int(2.9)`: da `2`, no `3` — corta la parte decimal, no redondea.

## f-strings: meter variables dentro de un mensaje

Para mostrar mensajes de combate necesitas insertar el valor de variables dentro de texto. La forma moderna y legible es el **f-string**: una cadena precedida por la letra `f`, con las variables entre llaves `{}`.

```python
pokemon_name = "Pikachu"
hp = 35
print(f"{pokemon_name} tiene {hp} PS")
# Pikachu tiene 35 PS
```

Python sustituye `{pokemon_name}` por su valor y `{hp}` por el suyo, convirtiéndolos a texto automáticamente. Puedes meter incluso pequeños cálculos dentro de las llaves:

```python
move_name = "Thunderbolt"
pp = 14
max_pp = 15
print(f"{move_name}: {pp}/{max_pp} PP")
# Thunderbolt: 14/15 PP
```

Toda la salida que verá el jugador en `ui.py` se construye con f-strings.

## Sintaxis Python (resumen de referencia)

```python
# Asignación
name = "Squirtle"          # str
hp = 44                    # int
multiplier = 0.5           # float
fainted = False            # bool

# Reasignación (usando el valor anterior)
hp = hp - 8                # hp pasa de 44 a 36

# Inspeccionar el tipo
type(hp)                   # <class 'int'>

# Conversión
int("40")                  # 40
str(36)                    # "36"
float(2)                   # 2.0

# f-string
print(f"{name} tiene {hp} PS")   # Squirtle tiene 36 PS
```

## Gotchas / Anti-patterns

| Anti-pattern | Qué pasa | Cómo hacerlo bien |
|---|---|---|
| `hp = "35"` cuando querías el número | `hp - 5` explota: no puedes restar de un texto | Sin comillas: `hp = 35` |
| `damage = "12" + "5"` esperando 17 | Da `"125"` (pega los textos) | Usa enteros: `12 + 5` → `17` |
| `"35" == 35` | Da `False`: texto y entero nunca son iguales | Convierte antes: `int("35") == 35` |
| `True` escrito como `"true"` o `true` | `"true"` es texto; `true` no existe (error) | Exactamente `True` / `False`, mayúscula, sin comillas |
| `int(2.9)` esperando `3` | Da `2`: corta, no redondea | Usa `round(2.9)` si quieres redondear |
| Leer input y compararlo con un número | `input()` siempre da `str` | `int(input(...))` antes de comparar |
| `name + hp` (texto + entero) | Error: no se puede concatenar `str` con `int` | f-string: `f"{name}{hp}"` |

## Tu turno

Antes de tocar el paquete `pokemon/`, asegúrate de que entiendes variables y tipos con un ejercicio mental que imita un turno de combate. Crea un fichero temporal de pruebas (no forma parte de la entrega) y razona el resultado **antes** de ejecutarlo:

```python
# scratch.py  (fichero de juguete, bórralo después)
attacker_name = "Charmander"
move_name = "Ember"
move_power = 40
target_hp = 44
multiplier = 0.5          # Fuego contra Agua: poco efectivo

damage = int(move_power * multiplier)   # ¿qué tipo es damage? ¿cuánto vale?
target_hp = target_hp - damage          # reasignación
fainted = target_hp <= 0                # ¿qué tipo es fainted?

print(f"{attacker_name} usó {move_name}")
print(f"El objetivo tiene {target_hp} PS. ¿Debilitado? {fainted}")
```

Predice las dos líneas de salida en papel, luego ejecuta:

```
python tests/run_tests.py
```

`run_tests.py` es el lanzador de la batería de pruebas del proyecto (funciona aunque no tengas `pytest` instalado). Aún no tienes nada implementado, así que verás fallos — es lo esperado en este punto. El objetivo aquí es solo familiarizarte con el comando y comprobar que tu Python funciona; los tests irán pasando a medida que avances por los documentos siguientes.

## Conexiones

- [[03-estructuras-de-datos]] — cuando una sola variable no basta y necesitas listas y diccionarios
- [[04-condicionales-y-bucles]] — los `bool` de aquí alimentan los `if` y `while` del combate
- [[05-funciones]] — empaquetar lógica que opera sobre estas variables
- Ficheros futuros: `pokemon/move.py` (`name`, `power`, `pp` como `int`/`str`), `pokemon/pokemon.py` (`hp`, `attack`, `defense` como `int`), `pokemon/types.py` (multiplicadores `float`)

## Resumen mental

> Una variable es una caja con una etiqueta: el nombre referencia un valor, y el valor lleva consigo su tipo. En este combate manejas cuatro tipos. `int` para todo lo que se cuenta de uno en uno: HP, ataque, defensa, potencia, PP, nivel. `float` para los multiplicadores de efectividad de tipo: `2.0`, `0.5`, `1.0`. `str` para nombres y mensajes, siempre entre comillas. `bool` para preguntas de sí/no como "¿está debilitado?", que valen `True` o `False`. El símbolo `=` no es igualdad: es "guarda lo de la derecha con el nombre de la izquierda", lo que permite que una variable se actualice usando su valor previo (`hp = hp - damage`). Confundir `"35"` con `35` es el bug número uno: comparar texto con número siempre da `False`, y `input()` siempre entrega texto. Convierte explícitamente con `int()`, `str()`, `float()`. Para mostrar valores dentro de mensajes usa f-strings: `f"{name} tiene {hp} PS"`.
