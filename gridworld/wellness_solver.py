from collections import deque
import heapq
from dataclasses import dataclass, field
from typing import Tuple, Mapping, List, Optional

import math

from gridworld.agent import Agent
from gridworld.costs import Costs
from gridworld.game import Game
from gridworld.grid import Grid
from gridworld.positions import valid_directions_from
from gridworld.terrain import Terrain


def wellness_metric(
    *, health: int, max_health: int, moves: int, max_moves: int
) -> float:
    """
    Returns metric in [0, 1] based on agent health and moves.

    When at full health and full moves, metric is 1.0.
    When at zero health or zero moves, metric is 0.0.
    """
    if max_health <= 0:
        raise ValueError(f"non-positive max_health: {max_health}")
    if max_moves <= 0:
        raise ValueError(f"non-positive max_moves: {max_moves}")
    if health < 0:
        return 0
    if moves < 0:
        return 0
    return (health * moves) / (max_health * max_moves)


def distance_metric(position: Tuple[int, int], goal: Tuple[int, int]) -> float:
    """
    Returns metric in (0, 1] based on how close position is to goal.

    When position is at goal (same), then metric is 1.0.
    Closer positions to goal will have larger metric values.
    """
    d = math.dist(position, goal)
    if position == goal or d == 0.0 or math.isclose(d, 0.0):
        return 1.0
    # Our "points" are integers, so unless the points are the same (in which
    # case their distance is 0), the smallest distance should be 1.0.
    # Given this assumption (d >= 1), we can use the inverse of d to have
    # bigger distances measure less favorably than shorter distances.
    # However, if 0 < d < 1, then this inverse would be greater than 1 and
    # would violate the expectations for this metric.  Hence, the assert below.
    assert d >= 1.0
    return 1.0 / d


@dataclass
class TravelingAgent:
    agent: Agent
    path: List[Tuple[int, int]]

    @property
    def wellness(self) -> float:
        return wellness_metric(
            health=self.agent.health,
            max_health=self.agent.max_health,
            moves=self.agent.moves,
            max_moves=self.agent.max_moves,
        )

    def proximity(self, goal: Tuple[int, int]) -> float:
        return distance_metric(position=self.agent.position, goal=goal)

    def utility_score(self, goal: Tuple[int, int]) -> float:
        """
        Returns weighted sum in [0, 1] of agent wellness and proximity to goal.

        Higher is "better".
        """
        w = self.wellness
        d = self.proximity(goal)
        # Weigh each metric of equal importance.
        return (w * 0.5) + (d * 0.5)


def _some_game():
    start = (0, 0)
    dims = (2, 3)
    goal = (1, 2)
    cells = [
        Terrain.BLANK,
        Terrain.LAVA,
        Terrain.SPEEDER,
        Terrain.MUD,
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
    return game


@dataclass
class WellnessSolver:
    game: Game
    # Mirrors the dimensions of the game's grid.
    # Holds the "best" path/agent in each element.
    _best_states: list[list[Optional[TravelingAgent]]] = field(
        default_factory=list
    )

    # Perform a breadth-first walk of the grid state space.
    def __post_init__(self):
        if not isinstance(self.game, Game):
            raise ValueError(f"invalid game: {self.game!r}")
        m, n = self.game.grid.dimensions
        self._best_states = [[None for _c in range(n)] for _r in range(m)]
        print(
            f"dims: {m} x {n},"
            f" states: {len(self._best_states)} x {len(self._best_states[0])}"
        )
