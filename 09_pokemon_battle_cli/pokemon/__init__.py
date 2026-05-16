"""Paquete `pokemon`: la logica del juego de batalla por terminal.

Reexporta las piezas principales para poder escribir, por ejemplo:

    from pokemon import Pokemon, Move, Battle
"""

from pokemon.move import Move
from pokemon.pokemon import Pokemon
from pokemon.types import TYPES, TYPE_CHART, effectiveness
from pokemon.battle import Battle, calculate_damage, ai_choose_move

__all__ = [
    "Move",
    "Pokemon",
    "TYPES",
    "TYPE_CHART",
    "effectiveness",
    "Battle",
    "calculate_damage",
    "ai_choose_move",
]
