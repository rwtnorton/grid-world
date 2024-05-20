import json
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping

from gridworld.terrain import Terrain

STD_HEALTH_COSTS = MappingProxyType(
    {
        Terrain.BLANK: 0,
        Terrain.SPEEDER: -5,
        Terrain.LAVA: -50,
        Terrain.MUD: -10,
    }
)
STD_MOVE_COSTS = MappingProxyType(
    {
        Terrain.BLANK: -1,
        Terrain.SPEEDER: 0,
        Terrain.LAVA: -10,
        Terrain.MUD: -5,
    }
)


def std_health_costs():
    return STD_HEALTH_COSTS


def std_move_costs():
    return STD_MOVE_COSTS


@dataclass(kw_only=True, frozen=True)
class Costs:
    health_costs: Mapping[Terrain, int] = field(
        default_factory=std_health_costs
    )
    move_costs: Mapping[Terrain, int] = field(default_factory=std_move_costs)

    def __post_init__(self):
        missing_health_terrains = set(Terrain) - set(self.health_costs.keys())
        if missing_health_terrains:
            missing = sorted([t.name.lower() for t in missing_health_terrains])
            raise ValueError(f"missing health terrains: {', '.join(missing)}")
        missing_move_terrains = set(Terrain) - set(self.move_costs.keys())
        if missing_move_terrains:
            missing = sorted([t.name.lower() for t in missing_move_terrains])
            raise ValueError(f"missing move terrains: {', '.join(missing)}")

    def health_cost_of(self, terrain: Terrain) -> int:
        cost = self.health_costs.get(terrain)
        if cost is None:
            raise ValueError(f"unknown terrain: {terrain!r}")
        return cost

    def move_cost_of(self, terrain: Terrain) -> int:
        cost = self.move_costs.get(terrain)
        if cost is None:
            raise ValueError(f"unknown terrain: {terrain!r}")
        return cost

    def to_json_str(self) -> str:
        hc = {t.abbr: v for (t, v) in self.health_costs.items()}
        mc = {t.abbr: v for (t, v) in self.move_costs.items()}
        v = {
            "health_costs": hc,
            "move_costs": mc,
        }
        return json.dumps(v)

    @classmethod
    def from_json_str(cls, json_str: str) -> "Costs":
        # print(f"json_str: {json_str!r}")
        m = json.loads(json_str)
        # print(f"m: {m!r}")
        hmap = {Terrain.from_abbr(k): v for k, v in m["health_costs"].items()}
        mmap = {Terrain.from_abbr(k): v for k, v in m["move_costs"].items()}
        return cls(health_costs=hmap, move_costs=mmap)
