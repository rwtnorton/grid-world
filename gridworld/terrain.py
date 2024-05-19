import enum


class Terrain(enum.IntEnum):
    """
    Terrain describes the type of terrain within a Grid.

    Uses enum.IntEnum to allow for dense packing into an array.
    """

    BLANK = 0
    SPEEDER = enum.auto()
    LAVA = enum.auto()
    MUD = enum.auto()

    def __str__(self) -> str:
        match self:
            case Terrain.BLANK:
                return "."
            case Terrain.SPEEDER:
                return "+"
            case Terrain.LAVA:
                return "*"
            case Terrain.MUD:
                return "#"
        raise ValueError(f"unknown terrain type: {self!r}")

    @classmethod
    def from_str(cls, s: str) -> "Terrain":
        match s:
            case ".":
                return Terrain.BLANK
            case "+":
                return Terrain.SPEEDER
            case "*":
                return Terrain.LAVA
            case "#":
                return Terrain.MUD
        raise ValueError(f"unknown terrain str type: {s!r}")

    @property
    def abbr(self) -> str:
        return self.name.lower()

    @classmethod
    def from_abbr(cls, s: str) -> "Terrain":
        lookup = {t.abbr: t for t in Terrain}
        v = lookup.get(s)
        if v is None:
            raise ValueError(f"unknown terrain abbr: {s!r}")
        return v
