from itertools import repeat
inputs = False


class Vector:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

    def from_line(self, line: str) -> None:
        line_to_dimension = [int(dim) for dim in line.split("\t")]
        self.x = line_to_dimension[0]
        self.y = line_to_dimension[1]

    def rotate(self):
        self.x, self.y = self.y, self.x

    def reset(self) -> None:
        self.x, self.y = 0, 0

    def set(self, v):
        self.x, self.y = v.x, v.y

    def translate(self, v):
        self.x, self.y = self.x+v.x, self.y+v.y

    def compare(self, v):
        return self.x == v.x and self.y == v.y


class Vehicule:
    def __init__(self, id: int, dimensions: str) -> None:
        self.id = id
        self.dimensions = Vector().from_line(dimensions)
        self.position = Vector()
        self.rotated = False

    def rotate(self):
        self.dimensions.rotate()
        self.rotated = True

    def translate(self, v: Vector):
        self.position.translate(v)

    def set(self, v: Vector):
        self.position.set(v)

    def reset(self):
        self.position.reset()


class Frontier:
    def __init__(self, banned_vehicules: list(int), position: Vector=Vector()):
        self.position=position
        self.banned_vehicules=banned_vehicules 
