from gridworld.terrain import Terrain
import gridworld.stdcosts as stdcosts


def test_standard_terrain_health_cost():
    sut = stdcosts.standard_terrain_health_cost
    assert sut(Terrain.BLANK) == 0
    assert sut(Terrain.SPEEDER) == -5
    assert sut(Terrain.LAVA) == -50
    assert sut(Terrain.MUD) == -10


def test_standard_terrain_movement_cost():
    sut = stdcosts.standard_terrain_movement_cost
    assert sut(Terrain.BLANK) == -1
    assert sut(Terrain.SPEEDER) == 0
    assert sut(Terrain.LAVA) == -10
    assert sut(Terrain.MUD) == -5
