from functools import cache
from typing import Tuple, Set

from gridworld.direction import Direction


@cache
def neighbors(position: Tuple[int, int]) -> Set[Tuple[int, int]]:
    r, c = position
    return {(r - 1, c + 0), (r + 0, c - 1), (r + 0, c + 1), (r + 1, c + 0)}


@cache
def neighborhood(
    *, dimensions: Tuple[int, int], position: Tuple[int, int]
) -> Set[Tuple[int, int]]:
    m, n = dimensions
    return {
        (r, c) for (r, c) in neighbors(position) if 0 <= r < m and 0 <= c < n
    }


@cache
def is_valid_at(
    *, dimensions: Tuple[int, int], position: Tuple[int, int]
) -> bool:
    m, n = dimensions
    r, c = position
    return 0 <= r < m and 0 <= c < n


@cache
def translate_along(
    *, direction: Direction, position: Tuple[int, int]
) -> Tuple[int, int]:
    r, c = position
    if direction == Direction.UP:
        return r - 1, c
    if direction == Direction.DOWN:
        return r + 1, c
    if direction == Direction.LEFT:
        return r, c - 1
    if direction == Direction.RIGHT:
        return r, c + 1
    raise ValueError(f"invalid direction: {direction!r}")


@cache
def valid_directions_from(
    *, dimensions: Tuple[int, int], position: Tuple[int, int]
) -> Set[Direction]:
    hood = neighborhood(dimensions=dimensions, position=position)
    dirs = [Direction(d) for d in Direction]  # to pacify mypy
    dir_pos = [
        (d, translate_along(position=position, direction=d)) for d in dirs
    ]
    return {d for d, p in dir_pos if p in hood}
