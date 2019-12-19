from dataclasses import dataclass


@dataclass
class Location:
    x: int
    y: int

    def __add__(self, other):
        return Location(self.x + other.x, self.y + other.y)
