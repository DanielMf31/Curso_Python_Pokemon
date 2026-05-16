"""Tests de la tabla de tipos (pokemon/types.py)."""

from pokemon.types import TYPES, TYPE_CHART, effectiveness


def test_types_list_has_six():
    assert len(TYPES) == 6
    for t in ["normal", "fire", "water", "grass", "electric", "rock"]:
        assert t in TYPES


def test_super_effective():
    assert effectiveness("fire", "grass") == 2.0
    assert effectiveness("water", "fire") == 2.0
    assert effectiveness("grass", "water") == 2.0
    assert effectiveness("electric", "water") == 2.0
    assert effectiveness("rock", "fire") == 2.0
    assert effectiveness("rock", "electric") == 2.0


def test_not_very_effective():
    assert effectiveness("fire", "water") == 0.5
    assert effectiveness("fire", "fire") == 0.5
    assert effectiveness("water", "grass") == 0.5
    assert effectiveness("grass", "fire") == 0.5
    assert effectiveness("electric", "electric") == 0.5


def test_neutral_is_default():
    # Combinaciones no listadas -> 1.0
    assert effectiveness("normal", "rock") == 1.0
    assert effectiveness("normal", "fire") == 1.0
    assert effectiveness("electric", "rock") == 1.0
    assert effectiveness("fire", "electric") == 1.0


def test_chart_only_contains_known_types():
    for attacker, row in TYPE_CHART.items():
        assert attacker in TYPES
        for defender in row:
            assert defender in TYPES
