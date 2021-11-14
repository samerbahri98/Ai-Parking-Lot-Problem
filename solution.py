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

    def compare(self, v): lambda: self.x == v.x and self.y == v.y

    def from_list(self, a):
        self.x = a[0]
        self.y = a[1]


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

        self.vehicules: list[Vehicule] = vehicules
        self.layout = []
        self.parking_lot_dimensions = parking_lot_dimensions
        for _ in repeat(None, parking_lot_dimensions.x):
            vector = []
            for __ in repeat(None, parking_lot_dimensions.y):
                vector.append(0)
            self.layout.append(vector)

        zero_vector = Vector("0\t0")
        self.cursor = Cursor(1, zero_vector)
        self.frontiers_array = [[zero_vector]]

    def is_placeable(self, vehicule: Vehicule) -> bool:
        if vehicule.position.x+vehicule.dimensions.x > self.parking_lot_dimensions.x or vehicule.position.y+vehicule.dimensions.y > self.parking_lot_dimensions.y:

            return False
        for i in range(vehicule.position.x, vehicule.position.x+vehicule.dimensions.x):
            for j in range(vehicule.position.y, vehicule.position.y+vehicule.dimensions.y):
                if self.layout[i][j] != 0:
                    # if(not inputs):
                    #     print(self.layout[i])
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
        current_frontier = self.frontiers_array[-1]
        x = vehicule.position.x+vehicule.dimensions.x
        v_x = Vector(f"{x}\t{vehicule.position.y}")
        y = vehicule.position.y+vehicule.dimensions.y
        v_y = Vector(f"{vehicule.position.x}\t{y}")
        e_x, e_y = False, False
        for frontier_vector in current_frontier:
            if frontier_vector.compare(v_x):
                e_x = True
            if frontier_vector.compare(v_y):
                e_y = True
            if e_x and e_y:
                return
        appended_frontier = []
        if (not e_x) and x < self.parking_lot_dimensions.x:
            appended_frontier.append(v_x)
        if (not e_y) and y < self.parking_lot_dimensions.y:
            appended_frontier.append(v_y)
        current_frontier = current_frontier[:index] + \
            appended_frontier + current_frontier[index+1:]
        self.frontiers_array.append(current_frontier)

    def try_to_place(self, current_vehicule_index: int) -> bool:
        is_placed = False
        current_frontier_array = self.frontiers_array[current_vehicule_index]
        for index, frontier in enumerate(current_frontier_array):
            # self.vehicules[current_vehicule_index].translate(frontier)
            self.vehicules[current_vehicule_index].position.x = frontier.x
            self.vehicules[current_vehicule_index].position.y = frontier.y
            if (self.is_placeable(self.vehicules[current_vehicule_index])):
                is_placed = True
            elif self.vehicules[current_vehicule_index].rotated == False:
                self.vehicules[current_vehicule_index].rotate()
                if (self.is_placeable(self.vehicules[current_vehicule_index])):
                    is_placed = True
            if(is_placed):
                self.place(self.vehicules[current_vehicule_index])
                self.intercept_frontier(
                    index, self.vehicules[current_vehicule_index])
                break
        return is_placed

    def rollback(self):
        del self.frontiers_array[-1]
        if(self.vehicules[self.cursor.id-1].rotated):
            self.vehicules[self.cursor.id-1].rotate()
            self.vehicules[self.cursor.id-1].rotated = False
            self.vehicules[self.cursor.id-1].position.x = 0
            self.vehicules[self.cursor.id-1].position.y = 0
        self.cursor.id -= 1
        self.erease(self.vehicules[self.cursor.id - 1])
        self.vehicules[self.cursor.id-1].rotate()

    def arrange(self):
        # initialization
        while self.cursor.id < len(self.vehicules)+1:

            current_vehicule_index = self.cursor.id - 1
            is_placed = self.try_to_place(current_vehicule_index)

            if(is_placed):
                self.cursor.id += 1

            else:
                self.rollback()
            # if(not inputs):
            #     print(f"\n--------{self.cursor.id}\n")
            #     print("\n".join(["\t".join(map(str, v)) for v in self.layout]))
            #     print("\n--------\n")
        print("\n".join(["\t".join(map(str, v)) for v in self.layout]))


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
