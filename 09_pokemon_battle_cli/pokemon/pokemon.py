"""La clase Pokemon: un combatiente con PS, ataque, defensa y movimientos."""


class Pokemon:
    """Un Pokemon concreto listo para combatir.

    Atributos:
        name:    nombre ("Pikachu").
        type:    su tipo ("electric").
        max_hp:  PS maximos.
        hp:      PS actuales (empiezan a tope).
        attack:  estadistica de ataque.
        defense: estadistica de defensa.
        level:   nivel (afecta a la formula de dano).
        moves:   lista de objetos Move.
    """

    def __init__(self, name, type, max_hp, attack, defense, level, moves):
        self.name = name
        self.type = type
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack
        self.defense = defense
        self.level = level
        self.moves = moves

    def take_damage(self, amount):
        """Resta `amount` PS sin bajar nunca de 0."""
        self.hp = max(0, self.hp - amount)

    def is_fainted(self):
        """True si el Pokemon esta debilitado (0 PS)."""
        return self.hp <= 0

    def reset(self):
        """Restaura PS y PP de todos los movimientos (para volver a jugar)."""
        self.hp = self.max_hp
        for move in self.moves:
            move.pp = move.max_pp

    def __str__(self):
        return f"{self.name} [{self.type}]  PS {self.hp}/{self.max_hp}"
