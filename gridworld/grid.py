# from collections.abc import Sequence
import json
from array import array
from dataclasses import dataclass
from random import Random
from typing import Iterable, Optional, Tuple

from gridworld.terrain import Terrain


@dataclass
class Grid:
    dimensions: Tuple[int, int]
    cells: array[Terrain | int]

    def __init__(self, dimensions: Tuple[int, int], cells: Iterable[Terrain]):
        m, n = dimensions
        cells = list(cells)
        if m * n != len(cells):
            raise ValueError(
                f"invalid dimensions: dimensions={dimensions!r},"
                f" len={len(cells)}"
            )
        if m <= 0:
            raise ValueError(f"non-positive row dim: {m}")
        if n <= 0:
            raise ValueError(f"non-positive col dim: {n}")
        self.dimensions = (m, n)
        # https://docs.python.org/3/library/array.html
        # B --> 'unsigned char' --> min size in bytes == 1
        self.cells = array("B", [])
        for cell in cells:
            t = Terrain(cell)
            # print(f'{t!r}')
            self.cells.append(t)

    @classmethod
    def from_rows(cls, rows: Iterable[str]) -> "Grid":
        rows = list(rows)
        m = len(rows)
        if m == 0:
            raise ValueError(f"non-positive row count: {m}")
        n = len(rows[0])
        dimensions = (m, n)
        cells = []
        for s in rows:
            if len(s) != n:
                raise ValueError(
                    f"inconsistent row len:"
                    f" dimensions={dimensions!r},"
                    f" given={len(s)}"
                )
            for c in s:
                t = Terrain.from_str(c)
                cells.append(t)
        return cls(dimensions, cells)

    @classmethod
    def from_json_str(cls, s: str) -> "Grid":
        v = json.loads(s)
        if not isinstance(v, list):
            raise ValueError(
                f"invalid type: expected list: {v!r}, given: {s!r}"
            )
        for s in v:
            if not isinstance(s, str):
                raise ValueError(
                    f"invalid row: expected string, received: {s!r} "
                )
        return cls.from_rows(v)

    def to_rows(self):
        m, n = self.dimensions
        result = []
        for i in range(m):
            x = i * n
            xn = x + n
            result.append("".join([str(Terrain(t)) for t in self.cells[x:xn]]))
        return result

    def to_json_str(self) -> str:
        return json.dumps(self.to_rows())

    @classmethod
    def from_str(cls, s: str) -> "Grid":
        rows = [chars for chars in s.split() if chars]
        return cls.from_rows(rows)

    @classmethod
    def random(
        cls, dimensions: Tuple[int, int], rand: Optional[Random] = None
    ) -> "Grid":
        if not rand:
            rand = Random()
        m, n = dimensions
        terrains = list(Terrain)
        cells = (rand.choice(terrains) for _ in range(m * n))
        return cls(dimensions, cells)

    @property
    def rows(self) -> int:
        return self.dimensions[0]

    @property
    def cols(self) -> int:
        return self.dimensions[1]

    def __getitem__(self, pos: Tuple[int, int]) -> Terrain:
        row, col = pos
        if row < 0 or row >= self.rows:
            raise IndexError(f"row index out of bounds: {row}")
        if col < 0 or col >= self.cols:
            raise IndexError(f"col index out of bounds: {col}")
        i = self.cols * row + col
        return Terrain(self.cells[i])

    def __len__(self) -> int:
        return self.rows * self.cols

    def __str__(self):
        rows = []
        m, n = self.dimensions
        for i in range(m):
            x = n * i
            xn = x + n
            ts = self.cells[x:xn]
            # print(f'{ts!r}')
            s = "".join(str(Terrain(t)) for t in ts)
            rows.append(s)
        return "\n".join(rows)

    def __iter__(self):
        return iter(Terrain(c) for c in self.cells)
