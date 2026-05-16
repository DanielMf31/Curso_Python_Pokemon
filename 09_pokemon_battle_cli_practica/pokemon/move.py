"""La clase Move.   --- TU TURNO (categoria B) ---

Implementa __init__, has_pp(), use() y __str__.
Lee primero: docs/06-clases-y-objetos.md

Verifica:  python -m pytest tests/test_move.py -q
"""


class Move:
    """Un movimiento (name, type, power, accuracy, pp, max_pp)."""

    def __init__(self, name, type, power, accuracy, pp, max_pp=None):
        # TODO (doc 06): guarda cada parametro como atributo (self.name = name, ...).
        # max_pp por defecto = pp (si max_pp es None, usa pp).
        raise NotImplementedError("TODO (doc 06): implementa Move.__init__")

    def has_pp(self):
        """True si todavia quedan usos (pp > 0)."""
        raise NotImplementedError("TODO (doc 06): implementa Move.has_pp")

    def use(self):
        """Consume 1 PP. Devuelve True si se pudo usar, False si no quedaban."""
        raise NotImplementedError("TODO (doc 06): implementa Move.use")

    def __str__(self):
        # Algo como: "Ember [fire] pot 40 PP 25/25"
        raise NotImplementedError("TODO (doc 06): implementa Move.__str__")
