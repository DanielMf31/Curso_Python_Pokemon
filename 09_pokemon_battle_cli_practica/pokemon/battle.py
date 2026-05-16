"""Calculo de dano y bucle de batalla.   --- TU TURNO (categoria B) ---

Implementa calculate_damage(), ai_choose_move() y los metodos
Battle._turn() y Battle.run(). El __init__ de Battle ya esta hecho.

Lee primero:
  - docs/09-la-formula-de-dano.md   (calculate_damage)
  - docs/10-el-bucle-de-batalla.md  (ai_choose_move + Battle)

Verifica:  python -m pytest tests/test_battle.py -q
"""

import random

from pokemon.types import effectiveness


def calculate_damage(attacker, defender, move):
    """Devuelve (damage, hit, multiplier).

    Pasos (doc 09):
      1. Si random.randint(1, 100) > move.accuracy -> falla: (0, False, 1.0)
      2. base = (((2*attacker.level/5 + 2) * move.power
                  * (attacker.attack/defender.defense)) / 50) + 2
      3. multiplier = effectiveness(move.type, defender.type)
      4. variance = random.uniform(0.85, 1.0)
      5. damage = max(1, int(base * multiplier * variance))
      6. return damage, True, multiplier
    """
    raise NotImplementedError("TODO (doc 09): implementa calculate_damage")


def ai_choose_move(pokemon, opponent):
    """Devuelve un movimiento al azar de los que tienen PP, o None si ninguno.

    Pista (doc 10): filtra los moves con has_pp() y usa random.choice().
    """
    raise NotImplementedError("TODO (doc 10): implementa ai_choose_move")


class Battle:
    """Batalla por turnos entre dos Pokemon. El __init__ ya esta dado."""

    def __init__(self, p1, p2,
                 choose_p1=ai_choose_move, choose_p2=ai_choose_move,
                 report=lambda text: None):
        self.p1 = p1
        self.p2 = p2
        self.choose_p1 = choose_p1
        self.choose_p2 = choose_p2
        self.report = report

    def _turn(self, attacker, defender, choose):
        """Un turno: elegir movimiento, gastar PP, calcular dano, aplicarlo.

        Pista (doc 10): si attacker o defender ya estan debilitados, no hagas
        nada. Si choose() devuelve None -> forcejeo (1 de dano). Usa
        self.report(texto) para narrar.
        """
        raise NotImplementedError("TODO (doc 10): implementa Battle._turn")

    def run(self):
        """Bucle while hasta que uno se debilite. Devuelve el ganador.

        Pista (doc 10): mientras ninguno este debilitado, turno de p1 y
        luego de p2. Al salir, el ganador es el que NO esta debilitado.
        """
        raise NotImplementedError("TODO (doc 10): implementa Battle.run")
