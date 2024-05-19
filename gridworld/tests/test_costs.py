import pytest

from gridworld.costs import Costs, std_move_costs, std_health_costs
from gridworld.terrain import Terrain


def test_costs_init():
    hmap = {
        Terrain.BLANK: -1,
        Terrain.SPEEDER: -2,
        Terrain.LAVA: -3,
        Terrain.MUD: -4,
    }
    mmap = {
        Terrain.BLANK: -10,
        Terrain.SPEEDER: -20,
        Terrain.LAVA: -30,
        Terrain.MUD: -40,
    }
    costs = Costs(health_costs=hmap, move_costs=mmap)
    assert costs.health_costs == hmap
    assert costs.move_costs == mmap


def test_costs_init_defaults():
    costs = Costs()
    assert costs.health_costs == std_health_costs()
    assert costs.move_costs == std_move_costs()


def test_costs_init_bad_health_args():
    hmap = {
        Terrain.BLANK: -1,
        Terrain.SPEEDER: -2,
    }
    mmap = {
        Terrain.BLANK: -10,
        Terrain.SPEEDER: -20,
        Terrain.LAVA: -30,
        Terrain.MUD: -40,
    }
    with pytest.raises(ValueError) as bad_h_err:
        Costs(health_costs=hmap, move_costs=mmap)
    assert "missing health terrains: lava, mud" in str(bad_h_err.value)


def test_costs_init_bad_move_args():
    hmap = {
        Terrain.BLANK: -1,
        Terrain.SPEEDER: -2,
        Terrain.LAVA: -3,
        Terrain.MUD: -4,
    }
    mmap = {
        Terrain.LAVA: -30,
        Terrain.MUD: -40,
    }
    with pytest.raises(ValueError) as bad_m_err:
        Costs(health_costs=hmap, move_costs=mmap)
    assert "missing move terrains: blank, speeder" in str(bad_m_err.value)


def test_health_cost_of():
    hmap = {
        Terrain.BLANK: -1,
        Terrain.SPEEDER: -2,
        Terrain.LAVA: -3,
        Terrain.MUD: -4,
    }
    mmap = {
        Terrain.BLANK: -10,
        Terrain.SPEEDER: -20,
        Terrain.LAVA: -30,
        Terrain.MUD: -40,
    }
    costs = Costs(health_costs=hmap, move_costs=mmap)
    assert costs.health_cost_of(Terrain.BLANK) == -1
    assert costs.health_cost_of(Terrain.SPEEDER) == -2
    assert costs.health_cost_of(Terrain.LAVA) == -3
    assert costs.health_cost_of(Terrain.MUD) == -4
    with pytest.raises(ValueError) as err:
        costs.health_cost_of(42)
    assert "unknown terrain: 42" in str(err.value)


def test_move_cost_of():
    hmap = {
        Terrain.BLANK: -1,
        Terrain.SPEEDER: -2,
        Terrain.LAVA: -3,
        Terrain.MUD: -4,
    }
    mmap = {
        Terrain.BLANK: -10,
        Terrain.SPEEDER: -20,
        Terrain.LAVA: -30,
        Terrain.MUD: -40,
    }
    costs = Costs(health_costs=hmap, move_costs=mmap)
    assert costs.move_cost_of(Terrain.BLANK) == -10
    assert costs.move_cost_of(Terrain.SPEEDER) == -20
    assert costs.move_cost_of(Terrain.LAVA) == -30
    assert costs.move_cost_of(Terrain.MUD) == -40
    with pytest.raises(ValueError) as err:
        costs.move_cost_of(42)
    assert "unknown terrain: 42" in str(err.value)


def test_costs_to_json_str():
    hmap = {
        Terrain.BLANK: -1,
        Terrain.SPEEDER: -2,
        Terrain.LAVA: -3,
        Terrain.MUD: -4,
    }
    mmap = {
        Terrain.BLANK: -10,
        Terrain.SPEEDER: -20,
        Terrain.LAVA: -30,
        Terrain.MUD: -40,
    }
    costs = Costs(health_costs=hmap, move_costs=mmap)
    assert costs.to_json_str() == (
        "{"
        '"health_costs": {"blank": -1, "speeder": -2, "lava": -3, "mud": -4}, '
        '"move_costs": {"blank": -10, "speeder": -20, "lava": -30, "mud": -40}'
        "}"
    )


def test_costs_from_json_str():
    s = (
        "{"
        '"health_costs": {"blank": -1, "speeder": -2, "lava": -3, "mud": -4}, '
        '"move_costs": {"blank": -10, "speeder": -20, "lava": -30, "mud": -40}'
        "}"
    )
    hmap = {
        Terrain.BLANK: -1,
        Terrain.SPEEDER: -2,
        Terrain.LAVA: -3,
        Terrain.MUD: -4,
    }
    mmap = {
        Terrain.BLANK: -10,
        Terrain.SPEEDER: -20,
        Terrain.LAVA: -30,
        Terrain.MUD: -40,
    }
    given = Costs.from_json_str(s)
    expected = Costs(health_costs=hmap, move_costs=mmap)
    assert given == expected
