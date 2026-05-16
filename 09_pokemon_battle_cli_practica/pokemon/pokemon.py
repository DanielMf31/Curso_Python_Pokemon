"""La clase Pokemon.   --- TU TURNO (categoria B) ---

Implementa __init__, take_damage(), is_fainted(), reset() y __str__.
Lee primero: docs/06-clases-y-objetos.md

Verifica:  python -m pytest tests/test_pokemon.py -q
"""


class Pokemon:
    """Un Pokemon (name, type, max_hp, attack, defense, level, moves)."""

    def __init__(self, name, type, max_hp, attack, defense, level, moves):
        # TODO (doc 06): guarda los parametros como atributos.
        # OJO: self.hp empieza igual a max_hp (PS a tope).
        raise NotImplementedError("TODO (doc 06): implementa Pokemon.__init__")

    def take_damage(self, amount):
        """Resta `amount` PS sin bajar nunca de 0 (pista: max(0, ...))."""
        raise NotImplementedError("TODO (doc 06): implementa take_damage")

    def is_fainted(self):
        """True si esta debilitado (hp <= 0)."""
        raise NotImplementedError("TODO (doc 06): implementa is_fainted")

    def reset(self):
        """Restaura hp a max_hp y el pp de cada movimiento a su max_pp."""
        raise NotImplementedError("TODO (doc 06): implementa reset")

    def __str__(self):
        # Algo como: "Pikachu [electric]  PS 35/35"
        raise NotImplementedError("TODO (doc 06): implementa Pokemon.__str__")
