---
title: 06 — Clases y objetos
date: 2026-05-16
tags: [programacion/python, programacion/oop, build-things, pokemon-cli, teaching]
type: doc
status: vivo
source: claude-code
---

# 06 — Clases y objetos: el molde y el Pokémon concreto

## Por qué importa

Hasta ahora, cuando querías representar un Pokémon, probablemente habrías usado un diccionario suelto: `{"name": "Pikachu", "hp": 35, "attack": 55}`. Funciona para uno. Pero en una batalla tienes dos Pokémon, cada uno con cuatro movimientos, y a cada uno le baja la vida en cada turno. Con diccionarios sueltos, la lógica de "bajar vida" vive desperdigada por todo el código: una resta aquí, una comprobación de "¿se debilitó?" allá. Cada vez que tocas un Pokémon tienes que recordar las reglas tú mismo.

Una **clase** resuelve esto juntando dos cosas que siempre van de la mano: los **datos** de un Pokémon (su nombre, su vida, su ataque) y las **operaciones** que se le pueden hacer (recibir daño, comprobar si está debilitado). En vez de "un diccionario más una pila de funciones que esperan que el diccionario tenga las claves correctas", tienes un objeto que sabe qué es y qué se le puede pedir.

Este es el doc base de todo el motor de batalla. `Move`, `Pokemon` y más adelante `Battle` son clases. Si este modelo mental queda firme, el resto es repetición.

## Schema / Modelo mental

La distinción central, antes que cualquier sintaxis:

```
        CLASE (el molde)                       OBJETOS / INSTANCIAS (lo fabricado)
   ┌───────────────────────┐
   │ class Pokemon          │   ──fabrica──►   ┌──────────────────────────┐
   │                        │                  │ pikachu                  │
   │ "todo Pokémon TIENE:"  │                  │  name    = "Pikachu"     │
   │   - name               │                  │  type    = "Electric"    │
   │   - type               │                  │  max_hp  = 35            │
   │   - max_hp             │                  │  hp      = 35            │
   │   - hp                 │                  │  attack  = 55            │
   │   - attack             │                  └──────────────────────────┘
   │   - defense            │
   │   - level              │   ──fabrica──►   ┌──────────────────────────┐
   │                        │                  │ charmander               │
   │ "todo Pokémon SABE:"   │                  │  name    = "Charmander"  │
   │   - take_damage(n)     │                  │  type    = "Fire"        │
   │   - is_fainted()       │                  │  max_hp  = 39            │
   │                        │                  │  hp      = 39            │
   └───────────────────────┘                  │  attack  = 52            │
                                                └──────────────────────────┘
```

Una sola clase `Pokemon`. Muchos objetos `Pokemon`: `pikachu`, `charmander`, `squirtle`... Cada objeto es **independiente**: si a `pikachu` le bajas la vida, `charmander` ni se entera. Comparten el molde (las mismas reglas, los mismos métodos), pero no los datos.

Frases para fijar el modelo:

- La **clase** es el plano de la casa. El **objeto** es una casa construida.
- La clase es la receta. El objeto es el plato que te comes.
- `class Pokemon` se escribe **una vez**. Objetos `Pokemon` se crean **diez veces** (uno por cada especie en `data.py`).

## Atributos: qué tiene un Pokémon

Un **atributo** es un dato que pertenece a un objeto. `pikachu.name` es el atributo `name` del objeto `pikachu`. Se accede con un punto: `objeto.atributo`.

```python
pikachu.name      # "Pikachu"     ── leer
pikachu.hp        # 35            ── leer
pikachu.hp = 20   #               ── escribir (modificar el objeto)
```

Antes de saber crearlos, ten claro qué atributos tendrá cada `Pokemon` según el CANON del proyecto:

| Atributo  | Tipo        | Significado                                   |
|-----------|-------------|-----------------------------------------------|
| `name`    | `str`       | "Pikachu"                                     |
| `type`    | `str`       | uno de los 6 tipos (ver más abajo)            |
| `max_hp`  | `int`       | vida máxima, no cambia                         |
| `hp`      | `int`       | vida actual, baja durante el combate           |
| `attack`  | `int`       | potencia ofensiva                              |
| `defense` | `int`       | reduce el daño recibido                         |
| `level`   | `int`       | nivel del Pokémon                              |
| `moves`   | `list[Move]`| sus movimientos (objetos `Move`)               |

Fíjate en algo clave: `max_hp` y `hp` empiezan iguales (un Pikachu recién creado tiene 35 de 35), pero `hp` está pensado para **cambiar** y `max_hp` para quedarse fijo. Esa diferencia es el corazón del estado mutable, lo vemos al final.

## `__init__`: cómo nace un objeto

Cuando escribes `Pokemon("Pikachu", "Electric", 35, 55, 40, 5, [...])`, Python crea un objeto vacío y acto seguido llama a un método especial llamado `__init__` para rellenarlo. `__init__` es el **constructor**: su único trabajo es poner los atributos iniciales en el objeto recién nacido.

No te enseño todavía cómo se escribe el de `Pokemon` (eso es tu práctica). Te lo enseño con `Move`, que es más pequeño y sirve de plantilla mental. Aquí está la clase `Move` **completa**:

```python
class Move:
    def __init__(self, name, type, power, accuracy, pp, max_pp):
        self.name = name
        self.type = type
        self.power = power
        self.accuracy = accuracy
        self.pp = pp
        self.max_pp = max_pp

    def use(self):
        self.pp -= 1

    def has_pp(self):
        return self.pp > 0
```

Léelo despacio. `__init__` recibe seis datos y los guarda en el objeto. `self.name = name` significa: "el atributo `name` *de este objeto* vale lo que me pasaron en el parámetro `name`". A la izquierda del `=` está el objeto; a la derecha, el dato de entrada. Es normal que el parámetro y el atributo se llamen igual; `self.` desambigua.

## `self`: la pieza que cuesta (vamos muy despacio)

`self` es el concepto que hace tropezar a todo el mundo. Tómatelo con calma.

Mira esta llamada:

```python
pikachu.take_damage(10)
```

Lees: "al objeto `pikachu`, aplícale `take_damage` con 10". Pero el método está definido así (firma de ejemplo, no te doy el cuerpo: es tu práctica):

```python
class Pokemon:
    def take_damage(self, amount):
        ...
```

`take_damage` tiene **dos** parámetros (`self`, `amount`) pero tú lo llamaste con **uno** (`10`). ¿De dónde sale `self`? Python lo rellena automáticamente con el objeto que está a la izquierda del punto. Mentalmente, traduce siempre así:

```
   pikachu.take_damage(10)
        └───── es lo mismo que ─────┐
                                     ▼
   Pokemon.take_damage(pikachu, 10)
                        ▲       ▲
                        │       └── amount = 10
                        └── self = pikachu
```

`self` es **el propio objeto sobre el que llamaste el método**. Dentro de `take_damage`, `self` *es* `pikachu`. Por eso `self.hp` dentro del método significa "el `hp` de `pikachu`". Si en otro turno llamas `charmander.take_damage(10)`, en esa llamada `self` *es* `charmander`, y `self.hp` es el de Charmander. El mismo código de método, distinto objeto cada vez, gracias a `self`.

Regla práctica que no falla: **el primer parámetro de todo método es `self`, siempre, y nunca lo pasas tú al llamar** — Python lo pone solo desde lo que hay antes del punto.

## Métodos: qué sabe hacer un Pokémon

Un **método** es una función que vive dentro de una clase y opera sobre el objeto vía `self`. Ya viste tres en `Move`:

- `use(self)`: gasta un punto de poder. `self.pp -= 1` resta 1 al `pp` *de ese movimiento*.
- `has_pp(self)`: devuelve `True` si todavía quedan usos. `return self.pp > 0` evalúa una comparación y devuelve el booleano resultante.

Para `Pokemon`, el CANON pide dos métodos. Te muestro **uno** entero como ejemplo guía y dejo el otro descrito (para que no se resuelva tu práctica):

```python
class Pokemon:
    def __init__(self, name, type, max_hp, attack, defense, level, moves):
        ...   # tu práctica

    def is_fainted(self):
        return self.hp <= 0
```

`is_fainted` no recibe nada aparte de `self`: solo mira el estado interno (`self.hp`) y responde una pregunta sí/no. "¿Este Pokémon está debilitado?" → `True` si su vida llegó a 0 o menos.

El otro método, `take_damage(self, amount)`, debe **bajar la vida del Pokémon** en función del daño recibido. Modifica `self.hp`. Cómo exactamente (y qué papel juega `defense`) lo decides tú en la práctica; el modelo mental que necesitas ya lo tienes: un método que recibe un número y muta un atributo del objeto.

## Estado mutable: el `hp` que baja

Aquí se junta todo. Un objeto no es una foto fija: sus atributos **cambian con el tiempo**. Eso es *estado mutable*, y es exactamente lo que hace que una batalla sea una batalla.

```
   pikachu = Pokemon("Pikachu", "Electric", 35, 55, 40, 5, [...])

   pikachu.hp          ──►  35      (recién creado: hp == max_hp)
   pikachu.take_damage(10)
   pikachu.hp          ──►  25      (el objeto CAMBIÓ)
   pikachu.take_damage(30)
   pikachu.hp          ──►  -5      (o lo que decida tu lógica)
   pikachu.is_fainted()──►  True    (hp <= 0)
```

`max_hp` sigue valiendo 35 todo el rato: es el techo. `hp` es lo que va cambiando. Dos atributos parecidos con responsabilidades distintas. Y crucial: si tuvieras `charmander` al lado, `charmander.hp` seguiría a 39 — golpear a uno no toca al otro, porque cada objeto tiene su propia copia de los atributos.

`Move.use()` es el mismo patrón: cada vez que un movimiento se usa, *su* `pp` baja un punto, hasta que `has_pp()` devuelve `False` y ya no se puede usar más. Mismo concepto (mutar un atributo del objeto), aplicado a otra clase.

## Sintaxis Python (al final)

Recopilada, ahora que el modelo está claro:

```python
class Move:                              # definir una clase: class + Nombre + :
    def __init__(self, name, power):     # constructor: primer parámetro self
        self.name = name                 # crear/asignar un atributo del objeto
        self.power = power

    def use(self):                       # método: función con self primero
        self.pp -= 1                     # mutar un atributo

    def has_pp(self):
        return self.pp > 0               # un método puede devolver un valor


fire_punch = Move("Fire Punch", 75)      # instanciar: ClaseNombre(args) → objeto
fire_punch.name                          # leer atributo  → "Fire Punch"
fire_punch.use()                         # llamar método  (no pasas self)
fire_punch.has_pp()                      # → True / False
```

Detalles que conviene fijar:

- El nombre de la clase va en `CapWords` (`Pokemon`, `Move`), por convención.
- `__init__` lleva doble guion bajo a cada lado (un *dunder*). No lo llamas tú: se dispara solo al instanciar.
- Dentro de un método, **siempre** usas `self.atributo` para tocar datos del objeto. Sin `self.`, `name` sería una variable local que muere al acabar el método y no quedaría guardada en el objeto.

## `__str__`: cómo se imprime un Pokémon

Si haces `print(pikachu)` sin más, ves algo feo tipo `<__main__.Pokemon object at 0x7f...>`. El método especial `__str__` te deja decidir qué texto representa al objeto:

```python
class Move:
    def __init__(self, name, pp):
        self.name = name
        self.pp = pp

    def __str__(self):
        return f"{self.name} ({self.pp} PP)"


print(Move("Thunderbolt", 15))    # → Thunderbolt (15 PP)
```

`__str__` recibe solo `self`, construye un string con los atributos del objeto y lo **devuelve** (`return`, no `print`). Quien haga `print(...)` o `str(...)` sobre el objeto verá ese texto. Para `Pokemon`, el CANON pide un `__str__`; un formato razonable mostraría el nombre y la vida actual frente a la máxima (por ejemplo `Pikachu HP: 25/35`), pero el contenido exacto lo decides tú en la práctica.

## Gotchas / Anti-patterns

| Error | Síntoma | Causa / Fix |
|---|---|---|
| Olvidar `self` en la firma | `TypeError: take_damage() takes 1 positional argument but 2 were given` | Todo método empieza por `self`: `def take_damage(self, amount):` |
| Olvidar `self.` al asignar | El atributo no se guarda; luego `AttributeError` al leerlo | Dentro de `__init__` usa `self.hp = max_hp`, no `hp = max_hp` |
| Pasar `self` tú al llamar | `TypeError: ... got multiple values for argument` | Llama `pikachu.take_damage(10)`, NUNCA `take_damage(pikachu, 10)` |
| Confundir clase con instancia | Tocas `Pokemon.hp` esperando afectar a un Pokémon concreto | Operas sobre objetos (`pikachu.hp`), no sobre la clase `Pokemon` |
| Creer que los objetos comparten datos | Golpeas a uno y "baja la vida del otro" | Cada objeto tiene atributos propios; comparten métodos, no estado |
| `__str__` con `print` en vez de `return` | `print(pikachu)` muestra `None` | `__str__` debe **devolver** un string con `return` |
| Mutar `max_hp` en vez de `hp` | El techo de vida cambia; curaciones rotas | `take_damage` toca `self.hp`; `max_hp` no se modifica |

## Tu turno

Implementa las dos clases base del motor:

1. **`pokemon/move.py`** — la clase `Move` con `__init__(self, name, type, power, accuracy, pp, max_pp)`, el método `use(self)` (baja `pp` en 1) y `has_pp(self)` (devuelve `bool`: ¿queda `pp`?). La tienes entera más arriba como ejemplo: aquí solo la transcribes a su fichero y la entiendes a fondo.
2. **`pokemon/pokemon.py`** — la clase `Pokemon` con `__init__(self, name, type, max_hp, attack, defense, level, moves)` (recuerda: `self.hp = max_hp` al nacer), el método `take_damage(self, amount)` (baja `self.hp`), `is_fainted(self)` (devuelve `True` si `hp <= 0`) y `__str__(self)`.

Verifica con el comando exacto:

```
python -m pytest tests/test_move.py tests/test_pokemon.py -q
```

Si no tienes pytest disponible, usa el fallback del proyecto: `python run_tests.py`.

## Conexiones

- [[07-imports-y-paquetes]] — `Move` y `Pokemon` viven en módulos separados que luego hay que importar entre sí.
- [[MOC_Programacion]] — punto de entrada del área.
- Ruta futura: `pokemon/move.py` (clase `Move`), `pokemon/pokemon.py` (clase `Pokemon`).
- Tests spec: `tests/test_move.py`, `tests/test_pokemon.py` (define el contrato exacto que debes cumplir).

## Resumen mental

> Una **clase** es un molde (`class Pokemon`, escrito una vez); un **objeto** es algo fabricado con ese molde (`pikachu`, con 35 de 35 PS, independiente de `charmander`). Los **atributos** son los datos del objeto (`pikachu.hp`), se leen y escriben con punto. `__init__` es el constructor: se dispara solo al instanciar y rellena los atributos vía `self.atributo = valor`. **`self`** es el propio objeto sobre el que llamaste el método: `pikachu.take_damage(10)` equivale a `Pokemon.take_damage(pikachu, 10)`, Python pone `self=pikachu` solo. Un **método** es una función dentro de la clase con `self` de primer parámetro; opera sobre el objeto. El **estado mutable** es que `hp` baja con `take_damage` mientras `max_hp` queda fijo, y cada objeto muta el suyo. `__str__` devuelve el texto con que se imprime el objeto. Errores típicos: olvidar `self`, confundir clase con instancia, mutar el atributo equivocado.
