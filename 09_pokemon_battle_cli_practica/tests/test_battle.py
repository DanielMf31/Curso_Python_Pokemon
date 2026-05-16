"""Tests del calculo de dano y del bucle de batalla (pokemon/battle.py).

Para que el dano sea DETERMINISTA reemplazamos temporalmente el modulo
`random` que usa battle.py por un objeto falso (monkeypatch). Asi no
dependemos del azar y podemos comprobar valores exactos.
"""

import random as _real_random

import pokemon.battle as battle
from pokemon.battle import Battle, calculate_damage
from pokemon.data import get_pokemon
from pokemon.move import Move
from pokemon.pokemon import Pokemon


class _NoRandom:
    """Nunca falla (randint=1) y varianza maxima (uniform=1.0)."""

    def randint(self, a, b):
        return 1

    def uniform(self, a, b):
        return 1.0

    def choice(self, seq):
        # Eleccion determinista: siempre el primer movimiento disponible.
        return seq[0]


class _AlwaysMiss:
    """Siempre falla: randint=100 > cualquier accuracy < 100."""

    def randint(self, a, b):
        return 100

    def uniform(self, a, b):
        return 1.0

    def choice(self, seq):
        return seq[0]


def _use(fake):
    battle.random = fake


def _restore():
    battle.random = _real_random


def test_damage_exact_when_neutral():
    _use(_NoRandom())
    try:
        atk = Pokemon("A", "normal", 50, 50, 50, 5, [])
        dfn = Pokemon("B", "normal", 50, 50, 50, 5, [])
        move = Move("Tackle", "normal", 50, 100, 35)
        dmg, hit, mult = calculate_damage(atk, dfn, move)
        # base = ((2*5/5+2) * 50 * (50/50)) / 50 + 2 = (4*50/50)+2 = 6
        # 6 * 1.0 (neutro) * 1.0 (varianza) -> 6
        assert hit is True
        assert mult == 1.0
        assert dmg == 6
    finally:
        _restore()


def test_super_effective_beats_resisted():
    _use(_NoRandom())
    try:
        fire = Pokemon("F", "fire", 50, 50, 50, 5, [])
        grass = Pokemon("G", "grass", 50, 50, 50, 5, [])
        water = Pokemon("W", "water", 50, 50, 50, 5, [])
        ember = Move("Ember", "fire", 40, 100, 25)

        dmg_grass, _, m1 = calculate_damage(fire, grass, ember)
        dmg_water, _, m2 = calculate_damage(fire, water, ember)

        assert m1 == 2.0 and m2 == 0.5
        assert dmg_grass > dmg_water
        assert dmg_grass >= 1 and dmg_water >= 1
    finally:
        _restore()


def test_miss_returns_zero_no_hit():
    _use(_AlwaysMiss())
    try:
        a = Pokemon("A", "fire", 50, 50, 50, 5, [])
        b = Pokemon("B", "grass", 50, 50, 50, 5, [])
        move = Move("Ember", "fire", 40, 80, 25)
        dmg, hit, mult = calculate_damage(a, b, move)
        assert hit is False
        assert dmg == 0
        assert mult == 1.0
    finally:
        _restore()


def test_damage_is_at_least_one():
    _use(_NoRandom())
    try:
        weak = Pokemon("Weak", "fire", 50, 1, 1, 1, [])
        tank = Pokemon("Tank", "water", 50, 1, 999, 1, [])
        move = Move("Ember", "fire", 1, 100, 25)
        dmg, hit, _ = calculate_damage(weak, tank, move)
        assert hit is True
        assert dmg >= 1
    finally:
        _restore()


def test_battle_always_has_a_winner():
    _use(_NoRandom())
    try:
        p1 = get_pokemon("Charmander")
        p2 = get_pokemon("Bulbasaur")
        winner = Battle(p1, p2).run()
        assert winner in (p1, p2)
        assert p1.is_fainted() or p2.is_fainted()
    finally:
        _restore()
