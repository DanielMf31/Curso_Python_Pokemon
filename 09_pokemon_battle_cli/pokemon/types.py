"""Tipos Pokemon y tabla de efectividad.

Un "tipo" es una categoria: normal, fire, water, grass, electric, rock.
La TYPE_CHART dice cuanto multiplica el dano un tipo atacante contra un
tipo defensor: 2.0 (supereficaz), 0.5 (poco eficaz) o 1.0 (neutro).
"""

# Los 6 tipos del juego. Se usan siempre en minusculas.
TYPES = ["normal", "fire", "water", "grass", "electric", "rock"]

# Solo se listan las relaciones distintas de 1.0.
# Cualquier combinacion que no aparezca aqui vale 1.0 (neutro).
# Estructura: TYPE_CHART[tipo_atacante][tipo_defensor] = multiplicador
TYPE_CHART = {
    "fire":     {"grass": 2.0, "water": 0.5, "rock": 0.5, "fire": 0.5},
    "water":    {"fire": 2.0, "rock": 2.0, "water": 0.5, "grass": 0.5},
    "grass":    {"water": 2.0, "rock": 2.0, "fire": 0.5, "grass": 0.5},
    "electric": {"water": 2.0, "grass": 0.5, "electric": 0.5},
    "rock":     {"fire": 2.0, "electric": 2.0, "water": 0.5, "grass": 0.5},
    "normal":   {},
}


def effectiveness(attack_type, defender_type):
    """Multiplicador del tipo atacante contra el tipo defensor.

    Devuelve 2.0, 0.5 o 1.0. Si la combinacion no esta en TYPE_CHART,
    el resultado es 1.0 (neutro) gracias al doble `.get(..., {})` / 1.0.
    """
    return TYPE_CHART.get(attack_type, {}).get(defender_type, 1.0)
