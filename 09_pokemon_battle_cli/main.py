"""Punto de entrada del juego.

Uso:
    python main.py          jugar tu contra la IA
    python main.py --demo   batalla automatica IA vs IA (sin teclado)
"""

import sys

from pokemon.battle import Battle, ai_choose_move
from pokemon.data import get_pokemon, list_pokemon
from pokemon import ui


def run_demo():
    """Batalla automatica, util para probar el juego sin interaccion."""
    p1 = get_pokemon("Charmander")
    p2 = get_pokemon("Bulbasaur")
    Battle(p1, p2, ai_choose_move, ai_choose_move, report=print).run()


def run_interactive():
    """Partida normal: tu eliges Pokemon y movimientos contra la IA."""
    names = list_pokemon()
    ui.announce("=== Pokemon Battle CLI ===")
    mine = ui.choose_pokemon(names)
    rival = "Squirtle" if mine != "Squirtle" else "Bulbasaur"
    p1 = get_pokemon(mine)
    p2 = get_pokemon(rival)
    ui.announce(f"\nTu:    {p1}\nRival: {p2}\n")
    Battle(p1, p2, ui.make_human_chooser(), ai_choose_move, report=print).run()


def main():
    if "--demo" in sys.argv:
        run_demo()
    else:
        run_interactive()


if __name__ == "__main__":
    main()
