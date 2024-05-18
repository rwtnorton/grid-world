from gridworld.grid import Grid
from gridworld.terrain import Terrain
import pytest


def test_grid_init():
    cells = [
        Terrain.BLANK,
        Terrain.LAVA,
        Terrain.SPEEDER,
        Terrain.LAVA,
        Terrain.MUD,
        Terrain.MUD,
    ]
    grid = Grid((2, 3), cells)
    assert grid.dimensions == (2, 3)
    assert list(grid.cells) == [v.value for v in cells]


def test_grid_init_bad_dims():
    cells = [
        Terrain.BLANK,
        Terrain.LAVA,
        Terrain.SPEEDER,
        Terrain.LAVA,
        Terrain.MUD,
        Terrain.MUD,
    ]
    with pytest.raises(ValueError) as dim_err:
        Grid((10, 3), cells)
    assert "invalid dimensions: dimensions=(10, 3), len=6" in str(
        dim_err.value
    )


def test_grid_init_bad_row_dim():
    cells = []
    with pytest.raises(ValueError) as dim_err:
        Grid((0, 3), cells)
    assert "non-positive row dim: 0" in str(dim_err.value)


def test_grid_init_bad_col_dim():
    cells = []
    with pytest.raises(ValueError) as dim_err:
        Grid((2, 0), cells)
    assert "non-positive col dim: 0" in str(dim_err.value)


def test_grid_rows():
    cells = [
        Terrain.BLANK,
        Terrain.LAVA,
        Terrain.SPEEDER,
        Terrain.LAVA,
        Terrain.MUD,
        Terrain.MUD,
    ]
    grid = Grid((2, 3), cells)
    assert grid.rows == 2


def test_grid_cols():
    cells = [
        Terrain.BLANK,
        Terrain.LAVA,
        Terrain.SPEEDER,
        Terrain.LAVA,
        Terrain.MUD,
        Terrain.MUD,
    ]
    grid = Grid((2, 3), cells)
    assert grid.cols == 3


def test_grid_str():
    cells = [
        Terrain.BLANK,
        Terrain.LAVA,
        Terrain.SPEEDER,
        Terrain.LAVA,
        Terrain.MUD,
        Terrain.MUD,
    ]
    grid = Grid((2, 3), cells)
    assert str(grid) == ".*+\n*##"


def test_grid_getitem():
    cells = [
        Terrain.BLANK,
        Terrain.LAVA,
        Terrain.SPEEDER,
        Terrain.LAVA,
        Terrain.MUD,
        Terrain.MUD,
    ]
    grid = Grid((2, 3), cells)
    assert grid[0, 0] == Terrain.BLANK
    assert grid[0, 1] == Terrain.LAVA
    assert grid[0, 2] == Terrain.SPEEDER
    assert grid[1, 0] == Terrain.LAVA
    assert grid[1, 1] == Terrain.MUD
    assert grid[1, 2] == Terrain.MUD
    # ensure out-of-bounds indices throw exceptions
    with pytest.raises(IndexError) as row_ex:
        grid[3, 0]
    assert "row index out of bounds: 3" in str(row_ex.value)
    with pytest.raises(IndexError) as col_ex:
        grid[0, 10]
    assert "col index out of bounds: 10" in str(col_ex.value)
    # same cells, different shape
    grid2 = Grid((3, 2), cells)
    assert grid2[0, 0] == Terrain.BLANK
    assert grid2[0, 1] == Terrain.LAVA
    assert grid2[1, 0] == Terrain.SPEEDER
    assert grid2[1, 1] == Terrain.LAVA
    assert grid2[2, 0] == Terrain.MUD
    assert grid2[2, 1] == Terrain.MUD


def test_grid_to_rows():
    cells = [
        Terrain.BLANK,
        Terrain.LAVA,
        Terrain.SPEEDER,
        Terrain.LAVA,
        Terrain.MUD,
        Terrain.MUD,
    ]
    grid = Grid((2, 3), cells)
    assert grid.to_rows() == [".*+", "*##"]


def test_grid_to_json_str():
    cells = [
        Terrain.BLANK,
        Terrain.LAVA,
        Terrain.SPEEDER,
        Terrain.LAVA,
        Terrain.MUD,
        Terrain.MUD,
    ]
    grid = Grid((2, 3), cells)
    assert grid.to_json_str() == '[".*+", "*##"]'


def test_grid_from_rows():
    rows = [".*+", "*##"]
    dims = (2, 3)
    grid = Grid.from_rows(rows)
    cells = [
        Terrain.BLANK,
        Terrain.LAVA,
        Terrain.SPEEDER,
        Terrain.LAVA,
        Terrain.MUD,
        Terrain.MUD,
    ]
    # fields are equivalent
    assert grid.dimensions == dims
    assert [Terrain(c) for c in grid.cells] == cells
    # and the aggregates are equivalent
    assert grid == Grid(dims, cells)


def test_grid_from_json_str():
    json_str = '[".*+", "*##"]'
    dims = (2, 3)
    grid = Grid.from_json_str(json_str)
    cells = [
        Terrain.BLANK,
        Terrain.LAVA,
        Terrain.SPEEDER,
        Terrain.LAVA,
        Terrain.MUD,
        Terrain.MUD,
    ]
    # fields are equivalent
    assert grid.dimensions == dims
    assert [Terrain(c) for c in grid.cells] == cells
    # and the aggregates are equivalent
    assert grid == Grid(dims, cells)


def test_grid_len():
    cells = [
        Terrain.BLANK,
        Terrain.LAVA,
        Terrain.SPEEDER,
        Terrain.LAVA,
        Terrain.MUD,
        Terrain.MUD,
    ]
    grid = Grid((2, 3), cells)
    assert len(grid) == 6


def test_grid_iter():
    cells = [
        Terrain.BLANK,
        Terrain.LAVA,
        Terrain.SPEEDER,
        Terrain.LAVA,
        Terrain.MUD,
        Terrain.MUD,
    ]
    grid = Grid((2, 3), cells)
    it = iter(grid)
    assert next(it) == Terrain.BLANK
    assert next(it) == Terrain.LAVA
    assert next(it) == Terrain.SPEEDER
    assert next(it) == Terrain.LAVA
    assert next(it) == Terrain.MUD
    assert next(it) == Terrain.MUD
    with pytest.raises(StopIteration):
        next(it)
