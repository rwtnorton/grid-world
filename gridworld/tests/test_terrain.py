from gridworld.terrain import Terrain
import pytest


def test_terrain_enum():
    assert Terrain.BLANK.value == 0
    assert Terrain.SPEEDER.value == 1
    assert Terrain.LAVA.value == 2
    assert Terrain.MUD.value == 3


def test_terrain_str():
    assert str(Terrain.BLANK) == "."
    assert str(Terrain.SPEEDER) == "+"
    assert str(Terrain.LAVA) == "*"
    assert str(Terrain.MUD) == "#"


def test_terrain_from_str():
    assert Terrain.from_str(".") == Terrain.BLANK
    assert Terrain.from_str("+") == Terrain.SPEEDER
    assert Terrain.from_str("*") == Terrain.LAVA
    assert Terrain.from_str("#") == Terrain.MUD
    with pytest.raises(ValueError) as err:
        Terrain.from_str(":-)")
    assert "unknown terrain" in str(err.value)
