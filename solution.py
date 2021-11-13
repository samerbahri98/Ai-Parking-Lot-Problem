from itertools import repeat
inputs = False
# classes


class Vector:
    def __init__(self, line) -> None:
        line_to_dimension = [int(dim) for dim in line.split("\t")]
        self.x = line_to_dimension[0]
        self.y = line_to_dimension[1]

    def rotate(self):
        self.x, self.y = self.y, self.x


class Cursor:
    def __init__(self, id, position: Vector) -> None:
        self.position = position
        self.id = id

    def translate(self, vec: Vector):
        self.position.x += vec.x
        self.position.y += vec.y


class Vehicule:
    def __init__(self, id, dimensions) -> None:
        self.id = id
        self.dimensions = Vector(dimensions)
        self.position = Vector("0\t0")
        self.rotated = False

    def rotate(self):
        self.dimensions.rotate()
        self.rotated = True

    def translate(self, vec: Vector):
        self.position.x += vec.x
        self.position.y += vec.y


class Grid:
    def __init__(self, parking_lot_dimensions: Vector, vehicules) -> None:

        self.vehicules = vehicules
        self.layout = []
        self.parking_lot_dimensions = parking_lot_dimensions
        for _ in repeat(None, parking_lot_dimensions.x):
            vector = []
            for __ in repeat(None, parking_lot_dimensions.y):
                vector.append(0)
            self.layout.append(vector)
        self.cursor = Cursor(1, Vector("0\t0"))

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

    def arrange(self):
        self.frontiers_array = [[[0, 0]]]
        while self.cursor.id < len(self.vehicules):
            # current_frontier_array = self.frontiers_array[self.cursor.id - 1]
            current_frontier_array = self.frontiers_array[0]
            is_placed = False
            for index, frontier in enumerate(current_frontier_array):
                self.vehicules[self.cursor.id -
                               1].position.x = frontier[0]
                self.vehicules[self.cursor.id -
                               1].position.y = frontier[1]
                if (self.is_placeable(self.vehicules[self.cursor.id - 1])):
                    is_placed = True
                else:
                    self.vehicules[self.cursor.id - 1].rotate()
                    if (self.is_placeable(self.vehicules[self.cursor.id - 1])):
                        is_placed = True
                if(is_placed):
                    self.place(self.vehicules[self.cursor.id - 1])
                    break
            if(is_placed):
                self.cursor.id += 1
            else:
                del self.frontiers_array[-1]
                self.cursor.id -= 1
                self.erease(self.vehicules[self.cursor.id - 1])
                self.vehicules[self.cursor.id - 1].rotate()

        return

    def print(self):
        return "\n".join(["\t".join(map(str, v)) for v in self.layout])


# inputs
vehicules = []
number_of_vehicules = 7
parking_lot_dimensions = Vector("5\t7")
if(inputs):
    parking_lot_input = input("")
    parking_lot_dimensions = Vector(parking_lot_input)
    number_of_vehicules_string = input("")
    number_of_vehicules = int(number_of_vehicules_string)
    for i in range(number_of_vehicules):
        vehicules.append(Vehicule(i+1, input("")))
else:
    # for testing
    vehicules.append(Vehicule(1, "4\t2"))
    vehicules.append(Vehicule(2, "3\t2"))
    vehicules.append(Vehicule(3, "1\t2"))
    vehicules.append(Vehicule(4, "2\t5"))
    vehicules.append(Vehicule(5, "2\t2"))
    vehicules.append(Vehicule(6, "2\t1"))
    vehicules.append(Vehicule(7, "3\t1"))

# grid
grid = Grid(parking_lot_dimensions, vehicules)

# grid.place(grid.vehicules[0])
# grid.place(grid.vehicules[1])
# grid.place(grid.vehicules[2])
# grid.place(grid.vehicules[3])

# solution
grid.arrange()
print(grid.print())
