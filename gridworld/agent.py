import dataclasses
import json
from dataclasses import dataclass
from typing import Tuple


DEFAULT_HEALTH = 200
DEFAULT_MOVES = 450


@dataclass
class Agent:
    position: Tuple[int, int]
    health: int = DEFAULT_HEALTH
    max_health: int = DEFAULT_HEALTH
    moves: int = DEFAULT_MOVES
    max_moves: int = DEFAULT_MOVES

    def __post_init__(self):
        if self.max_health <= 0:
            raise ValueError(f"non-positive max_health: {self.max_health}")
        if self.max_moves <= 0:
            raise ValueError(f"non-positive max_moves: {self.max_moves}")
        # Turns out, we can have non-positive vitals if deserialized
        # from an ongoing game.
        if self.health > self.max_health:
            raise ValueError(
                f"invalid health: {self.health}, max={self.max_health}"
            )
        if self.moves > self.max_moves:
            raise ValueError(
                f"invalid moves: {self.moves}, max={self.max_moves}"
            )

    def to_json_str(self) -> str:
        return json.dumps(dataclasses.asdict(self))

    @classmethod
    def from_json_str(cls, json_str: str) -> "Agent":
        v = json.loads(json_str)
        return cls(
            position=tuple(v["position"]),
            health=v["health"],
            moves=v["moves"],
            max_health=v["max_health"],
            max_moves=v["max_moves"],
        )

    def is_healthy(self) -> bool:
        return self.health > 0

    def is_motive(self) -> bool:
        return self.moves > 0

    def is_alive(self) -> bool:
        return self.is_healthy() and self.is_motive()

    def is_dead(self) -> bool:
        return not self.is_alive()
