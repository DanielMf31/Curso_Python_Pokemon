---
title: Glosario español-inglés del proyecto Pokémon CLI
date: 2026-05-16
tags: [programacion/python, build-things, pokemon-cli, teaching]
type: doc
status: vivo
source: claude-code
---
# Glosario español-inglés

## Por qué importa

Casi toda la documentación, los errores de Python y el código del mundo real están en inglés, pero piensas en español. Este glosario es tu diccionario de ida y vuelta: cada término aparece con su nombre en inglés, una definición en lenguaje llano (sin asumir que ya sabes programar) y un ejemplo sacado de este mismo proyecto Pokémon, para que el concepto tenga un anclaje concreto.

Úsalo como referencia: cuando una guía mencione un término que no recuerdas, búscalo aquí.

## Schema / Modelo mental

Los términos se agrupan mentalmente en tres familias:

- Cosas que guardan datos: variable, tipos, lista, diccionario, tupla.
- Cosas que ejecutan lógica: condicional, bucle, función, parámetro, argumento, return.
- Cosas que organizan el código: clase, objeto, atributo, método, módulo, paquete, import.

El resto son herramientas del entorno (terminal, venv, test) o conceptos propios del juego (TYPE_CHART, PP, STAB...). Están todos en orden alfabético abajo.

## Glosario alfabético

- accuracy (precisión) — Probabilidad de que un movimiento acierte en lugar de fallar. Ejemplo: un movimiento con accuracy 90 acierta aproximadamente 9 de cada 10 veces.
- argumento (argument) — El valor concreto que le pasas a una función cuando la llamas. Ejemplo: en `attack(charmander)`, charmander es el argumento.
- assert — Instrucción que dice "esto tiene que ser verdad; si no, falla". Es la base de los tests. Ejemplo: `assert damage > 0` comprueba que un ataque hace al menos algo de daño.
- atributo (attribute) — Un dato que pertenece a un objeto. Ejemplo: el atributo `hp` de un Pokémon guarda su vida actual.
- bucle (loop) — Repetir un bloque de código varias veces. Ejemplo: el bucle de combate repite "turno tras turno" hasta que un Pokémon cae.
- bool (booleano) — Tipo de dato que solo vale True o False. Ejemplo: `is_fainted` es True cuando el Pokémon está debilitado.
- clase (class) — Un molde para crear objetos del mismo tipo. Ejemplo: la clase Pokemon define cómo es cualquier Pokémon; Pikachu es uno hecho con ese molde.
- condicional (conditional / if) — Código que solo se ejecuta si se cumple una condición. Ejemplo: `if hp <= 0: print("debilitado")`.
- diccionario (dict) — Colección de pares clave-valor; buscas por la clave. Ejemplo: TYPE_CHART es un diccionario donde la clave es un tipo y el valor son sus multiplicadores.
- entorno virtual / venv (virtual environment) — Una "caja" aislada de Python por proyecto, para que las librerías de uno no choquen con las de otro. Ejemplo: activas el .venv antes de lanzar los tests.
- f-string — Cadena de texto que mete valores dentro con llaves. Ejemplo: `f"{pokemon.name} usa {move.name}"` produce "Pikachu usa Thunderbolt".
- float (decimal) — Tipo de dato para números con parte decimal. Ejemplo: el multiplicador de tipo 2.0 o 0.5 es un float.
- función (function) — Un bloque de código con nombre que hace una tarea y opcionalmente devuelve algo. Ejemplo: `calculate_damage(...)` calcula el daño de un golpe.
- import — Traer código de otro módulo o paquete para usarlo aquí. Ejemplo: `from pokemon.data import POKEMONS`.
- `__init__` — Método especial que se ejecuta al crear un objeto; suele asignar sus atributos iniciales. Ejemplo: el `__init__` de Pokemon recibe name, type, max_hp...
- `__init__.py` — Fichero (puede estar vacío) que convierte una carpeta en un paquete importable. Ejemplo: pokemon/__init__.py hace que `import pokemon` funcione.
- int (entero) — Tipo de dato para números sin decimales. Ejemplo: el atributo `level` de un Pokémon es un int.
- instancia (instance) — Ver objeto. Un objeto concreto creado a partir de una clase. Ejemplo: charmander es una instancia de Pokemon.
- KO / debilitado (fainted / knocked out) — Estado de un Pokémon cuando su hp llega a 0 y no puede seguir luchando. Ejemplo: cuando squirtle queda KO, debes sacar otro Pokémon.
- lista (list) — Colección ordenada de elementos a la que puedes acceder por posición. Ejemplo: los movimientos de un Pokémon son una lista de objetos Move.
- método (method) — Una función que pertenece a una clase y opera sobre el objeto. Ejemplo: `pokemon.take_damage(10)` es un método que baja su hp.
- módulo (module) — Un fichero .py con código reutilizable. Ejemplo: types.py es el módulo que contiene la tabla de tipos.
- multiplicador de tipo (type multiplier) — Número por el que se multiplica el daño según la ventaja de tipos: 2.0 muy eficaz, 0.5 poco eficaz, 1.0 normal. Ejemplo: Water contra Fire da 2.0.
- NotImplementedError — Error que lanzas a propósito en un esqueleto para marcar "esto aún hay que escribirlo". Ejemplo: una función con `raise NotImplementedError` recuerda que es un TODO de la práctica.
- objeto / instancia (object / instance) — Una "cosa" concreta creada a partir de una clase, con sus propios datos. Ejemplo: pikachu es un objeto de la clase Pokemon.
- parámetro (parameter) — El nombre que aparece en la definición de una función para recibir un valor. Ejemplo: en `def attack(target):`, target es el parámetro.
- paquete (package) — Una carpeta con un `__init__.py` que agrupa varios módulos relacionados. Ejemplo: pokemon/ es el paquete con types, move, pokemon, etc.
- PP (Power Points) — Número de veces que un movimiento se puede usar antes de agotarse. Ejemplo: un movimiento con pp 15 se puede lanzar 15 veces por combate.
- pytest — Herramienta que ejecuta los tests automáticamente y te dice cuáles pasan y cuáles fallan. Ejemplo: `pytest` recorre la carpeta tests/.
- return — Palabra que hace que una función devuelva un valor a quien la llamó. Ejemplo: `return damage` entrega el daño calculado.
- self — Dentro de un método, la palabra que se refiere al propio objeto sobre el que se actúa. Ejemplo: `self.hp -= amount` baja la vida de este Pokémon concreto.
- semilla / seed — Número que fija el azar para que `random` produzca siempre la misma secuencia; imprescindible para tests reproducibles. Ejemplo: con la misma semilla, un crítico ocurre siempre en el mismo turno.
- stdlib (standard library / librería estándar) — El conjunto de módulos que vienen con Python sin instalar nada. Ejemplo: json y random son stdlib; por eso el proyecto no necesita pip.
- str (cadena / string) — Tipo de dato para texto. Ejemplo: el atributo `name` "Pikachu" es un str.
- `__str__` — Método especial que define cómo se ve un objeto cuando lo imprimes. Ejemplo: el `__str__` de Pokemon devuelve "Pikachu (Electric) HP 35/35".
- terminal (terminal / shell) — La ventana de texto donde escribes comandos. Ejemplo: lanzas el juego con `python main.py` en la terminal.
- test (test / prueba) — Código que comprueba automáticamente que otro código funciona. Ejemplo: un test verifica que Water hace 2.0 de multiplicador contra Fire.
- tupla (tuple) — Colección ordenada como una lista, pero que no se puede modificar. Ejemplo: un par (atacante, defensor) que no debe cambiar puede ser una tupla.
- TYPE_CHART — Diccionario del proyecto que define qué tipo es fuerte, débil o normal contra qué otro. Ejemplo: TYPE_CHART dice que Fire es eficaz contra Grass.
- variable — Un nombre que apunta a un valor guardado en memoria. Ejemplo: `damage = 12` guarda el daño en la variable damage.
- varianza (variance) — Cuánto varía un resultado por el azar (por ejemplo, el daño no siempre es idéntico). Ejemplo: un golpe puede hacer entre 10 y 12 por una pequeña varianza aleatoria.

## Conexiones

- [[12-extender-el-proyecto]] — usa estos términos al describir cada extensión
- [[challenges]] — los retos asumen que entiendes este vocabulario
- [[MOC_Programacion]]

## Resumen mental

> Un objeto guarda datos (atributos) y sabe hacer cosas (métodos); su molde es la clase. Los datos viven en variables de distintos tipos (int, str, float, bool) y en colecciones (lista, diccionario, tupla). El código se organiza en módulos dentro de paquetes y se reutiliza con import. Lo demás (TYPE_CHART, PP, STAB, semilla) es vocabulario propio de este juego.
