import copy
import json
from dataclasses import dataclass
from typing import Tuple, Optional

from gridworld.direction import Direction
from gridworld.positions import is_valid_at, translate_along, neighborhood
from gridworld.agent import Agent
from gridworld.costs import Costs
from gridworld.grid import Grid


@dataclass
class Game:
    grid: Grid
    agent: Agent
    start_position: Tuple[int, int]
    goal_position: Tuple[int, int]
    costs: Costs

    def __post_init__(self):
        dims = self.grid.dimensions
        if not is_valid_at(position=self.start_position, dimensions=dims):
            raise IndexError(
                f"invalid start_position: {self.start_position},"
                f" dimensions: {self.grid.dimensions}"
            )
        if not is_valid_at(position=self.goal_position, dimensions=dims):
            raise IndexError(
                f"invalid goal_position: {self.goal_position},"
                f" dimensions: {self.grid.dimensions}"
            )

    def to_json_str(self) -> str:
        return (
            "{"
            f'"grid": {self.grid.to_json_str()}'
            f',\n"agent": {self.agent.to_json_str()}'
            f',\n"costs": {self.costs.to_json_str()}'
            f',\n"start_position": {json.dumps(self.start_position)}'
            f',\n"goal_position": {json.dumps(self.goal_position)}'
            "}"
        )

    @classmethod
    def from_json_str(cls, json_str: str) -> "Game":
        json_data = json.loads(json_str)
        # TODO: this is a little kludgy but gets the job done.
        grid = Grid.from_json_str(json.dumps(json_data["grid"]))
        agent = Agent.from_json_str(json.dumps(json_data["agent"]))
        costs = Costs.from_json_str(json.dumps(json_data["costs"]))
        start_pos = json_data["start_position"]
        goal_pos = json_data["goal_position"]
        return cls(
            grid=grid,
            agent=agent,
            costs=costs,
            start_position=(start_pos[0], start_pos[1]),
            goal_position=(goal_pos[0], goal_pos[1]),
        )

    @classmethod
    def from_dimensions(cls, dimensions: Tuple[int, int]) -> "Game":
        m, n = dimensions
        grid = Grid.random(dimensions)
        start = (0, 0)
        goal = (m - 1, n - 1)
        agent = Agent(position=start)
        costs = Costs()
        return cls(
            grid=grid,
            agent=agent,
            costs=costs,
            start_position=start,
            goal_position=goal,
        )

    def is_win(self) -> bool:
        return (
            self.agent.position == self.goal_position and self.agent.is_alive()
        )

    def is_loss(self) -> bool:
        # Independent of agent position; if dead, even on the goal, then
        # it's still a loss.
        return not self.agent.is_alive()

    def move(self, direction: Direction) -> bool:
        """
        Performs a move of the game agent if possible, adjusting
        agent health, moves, and position accordingly.

        Returns True if the move is possible, False otherwise.
        """
        dims = self.grid.dimensions
        pos = self.agent.position
        hood = neighborhood(dimensions=dims, position=pos)
        new_pos = translate_along(position=pos, direction=direction)
        if new_pos not in hood:
            return False
        terrain = self.grid[new_pos]
        self.agent.health += self.costs.health_cost_of(terrain)
        self.agent.moves += self.costs.move_cost_of(terrain)
        self.agent.position = new_pos
        return True

    def speculative_move(
        self, direction: Direction, agent: Optional[Agent] = None
    ) -> Optional[Agent]:
        """
        Returns a copy of Agent with consequences of moving in direction, or
        None if Agent cannot move that direction.

        Does not mutate any component of this Game.
        """
        agent = agent or self.agent
        dims = self.grid.dimensions
        pos = agent.position
        hood = neighborhood(dimensions=dims, position=pos)
        new_pos = translate_along(position=pos, direction=direction)
        result = copy.deepcopy(agent)
        if new_pos not in hood:
            return None
        terrain = self.grid[new_pos]
        result.health += self.costs.health_cost_of(terrain)
        result.moves += self.costs.move_cost_of(terrain)
        result.position = new_pos
        return result
