---
title: Retos opcionales (categoría D) del Pokémon Battle CLI
date: 2026-05-16
tags: [programacion/python, build-things, pokemon-cli, teaching]
type: doc
status: vivo
source: claude-code
---
# Retos opcionales — Categoría D

## Por qué importa

La suite de tests base te garantiza que el juego funciona. Estos retos son el siguiente nivel: cada uno te hace añadir una funcionalidad real practicando un concepto Python concreto, con pistas pero sin la solución delante. Es donde el aprendizaje se consolida, porque construyes tú.

Importante: estos retos son OPCIONALES y solo se abordan cuando la suite base esté completamente en verde (todos los tests pasan). Para cada reto existe una solución de referencia gated en `docs/soluciones/` — mírala solo después de intentarlo de verdad, nunca antes.

## Schema / Modelo mental

Cada reto sigue siempre la misma ficha:

- ID: identificador D1..D8.
- Dificultad: orientativa, de baja a alta.
- Concepto Python: la habilidad concreta que entrenas.
- Enunciado: qué hay que conseguir.
- Pistas: 1 a 3 empujones, en orden creciente; usa solo las que necesites.
- Criterio de "hecho": cómo sabes objetivamente que está terminado (un test que pasa o una verificación manual concreta).

Los retos están ordenados: D1 (persistencia) es la base sobre la que se apoyan varios de los siguientes. Síguelos en orden salvo que ya domines el concepto.

## D1 — Guardar y cargar un equipo en JSON

- Dificultad: baja.
- Concepto Python: módulo json de stdlib, serializar y deserializar a fichero.
- Enunciado: crea `pokemon/storage.py` con `save_team(team, path)` y `load_team(path)`. Guardar escribe la lista de Pokémon como JSON; cargar la lee y reconstruye objetos Pokemon válidos usando los datos de data.py.
- Pistas:
  1. json no entiende objetos: convierte cada Pokemon a un diccionario con sus atributos antes de json.dump.
  2. Al cargar, recorre la lista de diccionarios y vuelve a crear cada Pokemon; los movimientos puedes buscarlos por nombre en data.py.
  3. Abre los ficheros con `with open(path, "w", encoding="utf-8")` para escribir y `"r"` para leer.
- Criterio de hecho: un test que guarda un equipo, lo carga y comprueba que los Pokémon recuperados tienen el mismo name, type y max_hp que los originales.

## D2 — Equipo de 3 Pokémon con cambio en combate

- Dificultad: media.
- Concepto Python: listas de objetos y gestión de un índice de estado.
- Enunciado: cada lado de la batalla tiene una lista de 3 Pokémon y un índice del activo. El jugador puede usar el turno para cambiar de Pokémon. Se pierde cuando los 3 están debilitados.
- Pistas:
  1. Sustituye la variable de un solo Pokémon por team (lista) y active_index (int).
  2. Cambiar de Pokémon consume el turno igual que atacar.
  3. La condición de derrota es "todos los del equipo tienen hp <= 0": un bucle o `all(...)` sobre la lista.
- Criterio de hecho: verificación manual — al quedar KO el Pokémon activo el juego obliga a elegir otro, y la partida solo termina cuando caen los 3.

## D3 — Pociones que curan

- Dificultad: media.
- Concepto Python: diccionario como inventario y mutación controlada de atributos.
- Enunciado: añade un inventario `{"potion": n}`. Usar una poción cura una cantidad fija de hp al Pokémon activo sin superar max_hp, descuenta 1 del inventario y consume el turno.
- Pistas:
  1. Usa min(pokemon.hp + cantidad, pokemon.max_hp) para no curar de más.
  2. Si la cantidad en el inventario es 0, la opción no debe estar disponible.
- Criterio de hecho: un test que, con un Pokémon dañado, aplica una poción y comprueba que hp sube pero nunca pasa de max_hp, y que el contador del inventario baja en 1.

## D4 — Estado alterado "quemado"

- Dificultad: media-alta.
- Concepto Python: atributo de estado y condicionales aplicados cada turno.
- Enunciado: un movimiento puede dejar al rival con status "burned". Mientras esté quemado, al final de cada uno de sus turnos pierde una pequeña cantidad fija de hp.
- Pistas:
  1. Añade un atributo status (None por defecto) a Pokemon.
  2. El daño por quemado se aplica al final del turno, después de atacar, y también puede dejarlo KO.
- Criterio de hecho: un test que pone status = "burned", simula un turno y comprueba que el hp bajó por el quemado además del daño normal.

## D5 — IA del rival por efectividad de tipo

- Dificultad: alta.
- Concepto Python: recorrer y puntuar opciones, max con función clave.
- Enunciado: el rival deja de elegir al azar; recorre sus movimientos, puntúa cada uno por multiplicador de tipo contra el Pokémon del jugador, y usa el de mayor puntuación.
- Pistas:
  1. Define una función score(move) que devuelva multiplicador_de_tipo * move.power.
  2. `max(moves, key=score)` te da directamente el mejor movimiento.
  3. No olvides ignorar movimientos sin PP disponible.
- Criterio de hecho: un test donde, ante un Pokémon de tipo Grass, el rival con un movimiento Fire y otro Normal elige siempre el Fire.

## D6 — Golpes críticos

- Dificultad: media.
- Concepto Python: aleatoriedad controlada con random y semilla reproducible.
- Enunciado: cada ataque tiene una probabilidad pequeña (ej. 1/16) de ser crítico y multiplicar el daño (ej. x1.5). El cálculo debe poder testearse fijando la semilla.
- Pistas:
  1. Usa random.random() < 1/16 para decidir el crítico.
  2. En el test, llama a random.seed(...) con un valor que fuerce un crítico conocido.
- Criterio de hecho: un test que, con una semilla fija, comprueba que el daño es exactamente el esperado con crítico aplicado.

## D7 — Añadir un tipo nuevo al TYPE_CHART

- Dificultad: media.
- Concepto Python: extender un diccionario de datos manteniendo la coherencia.
- Enunciado: añade un séptimo tipo (por ejemplo Ice) a TYPE_CHART, definiendo sus relaciones de eficacia con los seis tipos existentes y las de ellos contra Ice. Crea al menos un Pokémon y un movimiento de ese tipo en data.py.
- Pistas:
  1. Toca solo types.py para las relaciones y data.py para el nuevo Pokémon/movimiento.
  2. Revisa que TODOS los pares (Ice vs X y X vs Ice) estén definidos; un hueco causará multiplicador incorrecto o error.
- Criterio de hecho: un test que comprueba al menos dos relaciones nuevas del tipo Ice (una eficaz y una poco eficaz) y que un combate con el Pokémon nuevo no lanza errores.

## D8 — Inmunidades (multiplicador 0.0) y su manejo

- Dificultad: alta.
- Concepto Python: caso límite en una fórmula numérica y condicionales de borde.
- Enunciado: introduce relaciones de inmunidad donde el multiplicador de tipo es 0.0 (el movimiento no afecta). El combate debe informar "no afecta" y no restar hp ni gastar el turno de forma confusa.
- Pistas:
  1. Añade algún par con valor 0.0 en TYPE_CHART.
  2. Detecta el caso antes de calcular daño: si el multiplicador es 0.0, salta el mensaje "no afecta" y aplica 0 de daño.
  3. Cuida que un daño 0 no provoque divisiones ni mínimos raros en la fórmula.
- Criterio de hecho: un test que, con un par inmune, comprueba que el daño es exactamente 0 y que el hp del defensor no cambia.

## Conexiones

- [[12-extender-el-proyecto]] — la teoría detrás de cada reto
- [[09-tests-y-tdd]] — escribe el test antes de dar el reto por hecho
- [[glosario]] — vocabulario que asumen los enunciados
- [[MOC_Programacion]]

## Resumen mental

> Cada reto = un concepto Python + un criterio objetivo de "hecho". Son opcionales y solo después de tener la suite base verde. D1 (JSON) es la base de varios; sigue el orden. Intenta primero, mira la solución gated en docs/soluciones/ solo después.
