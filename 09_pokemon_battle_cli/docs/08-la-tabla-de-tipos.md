---
title: 08 — La tabla de tipos
date: 2026-05-16
tags: [programacion/python, build-things, pokemon-cli, teaching]
type: doc
status: vivo
source: claude-code
---
# 08 — La tabla de tipos

## Por qué importa

En Pokémon, un ataque de Fuego contra un Pokémon de Planta hace el doble de daño. El mismo ataque de Fuego contra un Pokémon de Agua hace la mitad. Esa regla — "qué tipo es fuerte o débil contra qué tipo" — es el corazón estratégico del juego. Sin ella, todos los ataques harían el mismo daño y elegir movimiento sería irrelevante.

Necesitamos representar esa regla en código. La pregunta es: dado un **tipo atacante** (el tipo del movimiento) y un **tipo defensor** (el tipo del Pokémon que recibe), ¿por cuánto multiplicamos el daño? La respuesta es siempre uno de tres números: `2.0` (súper efectivo), `0.5` (poco efectivo) o `1.0` (normal, ni fu ni fa).

Este documento construye esa tabla. Es la primera pieza del proyecto porque todo lo demás (la fórmula de daño, la batalla) la usa.

## Schema / Modelo mental (diagrama ASCII)

Piensa en una **rejilla**. Las filas son el tipo que ataca. Las columnas son el tipo que defiende. La casilla donde se cruzan es el multiplicador.

```
                          DEFENSOR
              Normal  Fire  Water  Grass  Electric  Rock
            +--------------------------------------------+
   Normal   |  1.0   1.0   1.0    1.0    1.0      1.0    |
   Fire     |  1.0   0.5   0.5    2.0    1.0      0.5    |
A  Water    |  1.0   2.0   0.5    0.5    1.0      2.0    |
T  Grass    |  1.0   0.5   2.0    0.5    1.0      2.0    |
A  Electric |  1.0   1.0   2.0    0.5    0.5      1.0    |
C  Rock     |  1.0   2.0   0.5    0.5    2.0      0.5    |
A           +--------------------------------------------+
N
T  Lectura: fila Fire, columna Grass -> 2.0 (Fuego quema Planta)
           fila Fire, columna Water  -> 0.5 (Agua apaga Fuego)
           cualquier casilla no marcada como 2.0/0.5 -> 1.0
```

Casi todas las casillas son `1.0`. Solo unas pocas son interesantes (`2.0` o `0.5`). Esa observación es clave: en vez de escribir las 36 casillas, **solo escribimos las excepciones** y asumimos `1.0` por defecto.

## De la rejilla al código: diccionario de diccionarios

Una rejilla con etiquetas en filas y columnas se traduce de forma natural a un **diccionario cuyas claves son diccionarios**. La clave externa es el tipo atacante. El valor es otro diccionario: clave = tipo defensor, valor = multiplicador.

```
TYPE_CHART = {
    "Fire": {            <- atacante Fire
        "Grass": 2.0,    <-   contra Grass: x2
        "Water": 0.5,    <-   contra Water: x0.5
        "Rock":  0.5,
        "Fire":  0.5,
    },
    "Water": {
        "Fire": 2.0,
        "Rock": 2.0,
        "Water": 0.5,
        "Grass": 0.5,
    },
    ...
}
```

Fíjate en que dentro de `"Fire"` **no aparecen** `Normal`, `Electric`. Eso es deliberado: no las escribimos porque su multiplicador es `1.0`, el valor por defecto. La tabla solo contiene las relaciones que NO son neutrales.

### Por qué "solo las excepciones"

Si escribiéramos las 36 casillas, el 70% serían `1.0` repetido y la tabla sería ruidosa y fácil de equivocar. Guardando solo lo que se desvía de lo normal, la estructura grita "estas son las reglas que importan". Cuando preguntemos por una combinación que no está, contestamos `1.0` sin haberla escrito nunca.

## La función `effectiveness`

Necesitamos una función que, dados dos tipos, devuelva el multiplicador. Su trabajo es: buscar el tipo atacante en la tabla, dentro buscar el tipo defensor, y si en cualquiera de los dos pasos no encuentra nada, devolver `1.0`.

```
effectiveness(attack_type, defender_type) -> float

  paso 1: ¿existe attack_type como clave externa?
            no  -> devolver 1.0
            si  -> tengo el sub-diccionario de ese atacante
  paso 2: ¿existe defender_type dentro de ese sub-diccionario?
            no  -> devolver 1.0
            si  -> devolver ese multiplicador
```

El doble "si no, 1.0" es exactamente lo que `dict.get(clave, valor_por_defecto)` hace en una sola línea por nivel.

## Sintaxis Python (al final)

`dict.get(clave, default)` busca `clave` en el diccionario. Si está, devuelve su valor. Si no está, devuelve `default` en vez de lanzar error.

```python
chart = {"Fire": {"Grass": 2.0}}

chart.get("Fire", {})        # -> {"Grass": 2.0}  (existe)
chart.get("Water", {})       # -> {}              (no existe -> default)
```

Encadenando dos `.get()` resolvemos los dos niveles:

```python
def effectiveness(attack_type: str, defender_type: str) -> float:
    return TYPE_CHART.get(attack_type, {}).get(defender_type, 1.0)
```

Línea a línea:
- `TYPE_CHART.get(attack_type, {})` -> el sub-diccionario del atacante, o `{}` si ese tipo no tiene reglas especiales.
- `.get(defender_type, 1.0)` -> el multiplicador contra ese defensor, o `1.0` si no hay regla especial.

El default del primer `.get()` es `{}` (un dict vacío) precisamente para que el segundo `.get()` pueda llamarse sin romper: buscar cualquier cosa en `{}` siempre devuelve el default `1.0`.

## Gotchas / Anti-patterns (tabla)

| Anti-pattern | Síntoma | Fix |
|---|---|---|
| Escribir las 36 casillas a mano | Tabla enorme, `1.0` repetido, errores de tecleo | Solo las excepciones (`2.0` / `0.5`), `1.0` por defecto |
| `TYPE_CHART[attack_type][defender_type]` | `KeyError` cuando la combinación no está escrita | `.get(..., {}).get(..., 1.0)` |
| Primer `.get()` con default `1.0` | `1.0.get(...)` -> `AttributeError` (un float no tiene `.get`) | El default del primer nivel debe ser `{}`, no `1.0` |
| Tipos como `"fire"` vs `"Fire"` | `.get` no encuentra nada -> todo `1.0` | Usar exactamente las etiquetas del CANON: `Fire`, `Water`... (mayúscula inicial) |
| Invertir atacante/defensor | Daño al revés (Agua "débil" contra Fuego) | Orden fijo: `effectiveness(tipo_del_movimiento, tipo_del_pokemon_que_recibe)` |
| Meter `0.0` para "inmune" | El proyecto NO tiene inmunidades; rompe tests | Solo existen `2.0`, `0.5`, `1.0` |

## Tu turno

Abre `pokemon/types.py` (créalo si no existe) e implementa:

1. La constante `TYPE_CHART` como dict de dicts, conteniendo SOLO las relaciones no neutrales del CANON:
   - `Fire`: `>Grass` 2.0; `<Water` `<Rock` `<Fire` 0.5
   - `Water`: `>Fire` `>Rock` 2.0; `<Water` `<Grass` 0.5
   - `Grass`: `>Water` `>Rock` 2.0; `<Fire` `<Grass` 0.5
   - `Electric`: `>Water` 2.0; `<Grass` `<Electric` 0.5
   - `Rock`: `>Fire` `>Electric` 2.0; `<Water` `<Grass` 0.5
   - `Normal`: ninguna relación especial (todo 1.0)
2. La función `effectiveness(attack_type: str, defender_type: str) -> float` con el doble `.get()`.

Comando de test exacto:

```
python -m pytest tests/test_types.py -q
```

Cuando esté en verde, el resto del proyecto puede preguntar "¿cuánto multiplica este ataque?" sin pensar en casos especiales.

## Conexiones

- [[09-la-formula-de-dano]] — la fórmula de daño llama a `effectiveness()` para el término `mult`.
- [[10-el-bucle-de-batalla]] — cada turno aplica daño, que depende de esta tabla.
- Ruta futura: `pokemon/types.py` (constante `TYPE_CHART`, función `effectiveness`).
- Test: `tests/test_types.py`.

## Resumen mental

> La tabla de tipos es una rejilla atacante x defensor donde cada casilla es un multiplicador de daño: `2.0` súper efectivo, `0.5` poco efectivo, `1.0` neutral. La representamos como diccionario de diccionarios (`TYPE_CHART`): clave externa = tipo del movimiento, clave interna = tipo del Pokémon defensor, valor = multiplicador. Truco central: escribir SOLO las casillas no neutrales (las `2.0` y `0.5`) y tratar todo lo ausente como `1.0`. Así la estructura solo contiene las reglas que importan. La función `effectiveness(attack_type, defender_type)` resuelve cualquier consulta con dos `.get()` encadenados: `TYPE_CHART.get(attack_type, {}).get(defender_type, 1.0)`. El default del primer nivel es `{}` (no `1.0`) para que el segundo `.get()` no rompa. Cuidado con mayúsculas exactas (`Fire`, no `fire`) y con no invertir atacante/defensor. No hay inmunidades (`0.0`) en este proyecto. Es la primera pieza porque la fórmula de daño y el bucle de batalla dependen de ella.
