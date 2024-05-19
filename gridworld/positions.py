from typing import Tuple, Set

from gridworld.direction import Direction


def neighbors(position: Tuple[int, int]) -> Set[Tuple[int, int]]:
    r, c = position
    return {(r - 1, c + 0), (r + 0, c - 1), (r + 0, c + 1), (r + 1, c + 0)}


def neighborhood(
    *, dimensions: Tuple[int, int], position: Tuple[int, int]
) -> Set[Tuple[int, int]]:
    m, n = dimensions
    return {
        (r, c) for (r, c) in neighbors(position) if 0 <= r < m and 0 <= c < n
    }


def is_valid_at(
    *, dimensions: Tuple[int, int], position: Tuple[int, int]
) -> bool:
    m, n = dimensions
    r, c = position
    return 0 <= r < m and 0 <= c < n


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
