"""La clase Move: un movimiento que un Pokemon puede usar en combate."""


class Move:
    """Un movimiento.

    Atributos:
        name:     nombre legible ("Ember").
        type:     tipo del movimiento ("fire").
        power:    potencia base (entero).
        accuracy: precision 0-100 (probabilidad de acertar).
        pp:       usos restantes.
        max_pp:   usos maximos (si no se pasa, es igual a `pp`).
    """

    def __init__(self, name, type, power, accuracy, pp, max_pp=None):
        self.name = name
        self.type = type
        self.power = power
        self.accuracy = accuracy
        self.pp = pp
        self.max_pp = max_pp if max_pp is not None else pp

    def has_pp(self):
        """True si todavia quedan usos de este movimiento."""
        return self.pp > 0

    def use(self):
        """Consume 1 PP.

        Devuelve True si se pudo usar, False si ya no quedaban PP.
        """
        if self.pp > 0:
            self.pp -= 1
            return True
        return False

    def __str__(self):
        return (f"{self.name} [{self.type}] pot {self.power} "
                f"PP {self.pp}/{self.max_pp}")
