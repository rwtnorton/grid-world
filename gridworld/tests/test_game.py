from gridworld.agent import Agent
from gridworld.costs import Costs
from gridworld.game import Game
from gridworld.grid import Grid
from gridworld.terrain import Terrain


def test_game_init():
    start = (0, 0)
    dims = (2, 2)
    goal = (1, 1)
    cells = [
        Terrain.BLANK,
        Terrain.LAVA,
        Terrain.SPEEDER,
        Terrain.MUD,
    ]
    grid = Grid(dimensions=dims, cells=cells)
    costs = Costs()
    agent = Agent(position=start)
    game = Game(
        grid=grid,
        start_position=start,
        goal_position=goal,
        agent=agent,
        costs=costs,
    )
    assert game.grid == grid
    assert game.start_position == start
    assert game.goal_position == goal
    assert game.agent == agent
    assert game.costs == costs


def test_game_to_json_str():
    start = (0, 0)
    dims = (2, 2)
    goal = (1, 1)
    cells = [
        Terrain.BLANK,
        Terrain.LAVA,
        Terrain.SPEEDER,
        Terrain.MUD,
    ]
    grid = Grid(dimensions=dims, cells=cells)
    costs = Costs()
    agent = Agent(position=start)
    game = Game(
        grid=grid,
        start_position=start,
        goal_position=goal,
        agent=agent,
        costs=costs,
    )
    got = game.to_json_str()
    agent_str = (
        '{"position": [0, 0], "health": 200, "max_health": 200, '
        '"moves": 450, "max_moves": 450}'
    )
    costs_str = (
        "{"
        '"health_costs": {'
        '"blank": 0, "speeder": -5, "lava": -50, "mud": -10}'
        ", "
        '"move_costs": {'
        '"blank": -1, "speeder": 0, "lava": -10, "mud": -5}'
        "}"
    )
    expected = (
        "{"
        '"grid": [".*", "+#"]'
        f',\n"agent": {agent_str}'
        f',\n"costs": {costs_str}'
        ',\n"start_position": [0, 0]'
        ',\n"goal_position": [1, 1]'
        "}"
    )
    assert got == expected


# def test_game_from_json_str():
#     agent_str = (
#         '{"position": [0, 0], "health": 200, "max_health": 200, '
#         '"moves": 450, "max_moves": 450}'
#     )
#     costs_str = (
#         "{"
#         '"health_costs": {'
#         '"blank": 0, "speeder": -5, "lava": -50, "mud": -10}'
#         ", "
#         '"move_costs": {'
#         '"blank": -1, "speeder": 0, "lava": -10, "mud": -5}'
#         "}"
#     )
#     json_str = (
#         "{"
#         '"grid": [".*", "+#"]'
#         f', "agent": {agent_str}'
#         f', "costs": {costs_str}'
#         ', "start_position": [0, 0]'
#         ', "goal_position": [1, 1]'
#         "}"
#     )
#     given = Game.from_json_str(json_str)
#     start = (0, 0)
#     dims = (2, 2)
#     goal = (1, 1)
#     cells = [
#         Terrain.BLANK,
#         Terrain.LAVA,
#         Terrain.SPEEDER,
#         Terrain.MUD,
#     ]
#     grid = Grid(dimensions=dims, cells=cells)
#     costs = Costs()
#     agent = Agent(position=start)
#     game = Game(
#         grid=grid,
#         start_position=start,
#         goal_position=goal,
#         agent=agent,
#         costs=costs,
#     )
#     assert given == game
