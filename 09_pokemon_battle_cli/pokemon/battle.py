"""Calculo de dano y bucle de batalla por turnos."""

import random

from pokemon.types import effectiveness


def calculate_damage(attacker, defender, move):
    """Calcula el dano de `move` de `attacker` sobre `defender`.

    Devuelve una tupla (damage, hit, multiplier):
      - Si el movimiento falla (segun accuracy): (0, False, 1.0).
      - Si acierta: dano entero >= 1 con la formula estilo Pokemon
        simplificada, el multiplicador de tipo y una varianza aleatoria.
    """
    if random.randint(1, 100) > move.accuracy:
        return 0, False, 1.0

    base = (((2 * attacker.level / 5 + 2) * move.power
             * (attacker.attack / defender.defense)) / 50) + 2
    multiplier = effectiveness(move.type, defender.type)
    variance = random.uniform(0.85, 1.0)
    damage = max(1, int(base * multiplier * variance))
    return damage, True, multiplier


def ai_choose_move(pokemon, opponent):
    """Eleccion del rival: un movimiento al azar de entre los que tienen PP.

    Devuelve None si no le queda ningun movimiento con PP.
    """
    usable = [m for m in pokemon.moves if m.has_pp()]
    if not usable:
        return None
    return random.choice(usable)


class Battle:
    """Una batalla por turnos entre dos Pokemon.

    choose_p1 / choose_p2 son funciones (pokemon, opponent) -> Move
    (por defecto, la IA simple). `report` recibe texto para mostrarlo
    (por defecto no muestra nada; main.py pasa `print`).
    """

    def __init__(self, p1, p2,
                 choose_p1=ai_choose_move, choose_p2=ai_choose_move,
                 report=lambda text: None):
        self.p1 = p1
        self.p2 = p2
        self.choose_p1 = choose_p1
        self.choose_p2 = choose_p2
        self.report = report

    def _turn(self, attacker, defender, choose):
        if attacker.is_fainted() or defender.is_fainted():
            return
        move = choose(attacker, defender)
        if move is None:
            self.report(f"{attacker.name} no tiene PP. Forcejea (1 de dano).")
            defender.take_damage(1)
            return
        move.use()
        damage, hit, mult = calculate_damage(attacker, defender, move)
        if not hit:
            self.report(f"{attacker.name} usa {move.name}... pero falla.")
            return
        defender.take_damage(damage)
        nota = ""
        if mult > 1.0:
            nota = " Es supereficaz!"
        elif 0 < mult < 1.0:
            nota = " No es muy eficaz..."
        self.report(
            f"{attacker.name} usa {move.name}: {damage} de dano.{nota} "
            f"({defender.name} {defender.hp}/{defender.max_hp} PS)"
        )

    def run(self):
        """Corre la batalla hasta que uno se debilite. Devuelve el ganador."""
        self.report(f"Combate: {self.p1.name} vs {self.p2.name}")
        while not self.p1.is_fainted() and not self.p2.is_fainted():
            self._turn(self.p1, self.p2, self.choose_p1)
            self._turn(self.p2, self.p1, self.choose_p2)
        winner = self.p2 if self.p1.is_fainted() else self.p1
        self.report(f"Gana {winner.name}!")
        return winner
