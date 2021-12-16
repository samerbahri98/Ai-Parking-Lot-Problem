from Vector import Vector


class Frontier:
    def __init__(self, position: Vector, rotated: bool) -> None:
        self.position: Vector = position
        self.rotated: bool = rotated

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Frontier):
            return self.position == __o.position and self.rotated == __o.rotated
        return False
