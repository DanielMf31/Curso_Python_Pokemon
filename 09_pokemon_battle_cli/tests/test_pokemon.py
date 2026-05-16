"""Tests de la clase Pokemon (pokemon/pokemon.py)."""

from pokemon.move import Move
from pokemon.pokemon import Pokemon


def _pikachu():
    return Pokemon(
        "Pikachu", "electric", 35, 55, 40, 5,
        [Move("Thunder Shock", "electric", 40, 100, 30)],
    )


def test_starts_at_full_hp():
    p = _pikachu()
    assert p.hp == 35
    assert p.max_hp == 35
    assert p.is_fainted() is False


def test_take_damage_reduces_hp():
    p = _pikachu()
    p.take_damage(10)
    assert p.hp == 25
    assert p.is_fainted() is False


def test_take_damage_clamps_at_zero():
    p = _pikachu()
    p.take_damage(999)
    assert p.hp == 0
    assert p.is_fainted() is True


def test_reset_restores_hp_and_pp():
    p = _pikachu()
    p.take_damage(35)
    p.moves[0].use()
    p.reset()
    assert p.hp == 35
    assert p.moves[0].pp == 30
    assert p.is_fainted() is False
