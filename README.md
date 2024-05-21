# gridworld

50x50 2-D grid world with terrain

## Usage

### Initialize

```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ ./scripts/initialize
```

### Build

```
$ ./scripts/build
```

### Run

The entrypoint for running from the shell is `gridworld/main.py`.


```
$ ./gridworld/main.py --help
usage: gridworld [-h] [--dimensions DIMENSIONS] [--grid GRID] [--port PORT] [--servermode SERVERMODE] mode

Gridworld game

positional arguments:
  mode                  mode for interacting with project ['play', 'server', 'solve']

options:
  -h, --help            show this help message and exit
  --dimensions DIMENSIONS
                        dimensions for the 2-d grid
  --grid GRID           file to load grid data
  --port PORT           port to run web server on
  --servermode SERVERMODE
                        server mode ['dev', 'prod']
```

It can be started in one of three modes:

#### Solve mode

Solve mode allows:
- displaying random grids
- running a solver on a grid

```
$ ./gridworld/main.py solve --dimensions=7x5
*.+#+
#.#*#
+#.+*
.**#+
#*#+*
+**..
..+.*
```

This encoding of a grid can then be used via the `--grid` argument.

```
$ ./gridworld/main.py solve --grid=gridworld/data/grids/solvable-10x10-grid.out 
```

The solver will attempt to pilot an agent from a start position
at (0, 0) to a goal position at (m-1, n-1) [bottom-right corner].

*Caveat*:  The solver can handle grids around 20x20 okay, but much larger
takes several minutes.

#### Play mode

Play mode allows a human to pilot an agent through a grid world
via text I/O at the shell.

You can let the system generate a random grid of specified dimensions
(via `--dimensions`) or use a saved grid from a file (via `--grid`).

```
$ ./gridworld/main.py play --dimensions=7x5
terrain key with costs (H=health, M=move):
        | S |    H |    M
        |---|------|------
  blank | . |    0 |   -1
   lava | * |  -50 |  -10
    mud | # |  -10 |   -5
speeder | + |   -5 |    0
        ------------------
  01234
  -----
0|*#..*|0 <<
1|..*.#|1
2|.+**#|2
3|*+#..|3
4|...#+|4
5|..**#|5
6|*++..|6
  -----
  01234
  ^
start:   (0, 0)
goal:    (6, 4)
agent: @ (0, 0) H:200/200, M:450/450
== choose direction (u, d, l, r) and hit Enter:
```

(This feature was not requested but I thought it could be fun.)

#### Server mode

Server mode starts a FastAPI-based API server.

```
$ ./gridworld/main.py server --port 8001 --servermode dev
```

API endpoints are described below.

### Lint

Uses `flake8`.

```
$ ./scripts/lint
```

### Run code formatter

Uses [black](https://github.com/psf/black).

```
$ ./scripts/fmt
```

### Run tests locally

```
$ ./scripts/run_tests
```

### Run tests via tox

```
$ ./scripts/run_tests_with_tox
```

### Type-check via mypy

```
$ ./scripts/run_mypy
```

### Update requirements with pinned deps

(Really only should matter during development.)

```
$ ./scripts/pin_dep_versions
```

## Description

Fun toy problem to demonstrate competence with Python ecosystem as
part of an interview coding test.

This project addresses Options 2 and 3.

### Problem

```
In a 50 by 50 2-D grid world, you are given a starting point A on
one side of the grid, and an ending point B on the other side of
the grid. Your objective is to get from point A to point B. Each
grid space can be in a state of ["Blank", "Speeder", "Lava", "Mud"].
You start out with 200 points of health and 450 moves. Below is a
mapping of how much your health and moves are affected by landing
on a grid space.
[
  "Blank": {"Health": 0, "Moves": -1},
  "Speeder": {"Health": -5, "Moves": 0},
  "Lava": {"Health": -50, "Moves": -10},
  "Mud": {"Health": -10, "Moves": -5}
]
```

### Option 1

```
Build a front end React application, using Typescript, that allows
a player to use the arrow keys to play this game.
```

### Option 2

```
Build a back end API using Node.js (w/ Typescript), or Python, or
something similar, that allows a player to save the game and come
back to it later. As well as returns any relevant data to the front
end such as where the player is on the board, what the board is
configured like, how much health or moves are left, etc. Try to
include business logic such as logic on how the board is initially
configured and the change of state of the board / players as well.
We expect to be able to play the game over your API.
```

### Option 3

```
Build an application in any language (no UI necessary, terminal
output is great), that checks whether (a) The grid world level is
solvable for a given grid world level to get from point A to point
B, and (b) What the most efficient route is to get across if it is
solvable, in order to minimize health damage and moves it takes to
get from point A to point B.
```

## API endpoints

Swagger / OpenAPI interactive descriptions of these endpoints are
available at:
```
http://127.0.0.1:${port}/docs
```

### GET /games

Returns JSON representation of all games within db.

### GET /games/:game_id

Return JSON representation of specified game if present,
or 404 otherwise.

### POST /games

Creates a randomly generated game with the specified dimensions.

Request body is JSON of this shape:
```
{
  "dimensions": [5, 10]
}
```

Via curl:
```
$ curl -v --json '{"dimensions": [2, 2]}' 'http://localhost:8001/games'
```

Response is JSON:
```
{
  "game_id": 42
}
```

### PUT /games/:game_id/direction

Updates game by attempting to move agent in specified direction.

Request body is JSON of this shape:
```
{
  "direction": "D"
}
```

Response is JSON representation of updated game on success.

See helper curl script [curl-move-dir](./scripts/curl-move-dir)
for a more convenient way of moving your agent.

### GET /games/:game_id/status

Return JSON representation of the status of a game if present,
or 404 otherwise.

JSON response look like:
```
{
  "status": $status
}
```
where `$status` is one of `win`, `loss`, or `ongoing`.

## Author

[Richard W. Norton](mailto:rwtnorton@gmail.com)

## License

MIT License.  See the [LICENSE file](./LICENSE).
