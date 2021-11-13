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

    def rotate(self):
        self.dimensions.rotate()

    def translate(self, vec: Vector):
        self.position.x += vec.x
        self.position.y += vec.y

    def getPosition(self):
        lambda void: [self.position.x, self.position.y]

    def getFrontier(self):
        lambda void: [[self.position.x + self.dimensions.x, self.position.y],
                      [self.position.x, self.position.y + self.dimensions.y]]


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

    def place(self, vehicule: Vehicule) -> bool:
        p_x = self.parking_lot_dimensions.x - self.cursor.position.x
        p_y = self.parking_lot_dimensions.y - self.cursor.position.y

        if vehicule.dimensions.x > p_x:
            if vehicule.dimensions.y > p_y:
                return False
            vehicule.rotate()
        vehicule.translate(self.cursor.position)
        for i in range(self.cursor.position.x,
                       self.cursor.position.x + vehicule.dimensions.x):
            for j in range(self.cursor.position.y,
                           self.cursor.position.y + vehicule.dimensions.y):
                self.layout[i][j] = vehicule.id
        return True

    def arrange(self):
        self.vehicule_stack = []
        self.frontier = [[[0, 0]]]
        while self.cursor.id < len(self.vehicules):
            current_vehicule: Vehicule = self.vehicules[self.cursor.id - 1]
            current_frontier_array = self.frontier[self.cursor.id - 1]
            self.vehicule_stack.append(current_vehicule)
            is_placed = False
            for index, frontier in enumerate(current_frontier_array):
                self.cursor.position.x, self.cursor.position.y = frontier[
                    0], frontier[1]
                if self.place(current_vehicule):
                    self.cursor.id += 1
                    is_placed = True
                    current_frontier_array.remove(frontier)
                    frontier_x, frontier_y = frontier[
                        0] + current_vehicule.dimensions.x, frontier[
                            1] + current_vehicule.dimensions.y

                    appended_frontier = []
                    ### needs more testing
                    if frontier_x < self.parking_lot_dimensions.x and not [
                            frontier_x, frontier[1]
                    ] in current_frontier_array:
                        appended_frontier.append([frontier_x, frontier[1]])
                    if frontier_y < self.parking_lot_dimensions.y and not [
                            frontier[0], frontier_y
                    ] in current_frontier_array:
                        appended_frontier.append([frontier_x, frontier[1]])
                    current_frontier_array = current_frontier_array[:
                                                                    index] + appended_frontier + current_frontier_array[
                                                                        index +
                                                                        1:]
                    self.frontier.append(current_frontier_array)
                    break

            # else:
            #     self.cursor.id -= 1

    def print(self):
        return "\n".join(["\t".join(map(str, v)) for v in self.layout])


# inputs
vehicules = []
number_of_vehicules = 7
parking_lot_dimensions = Vector("5\t7")
if (inputs):
    parking_lot_input = input("")
    parking_lot_dimensions = Vector(parking_lot_input)
    number_of_vehicules_string = input("")
    number_of_vehicules = int(number_of_vehicules_string)
    for i in range(number_of_vehicules):
        vehicules.append(Vehicule(i + 1, input("")))
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

# grid.place(grid.vehicules[1])
# grid.place(grid.vehicules[5])

grid.arrange()

# solution
print(grid.print())
