from gridworld.terrain import Terrain


#
# Keep health and movement costs decoupled from Terrain enum
# to allow for non-standard cost strategies in other games.
#
def standard_terrain_health_cost(terrain: Terrain) -> int:
    match terrain:
        case Terrain.BLANK:
            return 0
        case Terrain.SPEEDER:
            return -5
        case Terrain.LAVA:
            return -50
        case Terrain.MUD:
            return -10
    raise ValueError(f"unknown terrain type: {terrain!r}")


def standard_terrain_movement_cost(terrain: Terrain) -> int:
    match terrain:
        case Terrain.BLANK:
            return -1
        case Terrain.SPEEDER:
            return 0
        case Terrain.LAVA:
            return -10
        case Terrain.MUD:
            return -5
    raise ValueError(f"unknown terrain type: {terrain!r}")
