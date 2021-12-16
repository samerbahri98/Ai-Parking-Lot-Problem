from Vector import Vector
from Vehicule import Vehicule
from Frontier import Frontier
from itertools import repeat


class Grid:
    def __init__(self, parking_lot_dimensions: Vector, vehicules: list(Vehicule)) -> None:

        self.vehicules: list[Vehicule] = vehicules
        self.vehicules.sort(key=lambda v: v.dimensions.x * v.dimensions.y)
        self.vehicules.reverse()
        self.layout = []
        self.parking_lot_dimensions = parking_lot_dimensions
        for _ in repeat(None, parking_lot_dimensions.x):
            vector = []
            for __ in repeat(None, parking_lot_dimensions.y):
                vector.append(0)
            self.layout.append(vector)
        self.cursor = 0
        self.frontiers_array = [
            [Frontier(Vector(0, 0), False), Frontier(Vector(0, 0), True)]]

    def is_placeable(self, vehicule: Vehicule) -> bool:
        if vehicule.position.x+vehicule.dimensions.x > self.parking_lot_dimensions.x or vehicule.position.y+vehicule.dimensions.y > self.parking_lot_dimensions.y:
            return False
        for i in range(vehicule.position.x, vehicule.position.x+vehicule.dimensions.x):
            for j in range(vehicule.position.y, vehicule.position.y+vehicule.dimensions.y):
                if self.layout[i][j] != 0:
                    return False
        return True

    def place(self, vehicule: Vehicule):
        for i in range(vehicule.position.x, vehicule.position.x+vehicule.dimensions.x):
            for j in range(vehicule.position.y, vehicule.position.y+vehicule.dimensions.y):
                self.layout[i][j] = vehicule.id

    def erease(self, vehicule: Vehicule):
        for i in range(vehicule.position.x, vehicule.position.x+vehicule.dimensions.x):
            for j in range(vehicule.position.y, vehicule.position.y+vehicule.dimensions.y):
                self.layout[i][j] = 0

    def intercept_frontier(self, index: int, vehicule: Vehicule):
        current_frontiers = self.frontiers_array[-1]
        potential_frontiers = vehicule.get_potential_frontiers()
        appended_frontier = []
        for frontier in potential_frontiers:
            if frontier.position.x < self.parking_lot_dimensions.x and frontier.position.y < self.parking_lot_dimensions.y:
                is_new = True
                for current_frontier in current_frontiers:
                    if current_frontier == frontier:
                        is_new = False
                        break
                if (is_new):
                    appended_frontier.append(frontier)

        current_frontier = current_frontier[:index] + \
            appended_frontier + current_frontier[index+1:]
        self.frontiers_array.append(current_frontier)

    def try_to_place(self) -> bool:
        is_placed = False
        current_frontier_array = self.frontiers_array[self.cursor]
        for index, frontier in enumerate(current_frontier_array):
            # self.vehicules[current_vehicule_index].translate(frontier)
            self.vehicules[self.cursor].positionnate(frontier)
            if (self.is_placeable(self.vehicules[self.cursor])):
                is_placed = True
            if(is_placed):
                self.place(self.vehicules[self.cursor])
                self.intercept_frontier(
                    index, self.vehicules[self.cursor])
                break
        return is_placed

    def rollback(self):
        del self.frontiers_array[-1]
        self.vehicules[self.cursor].reset()
        self.erease(self.vehicules[self.cursor])
        self.cursor -= 1

    def arrange(self):
        # initialization
        while self.cursor < len(self.vehicules):

            is_placed = self.try_to_place()

            if(is_placed):
                self.cursor += 1

            else:
                if (self.vehicules[self.cursor].frontier == len(self.frontiers_array[-1])):
                    self.rollback()
        print("\n".join(["\t".join(map(str, v)) for v in self.layout]))
