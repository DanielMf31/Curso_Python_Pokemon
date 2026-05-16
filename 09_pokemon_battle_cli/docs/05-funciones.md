---
title: 05 — Funciones
date: 2026-05-16
tags: [programacion/python, build-things, pokemon-cli, teaching]
type: doc
status: vivo
source: claude-code
---

# 05 — Funciones: empaquetar lógica en máquinas reutilizables

## Por qué importa

En el documento 04 escribiste lógica de combate: comparaciones, bucles, decisiones. Pero esa lógica vivía suelta. Imagina que la regla "Fuego contra Planta hace doble daño" tienes que consultarla en el turno del jugador, en el turno del rival, y al mostrar un aviso de "súper efectivo". Copiar la misma cadena de `if`/diccionario tres veces es la receta del desastre: el día que cambies la tabla de tipos, tienes que acordarte de cambiarla en tres sitios, y olvidarás uno.

Una **función** resuelve esto: empaquetas un trozo de lógica con un nombre, lo escribes una vez, y lo llamas desde donde quieras. `effectiveness(attack_type, defender_type)` calcula el multiplicador en *un* lugar; `calculate_damage(...)` aplica la fórmula de daño en *un* lugar. El resto del programa solo los invoca. Esto es por qué el paquete `pokemon/` está partido en módulos con funciones bien definidas en vez de un único guion gigante: cada función es una pieza testeable, reutilizable y reemplazable.

## Schema / Modelo mental

Una función es una **máquina**: entran datos por un lado (parámetros), ocurre algo dentro (cuerpo), y sale un resultado por el otro (`return`).

```
        entradas                  máquina                       salida
   (parámetros / argumentos)   (cuerpo: lógica)               (return)

   attack_type = "fire"  ──┐
                           ├──►  ┌─────────────────────┐
   defender_type = "grass"┘     │  effectiveness(...)  │ ──►  2.0
                                │  mira TYPE_CHART      │   (multiplicador)
                                │  default 1.0          │
                                └─────────────────────┘

   El que llama solo ve esto:   result = effectiveness("fire", "grass")
   No le importa CÓMO se calcula por dentro: solo qué entra y qué sale.
```

Reglas mentales:

1. **Definir no es ejecutar.** `def f(...)` solo crea la máquina. No hace nada hasta que la *llamas* con `f(...)`.
2. **Parámetro vs argumento.** El parámetro es el nombre en la definición (`attack_type`); el argumento es el valor real que pasas al llamar (`"fire"`).
3. **`return` devuelve un valor; `print` solo lo muestra.** Son cosas distintas y confundirlas es el bug más frecuente con funciones.
4. **Lo de dentro se queda dentro (scope).** Las variables creadas en una función no existen fuera de ella.

## def: definir una función

Una función se crea con `def`, un nombre, paréntesis con los parámetros, dos puntos, y un cuerpo indentado:

```python
def effectiveness(attack_type, defender_type):
    row = TYPE_CHART.get(attack_type, {})
    return row.get(defender_type, 1.0)
```

`def effectiveness(attack_type, defender_type):` declara una máquina llamada `effectiveness` que **espera dos entradas**. El cuerpo (las dos líneas indentadas) es lo que hace. Esta definición por sí sola no calcula nada: solo deja la máquina lista.

## Parámetros y argumentos: las entradas

Cuando *defines* la función, los nombres entre paréntesis son **parámetros** — huecos a rellenar. Cuando la *llamas*, los valores que pasas son **argumentos** — lo que metes en los huecos.

```python
def calculate_damage(power, attack, defense, multiplier):
    base = power * attack / defense
    return int(base * multiplier)

# Llamada: los argumentos rellenan los parámetros en orden
dmg = calculate_damage(40, 52, 65, 2.0)
#                       │   │   │   └─► multiplier
#                       │   │   └─────► defense
#                       │   └─────────► attack
#                       └─────────────► power
```

El orden importa: el primer argumento va al primer parámetro, y así sucesivamente. Dentro del cuerpo, `power` ya vale `40`, `multiplier` vale `2.0`, etc. La función no sabe ni le importa de dónde salieron esos números — solo trabaja con lo que recibe.

## return vs print: la diferencia que confunde a todo el mundo

Esta distinción es la que más cuesta y la que más bugs causa, así que va despacio.

- **`return`** entrega un valor *de vuelta* a quien llamó la función. Ese valor se puede guardar en una variable y seguir usándolo.
- **`print`** solo escribe texto en la pantalla. No devuelve nada útil; el valor se pierde.

```python
def effectiveness(attack_type, defender_type):
    row = TYPE_CHART.get(attack_type, {})
    return row.get(defender_type, 1.0)        # devuelve el número

mult = effectiveness("fire", "grass")          # mult vale 2.0, lo puedo usar
final_damage = base_damage * mult              # ...para calcular el daño
```

Compáralo con la versión rota:

```python
def effectiveness_broken(attack_type, defender_type):
    row = TYPE_CHART.get(attack_type, {})
    print(row.get(defender_type, 1.0))         # solo lo muestra, no lo devuelve

mult = effectiveness_broken("fire", "grass")   # imprime 2.0 en pantalla...
final_damage = base_damage * mult              # ...pero mult vale None -> ERROR
```

`effectiveness_broken` *parece* funcionar porque ves `2.0` en pantalla, pero `mult` queda en `None` y el cálculo de daño explota. Regla práctica: si otra parte del programa necesita el resultado para seguir calculando, usa `return`. `print` es solo para mensajes que lee el jugador (eso vive en `ui.py`, no en la lógica de `types.py` o `battle.py`).

Una función sin `return` explícito devuelve `None` automáticamente.

## Scope: lo de dentro se queda dentro

Las variables que creas *dentro* de una función solo existen ahí. Nacen al llamarla y desaparecen al terminar:

```python
def calculate_damage(power, attack, defense, multiplier):
    base = power * attack / defense    # 'base' solo vive aquí dentro
    return int(base * multiplier)

dmg = calculate_damage(40, 52, 65, 2.0)
print(base)   # ERROR: 'base' no existe fuera de la función
```

Esto es bueno: cada función es una caja sellada. `base` en `calculate_damage` no choca con ninguna otra `base` de otro módulo. La única forma de sacar información de una función es con `return`. Lo único que el resto del programa debe conocer de una función es su nombre, qué entradas espera y qué devuelve — no sus variables internas.

## Por qué separar la lógica en funciones

Mira las dos funciones clave del proyecto:

- `effectiveness(attack_type, defender_type)` en `pokemon/types.py`: encapsula *toda* la lógica de la tabla de tipos, incluido el `1.0` por defecto cuando la combinación no está. Quien la usa no necesita conocer la estructura de `TYPE_CHART`.
- `calculate_damage(...)` en la lógica de combate: encapsula la fórmula de daño. Si mañana ajustas la fórmula, la cambias en un sitio y *todo* el juego usa la nueva automáticamente.

Esto da tres ventajas concretas:

1. **No te repites.** La regla de tipos se escribe una vez, se llama muchas.
2. **Se puede testear aislado.** `tests/test_types.py` llama a `effectiveness(...)` con entradas concretas y comprueba la salida, sin montar una batalla entera.
3. **Se puede reemplazar.** Mientras nombre, entradas y salida no cambien, puedes reescribir el interior sin tocar el resto.

## Docstrings: documentar la máquina

Una cadena de texto justo después del `def` es un **docstring**: explica qué hace la función, qué espera y qué devuelve. Es para el humano que la lea (incluido tu yo futuro):

```python
def effectiveness(attack_type, defender_type):
    """Devuelve el multiplicador de daño del tipo atacante contra el defensor.

    Consulta TYPE_CHART. Si la combinación no está registrada (efecto
    neutro), devuelve 1.0.
    """
    row = TYPE_CHART.get(attack_type, {})
    return row.get(defender_type, 1.0)
```

Un buen docstring describe el contrato: entradas, salida y casos límite (aquí, el `1.0` por defecto). Quien llame a la función no debería tener que leer su cuerpo para saber usarla.

## Sintaxis Python (resumen de referencia)

```python
# Definir
def calculate_damage(power, attack, defense, multiplier):
    """Daño entero a partir de stats y multiplicador de tipo."""
    base = power * attack / defense
    return int(base * multiplier)        # devuelve un valor

# Llamar (argumentos rellenan parámetros en orden)
dmg = calculate_damage(40, 52, 65, 2.0)  # dmg utilizable después

# return vs print
def f(): return 7      # x = f()  -> x == 7
def g(): print(7)      # x = g()  -> x == None (solo imprimió)

# Sin return explícito -> devuelve None
# Variables del cuerpo NO existen fuera (scope)
```

## Gotchas / Anti-patterns

| Anti-pattern | Qué pasa | Cómo hacerlo bien |
|---|---|---|
| `print(...)` donde necesitabas `return` | El resultado se pierde, la variable queda `None` | `return` el valor; `print` solo para mensajes al jugador |
| Definir la función y no llamarla | `def` no ejecuta nada por sí solo | Llámala: `effectiveness("fire", "grass")` |
| Usar una variable interna fuera | `NameError`: no existe fuera del cuerpo | Sácala con `return` |
| Argumentos en orden equivocado | `calculate_damage(65, 40, ...)` da daño absurdo | Respeta el orden de los parámetros |
| Olvidar el `return` y esperar un valor | La función devuelve `None` silenciosamente | Asegura un `return` en todos los caminos |
| `effectiveness` sin default `1.0` | `KeyError` en combinaciones neutras | `dict.get(clave, 1.0)` para el caso por defecto |
| Lógica de tipos copiada en varios sitios | Inconsistencias al cambiarla | Una sola función, llamada desde todas partes |

## Tu turno

Implementa `effectiveness(attack_type, defender_type)` en `pokemon/types.py`. Contrato exacto:

- **Entradas:** dos cadenas, el tipo atacante y el tipo defensor (p. ej. `"fire"`, `"grass"`).
- **Salida:** un número (`float`) — el multiplicador de daño.
- **Regla:** consulta `TYPE_CHART`. Si la fila del atacante no existe, o la columna del defensor no está en esa fila, devuelve `1.0` (efecto neutro). No lances excepción, no imprimas: **`return`** el multiplicador.

Pista de diseño: `dict.get(clave, valor_por_defecto)` es tu aliado para no romper con `KeyError` y para el `1.0` por defecto en un solo paso.

Verifica contra la especificación, que es el fichero de pruebas de tipos:

```
python -m pytest tests/test_types.py -q
```

Lee `tests/test_types.py` antes de escribir nada: cada test te dice una combinación de entrada y el multiplicador exacto esperado (súper efectivo `2.0`, poco efectivo `0.5`, neutro `1.0`). Tu función debe hacer pasar todos esos casos. Cuando estén en verde, `effectiveness()` queda listo para que `calculate_damage()` y `battle.py` lo usen.

## Conexiones

- [[02-variables-y-tipos]] — los parámetros y el `return` llevan valores con tipo (doc 02)
- [[03-estructuras-de-datos]] — `effectiveness()` encapsula el acceso al `dict` de `dict`s `TYPE_CHART`
- [[04-condicionales-y-bucles]] — `is_fainted()`/`has_pp()` son funciones que devuelven el `bool` de los `if`/`while`
- Ficheros futuros: `pokemon/types.py` (`effectiveness()`), lógica de combate (`calculate_damage()`), `pokemon/move.py` (`use()`, `has_pp()`), `pokemon/pokemon.py` (`take_damage()`, `is_fainted()`)

## Resumen mental

> Una función es una máquina: entran datos por los parámetros, el cuerpo hace algo, y `return` entrega un resultado al que llamó. Definirla con `def` no la ejecuta; solo la llamada `nombre(argumentos)` la pone en marcha, y los argumentos rellenan los parámetros en orden. La distinción más importante y la más confundida es `return` frente a `print`: `return` devuelve un valor que el resto del programa puede guardar y seguir usando, mientras que `print` solo escribe en pantalla y deja la variable en `None`; usa `print` solo para mensajes al jugador. Las variables creadas dentro de una función no existen fuera (scope): la única salida es el `return`. Separar la lógica en funciones como `effectiveness()` y `calculate_damage()` evita repetir reglas, permite testear cada pieza aislada con su fichero de pruebas, y deja reescribir el interior sin tocar el resto mientras el contrato (nombre, entradas, salida) no cambie. El docstring documenta ese contrato, incluido el caso por defecto de `1.0`.
