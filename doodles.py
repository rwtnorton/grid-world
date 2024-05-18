#!/usr/bin/env python3

from random import randint, Random
import enum
from dataclasses import dataclass
from typing import Optional
from array import array
from collections.abc import Sequence, Iterable
import json
from itertools import repeat

WIDTH = 20
HEIGHT = 20

def generate_initial_position(dimensions: (int, int)) -> (int, int):
    m, _n = dimensions
    return randint(0, m-1), 0

def generate_goal_position(dimensions: (int, int)) -> (int, int):
    m, n = dimensions
    return randint(0, m-1), n-1


class Terrain(enum.IntEnum):
    """
    Terrain describes the type of terrain within a Grid.

    Uses enum.IntEnum to allow for dense packing into an array.
    """
    BLANK = enum.auto(0)
    SPEEDER = enum.auto()
    LAVA = enum.auto()
    MUD = enum.auto()

    def __str__(self):
        match self:
            case Terrain.BLANK:
                return '.'
            case Terrain.SPEEDER:
                return '+'
            case Terrain.LAVA:
                return '*'
            case Terrain.MUD:
                return '#'
        raise ValueError(f'unknown terrain type: {self!r}')

    @classmethod
    def from_str(cls, s):
        match s:
            case '.':
                return Terrain.BLANK
            case '+':
                return Terrain.SPEEDER
            case '*':
                return Terrain.LAVA
            case '#':
                return Terrain.MUD
        raise ValueError(f'unknown terrain str type: {s!r}')


#
# Keep health and movement costs decoupled from Terrain enum
# to allow for non-standard cost strategies in other games.
#
def standard_terrain_health_cost(terrain) -> int:
    match terrain:
        case Terrain.BLANK:
            return 0
        case Terrain.SPEEDER:
            return -5
        case Terrain.LAVA:
            return -50
        case Terrain.MUD:
            return -10
    raise ValueError(f'unknown terrain type: {terrain!r}')

def standard_terrain_movement_cost(terrain) -> int:
    match terrain:
        case Terrain.BLANK:
            return -1
        case Terrain.SPEEDER:
            return 0
        case Terrain.LAVA:
            return -10
        case Terrain.MUD:
            return -5
    raise ValueError(f'unknown terrain type: {terrain!r}')


@dataclass
class Grid:
    dimensions: (int, int)
    positions: Sequence[Terrain]

    def __init__(self, dimensions: (int, int), positions: Iterable[Terrain]):
        m, n = dimensions
        ps = list(positions)
        if m * n != len(ps):
            raise ValueError(f'invalid dimensions: dimensions={dimensions!r}, len(positions)={len(ps)}')
        if m <= 0:
            raise ValueError(f'non-positive row dim: {m}')
        if n <= 0:
            raise ValueError(f'non-positive col dim: {n}')
        self.dimensions = (m, n)
        # https://docs.python.org/3/library/array.html
        # B --> 'unsigned char' --> min size in bytes == 1
        self.positions = array('B', [])
        for p in ps:
            t = Terrain(p)
            # print(f'{t!r}')
            self.positions.append(t)

    @classmethod
    def from_list_of_lists(cls, list_of_lists: list[list[str]]) -> 'Grid':
        row_n = len(list_of_lists)
        if row_n == 0:
            raise ValueError(f'non-positive row count: {row_n}')
        col_n = len(list_of_lists[0])
        dimensions = (row_n, col_n)
        positions = []
        for row in list_of_lists:
            if len(row) != col_n:
                raise ValueError(f'inconsistent row len: dimensions={dimensions!r}, given={len(row)}')
            for s in row:
                t = Terrain.from_str(s)
                positions.append(t)
        return cls(dimensions, positions)

    @classmethod
    def from_json_str(cls, s: str) -> 'Grid':
        v = json.loads(s)
        if type(v) != list:
            raise ValueError(f'invalid type: expected list: {v!r}, given: {s!r}')
        for r in v:
            if type(r) != list:
                raise ValueError(f'invalid type: expected row list: {r!r}, given: {s!r}')
            if any(type(x) != str for x in r):
                raise ValueError(f'invalid type: expected list of strs: {r!r}, given: {s!r}')
        return cls.from_list_of_lists(v)

    def to_list_of_lists(self):
        m, n = self.dimensions
        result = []
        for i in range(m):
            x = i*n
            result.append([str(Terrain(t)) for t in self.positions[x:x+n]])
        return result

    @classmethod
    def from_str(cls, s: str) -> 'Grid':
        lol = [list(chars) for chars in s.split() if chars]
        return cls.from_list_of_lists(lol)

    @classmethod
    def random(cls, dimensions: (int, int), rand: Optional[Random] = None) -> 'Grid':
        if not rand:
            rand = Random()
        r, c = dimensions
        terrains = list(Terrain)
        positions = (rand.choice(terrains) for _ in range(r * c))
        return cls(dimensions, positions)

    def __get_rows(self) -> int:
        return self.dimensions[0]
    rows = property(__get_rows)

    def __get_cols(self) -> int:
        return self.dimensions[1]
    cols = property(__get_cols)

    def __str__(self):
        rows = []
        r, c = self.dimensions
        for i in range(r):
            x = c*i
            ts = self.positions[x:x+c]
            # print(f'{ts!r}')
            s = ''.join(str(Terrain(t)) for t in ts)
            rows.append(s)
        return '\n'.join(rows)

def ruler(s: str) -> str:
    rows = s.split('\n')
    m = len(rows)
    n = len(rows[0])
    # print(f'm x n = {m} x {n}')
    top_rule = '  ' + ''.join(str(i % 10) for i in range(n))
    top_bar = '  ' + ''.join(repeat('-', n))
    new_rows = [top_rule, top_bar]
    for i, row_str in enumerate(rows):
        i %= 10
        new_rows.append(f'{i}|{row_str}|{i}')
    new_rows.append(top_bar)
    new_rows.append(top_rule)
    return '\n'.join(new_rows)

def wellbeing(h: int, m: int, max_h: int, max_m: int):
    if max_h <= 0 or max_m <= 0:
        raise ValueError(f'non-positive max: max_h={max_h}, max_m={max_m}')
    if h <= 0 or m <= 0:
        return 0
    return (h * m) / (max_h * max_m)

def main():
    TOP_HEALTH = 101 # 2 * 50 + 1
    TOP_MOVE   =  21 # 2 * 10 + 1
    # iterate over all two steps, varying h and m, computing w
    for max_h in range(1, TOP_HEALTH+1):
        for max_m in range(1, TOP_MOVE+1):
            for goal in list(Terrain):
                g_s = str(goal)
                for right in list(Terrain):
                    r_s = str(right)
                    r_h = max_h + standard_terrain_health_cost(right)
                    r_m = max_m + standard_terrain_movement_cost(right)
                    r_w = wellbeing(r_h, r_m, max_h, max_m)
                    gr_h = r_h + standard_terrain_health_cost(goal)
                    gr_m = r_m + standard_terrain_movement_cost(goal)
                    gr_w = wellbeing(gr_h, gr_m, max_h, max_m)
                    for down in list(Terrain):
                        if right == down:
                            continue
                        #
                        d_s = str(down)
                        d_h = max_h + standard_terrain_health_cost(down)
                        d_m = max_m + standard_terrain_movement_cost(down)
                        d_w = wellbeing(d_h, d_m, max_h, max_m)
                        gd_h = d_h + standard_terrain_health_cost(goal)
                        gd_m = d_m + standard_terrain_movement_cost(goal)
                        gd_w = wellbeing(gd_h, gd_m, max_h, max_m)
                        special = ''
                        if (gd_h > gr_h and gd_m > gr_m and gd_w < gr_w) or (gd_h < gr_h and gd_m < gr_m and gd_w > gr_w):
                            special = ' ANOMALY'
                        print(f'H={max_h} M={max_m} :: {r_s}{g_s}: {r_s}:h={r_h},m={r_m},w={r_w:.6f} -> {r_s}{g_s}:h={gr_h},m={gr_m},w={gr_w:.6f} VS {d_s}{g_s}: {d_s}:h={d_h},m={d_m},w={d_w:.6f} -> {d_s}{g_s}:h={gd_h},m={gd_m},w={gd_w:.6f}{special}')

if __name__ == '__main__':
    main()
