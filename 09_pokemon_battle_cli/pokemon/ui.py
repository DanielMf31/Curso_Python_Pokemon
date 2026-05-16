"""Entrada/salida por terminal, SEPARADA de la logica de batalla.

Asi `battle.py` no sabe nada de print() ni input(): se puede testear
sin teclado. Esto es un patron importante (separar logica de interfaz).
"""


def announce(text):
    """Muestra una linea por pantalla."""
    print(text)


def show_status(p1, p2):
    """Muestra los PS de ambos Pokemon en una linea."""
    print(f"  {p1.name:<10} PS {p1.hp:>3}/{p1.max_hp:<3}   |   "
          f"{p2.name:<10} PS {p2.hp:>3}/{p2.max_hp:<3}")


def choose_pokemon(names):
    """Pide al usuario que elija un Pokemon de la lista `names`."""
    print("Pokemon disponibles:")
    for i, name in enumerate(names, 1):
        print(f"  {i}. {name}")
    while True:
        raw = input("Elige tu Pokemon (numero): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(names):
            return names[int(raw) - 1]
        print("Entrada no valida, intenta de nuevo.")


def make_human_chooser():
    """Devuelve una funcion (pokemon, opponent) -> Move que pregunta al usuario.

    Encaja como `choose_p1` de Battle.
    """
    def chooser(pokemon, opponent):
        usable = [m for m in pokemon.moves if m.has_pp()]
        if not usable:
            return None
        print(f"\nTurno de {pokemon.name}. Movimientos:")
        for i, m in enumerate(pokemon.moves, 1):
            estado = "" if m.has_pp() else "  (sin PP)"
            print(f"  {i}. {m.name} [{m.type}] pot {m.power} "
                  f"PP {m.pp}/{m.max_pp}{estado}")
        while True:
            raw = input("Elige movimiento (numero): ").strip()
            if raw.isdigit() and 1 <= int(raw) <= len(pokemon.moves):
                move = pokemon.moves[int(raw) - 1]
                if move.has_pp():
                    return move
                print("Ese movimiento no tiene PP.")
            else:
                print("Entrada no valida.")

    return chooser
