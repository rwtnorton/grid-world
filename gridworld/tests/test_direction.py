import pytest

from gridworld.direction import Direction


def test_direction():
    assert Direction("U") == Direction.UP
    assert Direction("D") == Direction.DOWN
    assert Direction("L") == Direction.LEFT
    assert Direction("R") == Direction.RIGHT


def test_direction_from_str():
    assert Direction.from_str("u") == Direction.UP
    assert Direction.from_str("U") == Direction.UP
    assert Direction.from_str("up") == Direction.UP
    assert Direction.from_str("D") == Direction.DOWN
    assert Direction.from_str("L") == Direction.LEFT
    assert Direction.from_str("R") == Direction.RIGHT
    with pytest.raises(ValueError) as foo_err:
        Direction.from_str("foo")
    assert "'F' is not a valid Direction" in str(foo_err.value)
    with pytest.raises(ValueError) as smiley_err:
        Direction.from_str("\u263alolollolololol")
    assert "'\u263a' is not a valid Direction" in str(smiley_err.value)
