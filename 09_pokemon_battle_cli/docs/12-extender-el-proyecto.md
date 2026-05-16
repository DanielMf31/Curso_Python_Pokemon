---
title: Extender el proyecto sin romper la simplicidad
date: 2026-05-16
tags: [programacion/python, build-things, pokemon-cli, teaching]
type: doc
status: vivo
source: claude-code
---
# Extender el proyecto: del Python básico a algo un poco más avanzado

## Por qué importa

Ya tienes una batalla Pokémon funcionando en la terminal. La tentación natural es pensar "¿y ahora qué? ¿le meto una base de datos? ¿una API? ¿lo hago multijugador online?". No. Todo eso introduce tecnologías completamente nuevas (SQL, redes, async) que no tienen nada que ver con aprender Python y que convertirían un proyecto limpio en un monstruo.

La forma sana de crecer es la contraria: coger el código que ya entiendes y añadirle capas pequeñas, cada una de las cuales te enseña un concepto nuevo de Python o de diseño, sin salir nunca de la librería estándar (stdlib). Vas a seguir teniendo un programa que se ejecuta con `python main.py` y que cualquiera puede leer de arriba a abajo.

Esta guía es el mapa de ese crecimiento. No es código para copiar: es la lista de "siguientes peldaños" ordenados por dificultad, diciéndote en cada uno qué concepto nuevo aprendes y qué fichero del paquete tocas.

## Schema / Modelo mental

Antes de extender nada, ten clara la forma del proyecto. Esta es la estructura canónica que vamos a respetar siempre:

```
pokemon/
    __init__.py
    types.py      # TYPE_CHART: qué tipo es fuerte/débil contra qué
    move.py       # clase Move
    pokemon.py    # clase Pokemon
    data.py       # los 10 Pokémon y sus movimientos predefinidos
    battle.py     # el bucle de combate (turnos, daño, victoria)
    ui.py         # entrada/salida por terminal (texto, menús)
main.py           # punto de entrada: arma una batalla y la lanza
tests/            # pruebas automáticas
run_tests.py      # lanza los tests aunque no tengas pytest instalado
```

La regla mental para decidir si una extensión es "sana":

> Una extensión es buena si se apoya en una pieza que ya existe y solo añade un concepto nuevo. Es mala si te obliga a meter una tecnología externa (base de datos, servidor, librería de terceros) para que funcione.

Las extensiones de esta guía van de menos a más, y cada una se construye sobre la anterior. No saltes: la persistencia JSON (la primera) es el escalón que te abre la puerta a guardar equipos, partidas y progreso en las siguientes.

## Tabla de extensiones por dificultad

| ID | Extensión | Dificultad | Concepto Python nuevo | Fichero(s) a tocar |
|----|-----------|------------|------------------------|--------------------|
| a | Persistencia con JSON | Baja | Módulo json: serializar/deserializar a fichero | nuevo pokemon/storage.py, main.py |
| b | Equipos de varios Pokémon + cambiar | Media | Listas de objetos, gestión de estado, índices | battle.py, ui.py |
| c | Ítems / pociones que curan | Media | Diccionarios como inventario, mutar atributos | pokemon.py, battle.py, ui.py |
| d | Estados alterados (quemado, paralizado) | Media-alta | Más condicionales, atributo de estado, efectos por turno | pokemon.py, battle.py |
| e | IA del rival por efectividad de tipo | Alta | Recorrer y puntuar opciones, max con clave | battle.py, types.py |
| f | Golpes críticos y STAB | Media | Aleatoriedad controlada, multiplicadores en el cálculo | pokemon.py o battle.py |

A continuación, una subsección por extensión. Cada una explica el concepto antes que el código.

## (a) Persistencia con JSON — el primer escalón

### El problema

Ahora mismo, cuando cierras el programa, todo desaparece. No puedes guardar tu Pokémon favorito, ni un equipo, ni el resultado de una batalla. Queremos poder escribir datos en un fichero y volver a leerlos la próxima vez.

### Concepto nuevo: el módulo json

JSON es simplemente un formato de texto para representar datos: números, cadenas, listas y diccionarios. Python trae en su librería estándar el módulo json, que hace dos cosas:

- Serializar (json.dump): coger un diccionario o lista de Python y escribirlo como texto en un fichero.
- Deserializar (json.load): leer ese texto del fichero y reconstruir el diccionario o lista.

El truco mental clave: json solo entiende tipos básicos (números, cadenas, booleanos, listas, diccionarios, None). NO entiende tus objetos Pokemon o Move directamente. Por eso necesitas dos funciones puente: una que convierta un Pokemon en un diccionario sencillo, y otra que reconstruya un Pokemon a partir de ese diccionario.

```python
# pokemon/storage.py  (fichero nuevo)
import json

def pokemon_to_dict(pokemon):
    # Convierte un Pokemon en un diccionario que json si entiende.
    return {
        "name": pokemon.name,
        "type": pokemon.type,
        "max_hp": pokemon.max_hp,
        "attack": pokemon.attack,
        "defense": pokemon.defense,
        "level": pokemon.level,
        "moves": [m.name for m in pokemon.moves],
    }

def save_team(team, path):
    data = [pokemon_to_dict(p) for p in team]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
```

Para cargar, lees el fichero con json.load y vuelves a construir los objetos usando los datos que ya tienes en data.py. (La reconstrucción exacta es parte del reto D1.)

### Por qué este es el primer escalón

Una vez sabes pasar objetos a fichero y de vuelta, todas las demás extensiones que necesiten "guardar" algo (equipos, progreso) se apoyan en esto. Es la pieza base.

Fichero a tocar: crea pokemon/storage.py, y en main.py añade la opción de guardar/cargar antes de empezar la batalla.

## (b) Equipos de varios Pokémon y cambiar en combate

### Concepto nuevo: una lista de objetos como estado de juego

Hasta ahora cada lado de la batalla tenía un Pokémon. Un equipo es simplemente una list de objetos Pokemon. Lo nuevo no es la lista en sí, sino mantener qué Pokémon está activo y permitir cambiarlo.

El modelo mental: en lugar de player_pokemon, tienes player_team (una lista) y player_active_index (un entero que dice cuál está luchando). Cambiar de Pokémon es cambiar ese índice, y consume el turno.

```python
player_team = [bulbasaur, charmander, squirtle]
player_active_index = 0
active = player_team[player_active_index]   # el que pelea ahora
```

La condición de derrota deja de ser "mi Pokémon está debilitado" y pasa a ser "todos los Pokémon de mi equipo están debilitados". Eso es un bucle que comprueba cada elemento de la lista.

Ficheros a tocar: battle.py (estado del equipo, lógica de cambio, condición de victoria) y ui.py (un menú para elegir a quién sacar).

## (c) Ítems y pociones que curan

### Concepto nuevo: un diccionario como inventario

Un inventario es un diccionario {nombre_item: cantidad}. Una poción es un efecto que muta un atributo de un objeto: sube el hp actual del Pokémon activo sin pasarse de max_hp.

```python
inventory = {"potion": 2, "super_potion": 1}

def use_potion(pokemon, amount):
    pokemon.hp = min(pokemon.hp + amount, pokemon.max_hp)
```

Lo que practicas aquí: leer y modificar un diccionario (restar 1 a la cantidad cuando se usa) y mutar el estado de un objeto de forma controlada (el min evita curar de más). Usar un ítem consume el turno, igual que cambiar de Pokémon.

Ficheros a tocar: pokemon.py (asegúrate de que el Pokémon tiene hp actual separado de max_hp), battle.py (gastar el turno, descontar del inventario) y ui.py (menú de ítems).

## (d) Estados alterados simples: quemado y paralizado

### Concepto nuevo: un atributo de estado y más condicionales

Un estado alterado es un atributo extra en el Pokémon, por ejemplo status, que vale None, "burned" o "paralyzed". La gracia es que cada turno se comprueba ese estado y se aplica un efecto:

- Quemado (burned): al final del turno, el Pokémon pierde un poco de HP.
- Paralizado (paralyzed): antes de atacar, hay cierta probabilidad de que el Pokémon "no se mueva" y pierda el turno.

Esto es básicamente entrenar condicionales: if status == "burned": ..., if status == "paralyzed" and random_check: .... No hay tecnología nueva, solo lógica más rica dentro del bucle de combate que ya tienes.

Ficheros a tocar: pokemon.py (añadir el atributo status) y battle.py (revisar el estado en el momento adecuado de cada turno).

## (e) IA del rival que elige el movimiento más efectivo

### Concepto nuevo: puntuar opciones y elegir la mejor

Hasta ahora el rival probablemente elige un movimiento al azar. Una IA "lista" recorre todos sus movimientos, calcula para cada uno cuán efectivo sería contra el tipo del Pokémon enemigo (consultando TYPE_CHART), y se queda con el de mayor puntuación.

El patrón Python que practicas es "recorrer una lista calculando un valor por elemento y quedarte con el máximo":

```python
def choose_best_move(attacker, defender):
    def score(move):
        return type_multiplier(move.type, defender.type) * move.power
    return max(attacker.moves, key=score)
```

max(..., key=score) significa "dame el elemento cuya score sea mayor". Es el mismo concepto que ordenar por una clave, pero quedándote solo con el primero.

Ficheros a tocar: battle.py (donde el rival decide su movimiento) apoyándose en la función de multiplicador de types.py.

## (f) Golpes críticos y STAB

### Concepto nuevo: aleatoriedad controlada y multiplicadores apilados

Dos mejoras clásicas al cálculo de daño que ya tienes:

- Crítico: con cierta probabilidad pequeña (por ejemplo, 1 de cada 16), el daño se multiplica por 1.5 o 2. Usas el módulo random de stdlib para "tirar el dado".
- STAB (Same-Type Attack Bonus): si el tipo del movimiento coincide con el tipo del Pokémon que ataca, el daño se multiplica por 1.5. Es solo una comparación más.

Lo que aprendes es a encadenar multiplicadores en la fórmula de daño de forma ordenada (base x tipo x STAB x crítico) y a usar aleatoriedad sin que el juego se vuelva imposible de testear (de ahí la importancia de poder fijar una semilla en los tests).

Ficheros a tocar: la función que calcula el daño (en pokemon.py o battle.py, según dónde la tengas).

## Conexiones

- [[09-tests-y-tdd]] — toda extensión debe venir con su test antes de darla por buena
- [[challenges]] — la categoría D convierte estas extensiones en retos guiados (D1..D8)
- [[glosario]] — términos como serializar, multiplicador de tipo, semilla
- [[MOC_Programacion]]

## Resumen mental

> No crezcas hacia afuera (bases de datos, redes): crece hacia adentro. Coge una pieza que ya entiendes y añádele un concepto Python nuevo. La persistencia JSON es el primer escalón porque cualquier "guardar" futuro se apoya en ella. Cada extensión = un concepto + un fichero, sin salir de la stdlib.
