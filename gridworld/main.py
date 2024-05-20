#!/usr/bin/env python3
import argparse
import re
from typing import Tuple

from gridworld.grid import Grid
from gridworld.game import Game
from gridworld.wellness_solver import WellnessSolver, _some_game


def two_dimensions(dim_str: str) -> Tuple[int, int]:
    dim_str = dim_str.strip().strip("()[]")
    splitter = re.compile(r"[,x ]+")
    m, n = [int(s) for s in splitter.split(dim_str)]
    if not isinstance(m, int) or m <= 0 or not isinstance(n, int) or n <= 0:
        raise ValueError(f"invalid dimensions: {dim_str!r}")
    return m, n


def main():
    parser = argparse.ArgumentParser(
        prog="gridworld",
        description="Gridworld game",
    )
    parser.add_argument(
        "--dimensions",
        dest="dimensions",
        type=two_dimensions,
        default="8x8",
        required=False,
        help="dimensions for the 2-d grid",
    )
    args = parser.parse_args()
    dims = args.dimensions
    g = _some_game(dims)
    print(g.grid)
    sv = WellnessSolver(g)
    got = sv.solve()
    print(got)


if __name__ == "__main__":
    main()
