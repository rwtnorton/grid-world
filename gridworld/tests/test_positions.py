from gridworld.positions import (
    neighborhood,
    neighbors,
    translate_along,
    valid_directions_from,
)
from gridworld.direction import Direction


def test_neighors():
    pos = (2, 3)
    assert neighbors(pos) == {(1, 3), (3, 3), (2, 2), (2, 4)}


def test_neighborhood():
    assert neighborhood(dimensions=(2, 2), position=(0, 0)) == {
        (0, 1),
        (1, 0),
    }
    assert neighborhood(dimensions=(1, 1), position=(0, 0)) == set()
    assert neighborhood(dimensions=(3, 3), position=(1, 1)) == {
        (0, 1),
        (1, 0),
        (1, 2),
        (2, 1),
    }
    assert neighborhood(dimensions=(2, 2), position=(1, 1)) == {
        (0, 1),
        (1, 0),
    }


def test_translate_along():
    pos = (1, 1)
    assert translate_along(position=pos, direction=Direction.UP) == (0, 1)
    assert translate_along(position=pos, direction=Direction.DOWN) == (2, 1)
    assert translate_along(position=pos, direction=Direction.LEFT) == (1, 0)
    assert translate_along(position=pos, direction=Direction.RIGHT) == (1, 2)


def test_valid_directions_from():
    assert valid_directions_from(dimensions=(2, 2), position=(0, 0)) == {
        Direction.DOWN,
        Direction.RIGHT,
    }
    assert valid_directions_from(dimensions=(2, 2), position=(0, 1)) == {
        Direction.DOWN,
        Direction.LEFT,
    }
    assert valid_directions_from(dimensions=(2, 2), position=(1, 0)) == {
        Direction.UP,
        Direction.RIGHT,
    }
    assert valid_directions_from(dimensions=(2, 2), position=(1, 1)) == {
        Direction.UP,
        Direction.LEFT,
    }
    assert valid_directions_from(dimensions=(3, 3), position=(1, 1)) == {
        Direction.UP,
        Direction.DOWN,
        Direction.LEFT,
        Direction.RIGHT,
    }
    assert valid_directions_from(dimensions=(1, 1), position=(0, 0)) == set()
