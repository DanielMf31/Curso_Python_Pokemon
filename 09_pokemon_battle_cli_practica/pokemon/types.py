"""Tipos Pokemon y tabla de efectividad.   --- TU TURNO (categoria B) ---

Tienes que implementar TYPE_CHART y effectiveness().
Lee primero: docs/08-la-tabla-de-tipos.md  (y docs/05-funciones.md)

Cuando lo tengas:  python -m pytest tests/test_types.py -q
(o sin pytest:     python tests/run_tests.py)
"""

# Esto ya esta dado: los 6 tipos del juego (siempre en minusculas).
TYPES = ["normal", "fire", "water", "grass", "electric", "rock"]

# TODO (doc 08): rellena la tabla. Estructura:
#   TYPE_CHART[tipo_atacante][tipo_defensor] = multiplicador
# Solo se listan las relaciones distintas de 1.0; lo que no aparezca = 1.0.
# Ejemplo de una fila:  "fire": {"grass": 2.0, "water": 0.5, ...}
TYPE_CHART = {
    # "fire":     {...},
    # "water":    {...},
    # "grass":    {...},
    # "electric": {...},
    # "rock":     {...},
    # "normal":   {},
}


def effectiveness(attack_type, defender_type):
    """Multiplicador del tipo atacante contra el defensor (2.0 / 0.5 / 1.0).

    Pista: una sola linea. Usa TYPE_CHART con doble `.get(..., {})`
    terminando en `.get(defender_type, 1.0)` para que lo no listado sea 1.0.
    """
    raise NotImplementedError(
        "TODO (doc 08): implementa effectiveness() usando TYPE_CHART"
    )
