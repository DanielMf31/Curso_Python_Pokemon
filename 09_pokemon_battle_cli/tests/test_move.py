"""Tests de la clase Move (pokemon/move.py)."""

from pokemon.move import Move


def test_max_pp_defaults_to_pp():
    m = Move("Tackle", "normal", 40, 100, 35)
    assert m.max_pp == 35


def test_max_pp_can_be_explicit():
    m = Move("Ember", "fire", 40, 100, 10, max_pp=25)
    assert m.pp == 10
    assert m.max_pp == 25


def test_has_pp_and_use_decrements():
    m = Move("Ember", "fire", 40, 100, 2)
    assert m.has_pp() is True

    assert m.use() is True
    assert m.pp == 1

    assert m.use() is True
    assert m.pp == 0
    assert m.has_pp() is False

    # Sin PP no se puede usar y no baja por debajo de 0.
    assert m.use() is False
    assert m.pp == 0
