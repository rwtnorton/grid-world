#!/usr/bin/env python3
import argparse
import operator
import os.path
import re
import subprocess
import tracemalloc
from enum import StrEnum
from itertools import repeat
from typing import Tuple

from gridworld.agent import Agent
from gridworld.costs import Costs
from gridworld.direction import Direction
from gridworld.grid import Grid
from gridworld.game import Game
from gridworld.wellness_solver import WellnessSolver


def two_dimensions(dim_str: str) -> Tuple[int, int]:
    dim_str = dim_str.strip().strip("()[]")
    splitter = re.compile(r"[,x ]+")
    m, n = [int(s) for s in splitter.split(dim_str)]
    if not isinstance(m, int) or m <= 0 or not isinstance(n, int) or n <= 0:
        raise ValueError(f"invalid dimensions: {dim_str!r}")
    return m, n


def _some_game(dims=(2, 3), grid_str=None):
    start = (0, 0)
    if grid_str is None:
        m, n = dims
        grid = Grid.random(dims)
    else:
        grid = Grid.from_str(grid_str)
        dims = grid.dimensions
        m, n = dims
    goal = (m - 1, n - 1)
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


def humansized(n0: int) -> str:
    if n0 < 1024:
        return f"{n0} bytes"
    n1, r1 = divmod(n0, 1024)
    if n1 < 1024:
        return f"{n0/1024.0:0.3f} KiB"
    n2, r2 = divmod(n1, 1024)
    if n2 < 1024:
        x = n0 / (1024.0**2)
        return f"{x:0.3f} MiB"

    x = n0 / (1024.0**3)
    return f"{x:0.3f} GiB"


class Mode(StrEnum):
    SOLVE = "solve"
    SERVER = "server"
    PLAY = "play"


def gather_game_from_args(args) -> Game:
    if args.grid is None:
        dims = args.dimensions
        return _some_game(dims=dims)
    with open(args.grid, "r") as f:
        grid_str = f.read()
        return _some_game(grid_str=grid_str)


def ruler(s: str, pos: Tuple[int, int]) -> str:
    rows = s.split("\n")
    # m = len(rows)
    n = len(rows[0])
    # print(f'm x n = {m} x {n}')
    r, c = pos
    top_rule = "  " + "".join(str(i % 10) for i in range(n))
    top_bar = "  " + "".join(repeat("-", n))
    new_rows = [top_rule, top_bar]
    for i, row_str in enumerate(rows):
        pointer = " <<" if r == i else ""
        i %= 10
        new_rows.append(f"{i}|{row_str}|{i}{pointer}")
    new_rows.append(top_bar)
    new_rows.append(top_rule)
    pointer_buf = list(repeat(" ", n))
    pointer_buf[c] = "^"
    bottom_pointer = "  " + "".join(pointer_buf)
    new_rows.append(bottom_pointer)
    return "\n".join(new_rows)


class ServerMode(StrEnum):
    DEV = "dev"
    PROD = "prod"


WEB_PATH = os.path.join("gridworld", "web.py")


def run_web_server(port: int = 8000, server_mode: ServerMode = ServerMode.DEV):
    match server_mode:
        case ServerMode.DEV:
            fastapi_subcmd = "dev"
        case ServerMode.PROD:
            fastapi_subcmd = "run"
        case _:
            raise ValueError(f"unknown server mode: {server_mode!r}")
    cmd = ["fastapi", fastapi_subcmd, WEB_PATH, "--port", str(port)]
    db_name = os.getenv("DB_NAME")
    if db_name is None:
        db_name = server_mode.name.lower()
    env = os.environ.copy()
    env["DB_NAME"] = db_name
    # print(f"web cmd: {cmd!r}")
    try:
        result = subprocess.run(cmd, env=env)
    except KeyboardInterrupt:
        exit(0)
    exit(result.returncode)


def show_costs(costs: Costs) -> None:
    terrains = sorted(
        [(t.abbr, t) for t in costs.health_costs.keys()],
        key=operator.itemgetter(0),
    )
    longest = max(len(s) for s, _t in terrains)
    sp = "".join(repeat(" ", longest))
    print("terrain key with costs (H=health, M=move):")
    print(f"{sp} | S |    H |    M")
    print(f"{sp} |---|------|------")
    for s, t in terrains:
        h = costs.health_cost_of(t)
        m = costs.move_cost_of(t)
        sym = str(t)
        print(f"{s.rjust(longest)} | {sym} | {h:>4} | {m:>4} ")
    print(f"{sp} ------------------")


def run_game_loop(game: Game):
    dir_prompt = "== choose direction (u, d, l, r) and hit Enter: "
    path = [game.agent.position]

    def show_agent_stats():
        ag = game.agent
        print(
            f"agent: @ {ag.position}"
            f" H:{ag.health}/{ag.max_health},"
            f" M:{ag.moves}/{ag.max_moves}"
        )

    while True:
        show_costs(game.costs)
        print(ruler(str(game.grid), game.agent.position))
        print(f"start:   {game.start_position}")
        print(f"goal:    {game.goal_position}")
        show_agent_stats()
        if game.is_win():
            print("Success!")
            print(f"path: {path}")
            exit(0)
        if game.is_loss():
            print("Failure!")
            print(f"path: {path}")
            exit(0)
        input_str = input(dir_prompt)
        d = Direction.from_str(input_str)
        if not game.move(d):
            print("Invalid move, enter one of:  u, d, l, r")
        else:
            path.append(game.agent.position)


def main():
    parser = argparse.ArgumentParser(
        prog="gridworld",
        description="Gridworld game",
    )
    parser.add_argument(
        "mode",
        type=Mode,
        help=(
            f"mode for interacting with project "
            f"{sorted(m.name.lower() for m in Mode)}"
        ),
    )
    parser.add_argument(
        "--dimensions",
        dest="dimensions",
        type=two_dimensions,
        default="8x8",
        required=False,
        help="dimensions for the 2-d grid",
    )
    parser.add_argument(
        "--grid",
        dest="grid",
        type=str,
        required=False,
        help="file to load grid data",
    )
    parser.add_argument(
        "--port",
        dest="port",
        type=int,
        required=False,
        default="8000",
        help="port to run web server on",
    )
    parser.add_argument(
        "--servermode",
        dest="servermode",
        type=ServerMode,
        required=False,
        default="dev",
        help=f"server mode {sorted(m.name.lower() for m in ServerMode)}",
    )
    args = parser.parse_args()
    mode = args.mode
    # print(f"mode: {mode!r}")
    match mode:
        case Mode.SOLVE:
            g = gather_game_from_args(args)
            show_costs(g.costs)
            print(g.grid)
            tracemalloc.start()
            sv = WellnessSolver(g)
            got = sv.solve()
            print(got)
            mem_pair = tracemalloc.get_traced_memory()
            print(mem_pair)
            print([humansized(i) for i in mem_pair])
            tracemalloc.stop()
        case Mode.PLAY:
            g = gather_game_from_args(args)
            run_game_loop(g)
        case Mode.SERVER:
            run_web_server(port=args.port, server_mode=args.servermode)


if __name__ == "__main__":
    main()
