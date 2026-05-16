---
title: 00 — Empieza aqui
date: 2026-05-16
tags: [programacion/python, build-things, pokemon-cli, teaching]
type: doc
status: vivo
source: claude-code
---

# Empieza aqui

Bienvenido. Vas a construir un juego de **batalla Pokemon que se juega
escribiendo en la terminal** (sin graficos, solo texto). Lo importante no
es el juego: es que **vas a aprender a programar en Python desde cero
absoluto** mientras lo construyes. No hace falta que sepas nada de
programacion. Nada. Cero. Empezamos por encender la terminal.

## Por que importa

Mucha gente intenta aprender a programar viendo videos y nunca escribe
una linea de codigo. Aqui el plan es el contrario: **tu tecleas el
codigo con tus dedos**, pieza a pieza, y cada pieza se comprueba sola con
una prueba automatica. Cuando la prueba se pone "verde", sabes que esa
parte funciona de verdad. No hay que confiar en tu memoria ni en la
suerte: el ordenador te dice si lo has hecho bien.

## Schema / Modelo mental

Hay **dos carpetas gemelas**. Esto es la idea mas importante de todo el
proyecto, asi que leelo dos veces:

```
   09_pokemon_battle_cli/            <-- EL MODELO
   (el juego YA terminado y funcionando)
        |
        |  lo MIRAS cuando estas atascado
        v
   09_pokemon_battle_cli_practica/   <-- LA PRACTICA
   (el mismo juego, pero con HUECOS que TU rellenas)
        |
        |  aqui es donde TECLEAS
        v
        TU CODIGO  --->  un test lo comprueba  --->  VERDE = dominado
```

- **Modelo** = la respuesta. Esta completo. Funciona. Solo lo abres si
  te quedas bloqueado y necesitas ver "como se hace".
- **Practica** = tu cuaderno. Tiene la estructura montada pero faltan
  trozos marcados con `TODO`. Tu trabajo es rellenarlos.

### Split-view (pantalla partida)

La forma recomendada de trabajar:

```
  +---------------------------+---------------------------+
  |  IZQUIERDA: la PRACTICA   |  DERECHA: el MODELO        |
  |  (aqui ESCRIBES tu)       |  (aqui solo MIRAS)         |
  +---------------------------+---------------------------+
```

Regla de oro: **lee la practica, intenta hacerlo tu, y solo si te
atascas miras el modelo. Nunca copies a ciegas: entiende y luego
teclea en la practica.**

## Pasos

1. Empieza por la siguiente doc: `docs/01-instalar-python-y-terminal.md`.
   Te explica desde cero que es una terminal y como dejar el ordenador
   listo. No te saltes esto aunque te de pereza.
2. Sigue las docs **en orden numerico**: `00 -> 01 -> 02 -> ... -> 12`.
   Cada una introduce un concepto nuevo y te dice exactamente que
   fichero rellenar.
3. Despues de cada doc, corre los tests (mas abajo). Si estan en verde,
   has dominado ese nivel. Pasa al siguiente.
4. Cuando termines todas las docs, el juego completo funcionara.

## Como correr los tests

Un "test" es un programa pequeno que comprueba si tu codigo hace lo que
debe. Tu no escribes los tests: ya estan hechos. Tu solo los ejecutas
para ver si vas bien.

Forma normal (necesita la herramienta `pytest`, que `setup.sh` instala):

```bash
python -m pytest -q
```

Forma alternativa (si `pytest` no esta disponible por lo que sea):

```bash
python tests/run_tests.py
```

Las dos hacen lo mismo: ejecutan todas las comprobaciones y te dicen
cuantas pasan y cuantas fallan.

## Comandos / sintaxis (al final)

| Quiero...                         | Escribo...                  |
|-----------------------------------|-----------------------------|
| Preparar el ordenador (una vez)   | `bash scripts/setup.sh`     |
| Jugar al juego                    | `python main.py`            |
| Ver mi progreso (tests)           | `python -m pytest -q`       |
| Ver progreso sin pytest           | `python tests/run_tests.py` |

## Gotchas / Anti-patterns

| Anti-patron                              | Que hacer en su lugar                          |
|------------------------------------------|------------------------------------------------|
| Copiar el modelo entero sin leer         | Lee, entiende, y teclea TU en la practica      |
| Saltarse la doc 01 "porque ya se"        | Hazla igual: monta el entorno bien una vez     |
| Seguir a la doc 5 con tests en rojo      | No avances con tests rojos: arregla primero    |
| Tocar ficheros en la carpeta del modelo  | El modelo no se toca; tu trabajas en practica  |
| Frustrarte si algo falla a la primera    | Es normal. Lee el error. Vuelve a intentarlo.  |

## Tu turno

1. Abre la siguiente doc:
   `docs/01-instalar-python-y-terminal.md`.
2. No escribas codigo todavia. Primero deja el ordenador listo.

## Conexiones

- Siguiente: [[01-instalar-python-y-terminal]]
- Mapa de niveles: [[PHASES]]
- Codigo del modelo (cuando llegues ahi): `09_pokemon_battle_cli/pokemon/`
- Donde tecleas: `09_pokemon_battle_cli_practica/pokemon/`

## Resumen mental

> Vas a programar tu primer juego en Python sin saber nada de antemano.
> Hay dos carpetas: el **modelo** (juego terminado, solo para mirar) y la
> **practica** (mismo juego con huecos `TODO` que tu rellenas). Trabajas
> con pantalla partida: practica a la izquierda donde escribes, modelo a
> la derecha donde miras solo si te atascas. Nunca copies a ciegas:
> entiende y luego teclea tu. Sigues las docs en orden 00, 01, 02, hasta
> 12. Cada una ensena un concepto y te dice que fichero rellenar.
> Despues de cada doc corres los tests con `python -m pytest -q` (o el
> plan B `python tests/run_tests.py`). Cuando un test esta verde, ese
> trozo funciona de verdad y lo has dominado. No avances con tests en
> rojo. Empieza ya por la doc 01: deja el ordenador listo antes de
> escribir tu primera linea de codigo.
