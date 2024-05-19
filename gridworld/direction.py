import enum


class Direction(enum.StrEnum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"

    @classmethod
    def from_str(cls, s: str) -> "Direction":
        return cls(s.upper()[0])
