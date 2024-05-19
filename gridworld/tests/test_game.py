import copy

from gridworld.agent import Agent
from gridworld.costs import Costs
from gridworld.direction import Direction
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


def test_game_from_json_str():
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
    json_str = (
        "{"
        '"grid": [".*", "+#"]'
        f', "agent": {agent_str}'
        f', "costs": {costs_str}'
        ', "start_position": [0, 0]'
        ', "goal_position": [1, 1]'
        "}"
    )
    given = Game.from_json_str(json_str)
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
    assert given == game


def test_game_is_win_won():
    start = (1, 1)
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
    assert game.is_win() is True


def test_game_is_win_not_won_but_alive():
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
    assert game.is_win() is False
    assert game.agent.is_alive() is True


def test_game_is_win_not_won_cuz_dead():
    start = (1, 1)
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
    agent.health = 0
    game = Game(
        grid=grid,
        start_position=start,
        goal_position=goal,
        agent=agent,
        costs=costs,
    )
    assert game.is_win() is False
    assert game.agent.is_alive() is False


def test_game_is_loss_at_goal():
    start = (1, 1)
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
    agent.health = 0
    game = Game(
        grid=grid,
        start_position=start,
        goal_position=goal,
        agent=agent,
        costs=costs,
    )
    assert game.is_win() is False
    assert game.agent.is_alive() is False
    assert game.is_loss() is True


def test_game_is_loss_before_goal():
    start = (1, 0)
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
    agent.moves = 0
    game = Game(
        grid=grid,
        start_position=start,
        goal_position=goal,
        agent=agent,
        costs=costs,
    )
    assert game.is_win() is False
    assert game.agent.is_alive() is False
    assert game.is_loss() is True


def test_game_move_ok():
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
    agent = Agent(
        position=start, health=100, max_health=100, moves=100, max_moves=100
    )
    game = Game(
        grid=grid,
        start_position=start,
        goal_position=goal,
        agent=agent,
        costs=costs,
    )
    assert game.move(Direction.RIGHT) is True
    assert game.agent.position == (0, 1)
    assert game.agent.health < 100
    assert game.agent.moves < 100
    assert game.agent.is_alive() is True
    assert game.is_win() is False


def test_game_move_invalid_direction():
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
    agent = Agent(
        position=start, health=100, max_health=100, moves=100, max_moves=100
    )
    game = Game(
        grid=grid,
        start_position=start,
        goal_position=goal,
        agent=agent,
        costs=costs,
    )
    assert game.move(Direction.UP) is False
    assert game.agent.position == start  # did not move
    assert game.agent.health == agent.max_health
    assert game.agent.moves == agent.max_moves
    assert game.agent.is_alive() is True
    assert game.is_win() is False


def test_game_move_died():
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
    agent = Agent(
        position=start, health=10, max_health=100, moves=100, max_moves=100
    )
    game = Game(
        grid=grid,
        start_position=start,
        goal_position=goal,
        agent=agent,
        costs=costs,
    )
    assert game.move(Direction.RIGHT) is True
    assert game.agent.position == (0, 1)
    assert game.agent.health <= 0
    assert game.agent.moves < 100
    assert game.agent.is_alive() is False
    assert game.is_win() is False


def test_game_move_non_win_alive():
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
    orig_health = agent.health
    orig_moves = agent.moves
    game = Game(
        grid=grid,
        start_position=start,
        goal_position=goal,
        agent=agent,
        costs=costs,
    )
    new_position = (0, 1)
    new_terrain = game.grid[new_position]
    assert game.move(Direction.RIGHT) is True
    assert game.agent.position == new_position
    assert game.agent.health == (
        orig_health + costs.health_cost_of(new_terrain)
    )
    assert game.agent.moves == (orig_moves + costs.move_cost_of(new_terrain))
    assert game.agent.is_healthy() is True
    assert game.agent.is_motive() is True
    assert game.is_win() is False
    assert game.is_loss() is False


def test_game_move_win_alive():
    start = (0, 1)
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
    orig_health = agent.health
    orig_moves = agent.moves
    game = Game(
        grid=grid,
        start_position=start,
        goal_position=goal,
        agent=agent,
        costs=costs,
    )
    new_position = (1, 1)
    new_terrain = game.grid[new_position]
    assert game.move(Direction.DOWN) is True
    assert game.agent.position == new_position
    assert game.agent.health == (
        orig_health + costs.health_cost_of(new_terrain)
    )
    assert game.agent.moves == (orig_moves + costs.move_cost_of(new_terrain))
    assert game.agent.is_healthy() is True
    assert game.agent.is_motive() is True
    assert game.is_win() is True
    assert game.is_loss() is False


def test_game_speculative_move_bad_move():
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
    double_agent = copy.deepcopy(agent)
    game = Game(
        grid=grid,
        start_position=start,
        goal_position=goal,
        agent=agent,
        costs=costs,
    )
    assert game.speculative_move(Direction.UP) is None
    assert agent == double_agent  # no change to game's agent


def test_game_speculative_move_good_move():
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
    double_agent = copy.deepcopy(agent)
    game = Game(
        grid=grid,
        start_position=start,
        goal_position=goal,
        agent=agent,
        costs=costs,
    )
    moved_agent = game.speculative_move(Direction.RIGHT)
    assert agent == double_agent  # no change to game's agent
    assert isinstance(moved_agent, Agent) is True
    assert moved_agent != agent
    assert moved_agent.position == (0, 1)
    # Moved into lava, so health and moves should have both decreased.
    assert moved_agent.health < agent.health
    assert moved_agent.moves < agent.moves
