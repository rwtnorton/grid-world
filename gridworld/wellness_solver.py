import time
from copy import deepcopy
from collections import deque

# import heapq
from dataclasses import dataclass, field
from functools import cache
from typing import Tuple, List, Optional, Set

import math

from gridworld.agent import Agent
from gridworld.costs import Costs
from gridworld.direction import Direction
from gridworld.game import Game
from gridworld.grid import Grid
from gridworld.positions import valid_directions_from, translate_along
from gridworld.terrain import Terrain


@cache
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


@cache
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


def _some_game(dims=(2, 3)):
    start = (0, 0)
    m, n = dims
    goal = (m - 1, n - 1)
    # cells = [
    #     Terrain.BLANK,
    #     Terrain.LAVA,
    #     Terrain.SPEEDER,
    #     Terrain.MUD,
    #     Terrain.SPEEDER,
    #     Terrain.MUD,
    # ]
    # grid = Grid(dimensions=dims, cells=cells)
    grid = Grid.random(dims)
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

    def solve(self, debug: bool = False) -> Optional[TravelingAgent]:
        ag = deepcopy(self.game.agent)
        pos = ag.position
        ta = TravelingAgent(agent=ag, path=[pos])
        seen: Set[Tuple[Direction, Tuple[int, int]]] = set()
        dims = self.game.grid.dimensions
        dirs = valid_directions_from(position=pos, dimensions=dims)
        dir_pos_pairs = [
            (d, translate_along(position=pos, direction=d)) for d in dirs
        ]
        self._best_states[pos[0]][pos[1]] = ta
        queue = deque()
        for d, p in dir_pos_pairs:
            entry = (d, p, deepcopy(ta))
            queue.append(entry)
        t0 = time.perf_counter()
        while queue:
            from_dir, new_pos, trav_ag = queue.popleft()
            if debug:
                print(
                    f"from_dir={from_dir}"
                    f", new_pos={new_pos}"
                    f", terr={self.game.grid[new_pos]}"
                    f", trav_ag={trav_ag}"
                )
            new_agent = self.game.speculative_move(from_dir, trav_ag.agent)
            if debug:
                print(f" - new_agent={new_agent}")
            if new_agent is None or new_agent.is_dead():
                continue
            curr_best = self._best_states[new_pos[0]][new_pos[1]]
            if (
                curr_best is not None
                and curr_best.agent.health > new_agent.health
                and curr_best.agent.moves > new_agent.moves
            ):
                # If what we already have is clearly better, no need to go
                # down this road any further.
                continue
            new_path = trav_ag.path[:]
            new_path.append(new_pos)
            new_ta = TravelingAgent(agent=new_agent, path=new_path)
            if curr_best is None or curr_best.wellness < new_ta.wellness:
                self._best_states[new_pos[0]][new_pos[1]] = new_ta
            elif curr_best.wellness == new_ta.wellness and len(ta.path) < len(
                curr_best.path
            ):
                self._best_states[new_pos[0]][new_pos[1]] = new_ta
            seen.add((from_dir, new_pos))
            dirs = valid_directions_from(position=new_pos, dimensions=dims)
            dir_pos_pairs = [
                (d, translate_along(position=new_pos, direction=d))
                for d in dirs
            ]
            for d, p in dir_pos_pairs:
                if not (d, p) in seen:
                    queue.append((d, p, new_ta))
        t1 = time.perf_counter()
        dt = t1 - t0
        print(f"elapsed time: {dt:0.4f}")
        goal_r, goal_c = self.game.goal_position
        return self._best_states[goal_r][goal_c]
