"""Los Pokemon y sus movimientos: los DATOS del juego.

Categoria A (parte completa) + practica de instanciacion:
  - La logica (_moves_for, list_pokemon, get_pokemon) YA esta hecha.
  - _MOVES_BY_TYPE YA esta hecho.
  - _POKEDEX trae 2 Pokemon COMPLETOS de ejemplo (Charmander, Bulbasaur).
  - TU TURNO: anade los 8 Pokemon que faltan al diccionario _POKEDEX
    copiando el patron. Lee docs/02-variables-y-tipos.md y
    docs/03-estructuras-de-datos.md. (Con solo los 2 de ejemplo el juego
    ya funciona; los 8 restantes amplian el roster y tu practica.)
"""

from pokemon.move import Move
from pokemon.pokemon import Pokemon

# YA HECHO. Movimientos extra por tipo (todos llevan ademas "Tackle").
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
    # --- 2 EJEMPLOS COMPLETOS (no los toques, son tu plantilla) ---
    "Charmander": ("fire", 39, 52, 43, 5),
    "Bulbasaur":  ("grass", 45, 49, 49, 5),

    # --- TU TURNO: anade estos 8 copiando el patron de arriba ---
    # "Squirtle":   ("water", 44, 48, 65, 5),
    # "Pikachu":    ("electric", 35, 55, 40, 5),
    # "Geodude":    ("rock", 40, 80, 100, 5),
    # "Rattata":    ("normal", 30, 56, 35, 5),
    # "Charizard":  ("fire", 78, 84, 78, 10),
    # "Blastoise":  ("water", 79, 83, 100, 10),
    # "Venusaur":   ("grass", 80, 82, 83, 10),
    # "Raichu":     ("electric", 60, 90, 55, 10),
}


def _moves_for(type):
    """YA HECHO. Construye la lista de Move segun el tipo."""
    moves = [Move("Tackle", "normal", 40, 100, 35)]
    for name, mtype, power, acc, pp in _MOVES_BY_TYPE.get(type, []):
        moves.append(Move(name, mtype, power, acc, pp))
    return moves


def list_pokemon():
    """YA HECHO. Devuelve la lista de nombres disponibles."""
    return list(_POKEDEX.keys())


def get_pokemon(name):
    """YA HECHO. Crea una instancia NUEVA de Pokemon por su nombre."""
    type, max_hp, attack, defense, level = _POKEDEX[name]
    return Pokemon(name, type, max_hp, attack, defense, level, _moves_for(type))
