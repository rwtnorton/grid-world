# gridworld

50x50 2-D grid world with terrain

## Usage

```
$ source .venv/bin/activate
```

## Description

Fun toy problem to demonstrate competence with Python ecosystem as
part of an interview coding test.

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

## Author

[Richard W. Norton](mailto:rwtnorton@gmail.com)

## License

MIT License.  See the [LICENSE file](./LICENSE).
