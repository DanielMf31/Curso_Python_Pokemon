"""Los 10 Pokemon y sus movimientos: los DATOS del juego.

Aqui no hay logica, solo datos escritos a mano. `get_pokemon(name)`
construye una instancia NUEVA cada vez (con PS y PP frescos) para que
dos partidas no compartan estado.
"""

from pokemon.move import Move
from pokemon.pokemon import Pokemon

# Movimientos extra por tipo. Todos los Pokemon llevan ademas "Tackle".
_MOVES_BY_TYPE = {
    "fire": [
        ("Ember", "fire", 40, 100, 25),
        ("Flamethrower", "fire", 90, 100, 15),
    ],
    "water": [
        ("Water Gun", "water", 40, 100, 25),
        ("Hydro Pump", "water", 110, 80, 5),
    ],
    "grass": [
        ("Vine Whip", "grass", 45, 100, 25),
        ("Razor Leaf", "grass", 55, 95, 25),
    ],
    "electric": [
        ("Thunder Shock", "electric", 40, 100, 30),
        ("Thunderbolt", "electric", 90, 100, 15),
    ],
    "rock": [
        ("Rock Throw", "rock", 50, 90, 15),
        ("Rock Slide", "rock", 75, 90, 10),
    ],
    "normal": [
        ("Scratch", "normal", 40, 100, 35),
    ],
}

# (type, max_hp, attack, defense, level)
_POKEDEX = {
    "Charmander": ("fire", 39, 52, 43, 5),
    "Squirtle":   ("water", 44, 48, 65, 5),
    "Bulbasaur":  ("grass", 45, 49, 49, 5),
    "Pikachu":    ("electric", 35, 55, 40, 5),
    "Geodude":    ("rock", 40, 80, 100, 5),
    "Rattata":    ("normal", 30, 56, 35, 5),
    "Charizard":  ("fire", 78, 84, 78, 10),
    "Blastoise":  ("water", 79, 83, 100, 10),
    "Venusaur":   ("grass", 80, 82, 83, 10),
    "Raichu":     ("electric", 60, 90, 55, 10),
}


def _moves_for(type):
    """Construye la lista de Move de un Pokemon segun su tipo."""
    moves = [Move("Tackle", "normal", 40, 100, 35)]
    for name, mtype, power, acc, pp in _MOVES_BY_TYPE.get(type, []):
        moves.append(Move(name, mtype, power, acc, pp))
    return moves


def list_pokemon():
    """Devuelve la lista de nombres disponibles."""
    return list(_POKEDEX.keys())


def get_pokemon(name):
    """Crea una instancia NUEVA de Pokemon por su nombre.

    Lanza KeyError si el nombre no existe.
    """
    type, max_hp, attack, defense, level = _POKEDEX[name]
    return Pokemon(name, type, max_hp, attack, defense, level, _moves_for(type))
