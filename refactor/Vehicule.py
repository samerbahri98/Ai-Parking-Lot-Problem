from Vector import Vector
from Frontier import Frontier


class Vehicule:
    def __init__(self, id, dimensions) -> None:
        self.id = id
        self.dimensions = Vector(dimensions)
        self.position = Vector("0\t0")
        self.rotated = False
        self.frontier = 0

    def rotate(self):
        self.dimensions.rotate()
        self.rotated = True

    def area(self):
        return self.dimensions.x * self.dimensions.y

    def reset(self):
        self.position.reset()
        if (self.rotated):
            self.rotate()
            self.rotated = False
        self.frontier = 0

    def positionnate(self, frontier: Frontier):
        self.position = frontier.position
        if frontier.rotated:
            self.rotate()

        self.frontier +=1

    def get_potential_frontiers(self):
        left = Vector(self.position.x+self.dimensions.x, self.position.y)
        top = Vector(self.position.x, self.position.y+self.dimensions.y)
        return [Frontier(left, False), Frontier(left, True), Frontier(top, False), Frontier(top, True)]
