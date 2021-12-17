from itertools import repeat
inputs = True
# classes


class Vector:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x :int = x
        self.y :int= y

    def from_line(self, line: str):
        line_to_dimension = [int(dim) for dim in line.split("\t")]
        self.x = line_to_dimension[0]
        self.y = line_to_dimension[1]

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Vector):
            return self.x == __o.x and self.y == __o.y
        return False

    def rotate(self):
        self.x, self.y = self.y, self.x


    def __add__(self,v):
        self.x, self.y = self.x+v.x, self.y+v.y

    def from_list(self, a):
        self.x = a[0]
        self.y = a[1]

    def reset(self) -> None:
        self.x, self.y = 0, 0


class Frontier:
    def __init__(self, position: Vector, rotated: bool) -> None:
        self.position: Vector = position
        self.rotated: bool = rotated

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Frontier):
            return self.position == __o.position and self.rotated == __o.rotated
        return False

class Vehicule:
    def __init__(self, id, dimensions) -> None:
        self.id:int = id
        self.dimensions:Vector = Vector()
        self.dimensions.from_line(dimensions)
        self.position:Vector = Vector()
        self.rotated:bool = False
        self.frontier:int = 0

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


class Grid:
    def __init__(self, parking_lot_dimensions: Vector, vehicules) -> None:

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
        0

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

        current_frontier = current_frontiers[:index] + \
            appended_frontier + current_frontiers[index+1:]
        self.frontiers_array.append(current_frontier)

    def try_to_place(self) -> bool:
        is_placed = False
        current_frontier_array = self.frontiers_array[self.cursor]
        for index, frontier in enumerate(current_frontier_array):
            if (index < self.vehicules[self.cursor].frontier): continue
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
        self.cursor -= 1
        self.erease(self.vehicules[self.cursor])


    def arrange(self):
        # initialization
        while self.cursor < len(self.vehicules):
            
            
            if (self.vehicules[self.cursor].frontier >= len(self.frontiers_array[self.cursor])):
                self.rollback()   

            is_placed = self.try_to_place()

            if(is_placed):
                self.cursor += 1

            else:
                self.rollback() 
                # self.erease(self.vehicules[self.cursor])
   
        print("\n".join(["\t".join(map(str, v)) for v in self.layout]))
            








vehicules = []
number_of_vehicules = 19
parking_lot_dimensions = Vector()
parking_lot_dimensions.from_line("9\t9") 
if(inputs):
    parking_lot_input = input("")
    parking_lot_dimensions.from_line(parking_lot_input)
    number_of_vehicules_string = input("")
    number_of_vehicules = int(number_of_vehicules_string)
    for i in range(number_of_vehicules):
        vehicules.append(Vehicule(i+1, input("")))
else:
    # for testing
    vehicules.append(Vehicule(1, "1\t1"))
    vehicules.append(Vehicule(2, "1\t1"))
    vehicules.append(Vehicule(3, "2\t3"))
    vehicules.append(Vehicule(4, "1\t1"))
    vehicules.append(Vehicule(5, "1\t1"))
    vehicules.append(Vehicule(6, "4\t2"))
    vehicules.append(Vehicule(7, "1\t3"))
    vehicules.append(Vehicule(8, "7\t1"))
    vehicules.append(Vehicule(9, "7\t2"))
    vehicules.append(Vehicule(10, "1\t1"))
    vehicules.append(Vehicule(11, "1\t5"))
    vehicules.append(Vehicule(12, "1\t1"))
    vehicules.append(Vehicule(13, "1\t1"))
    vehicules.append(Vehicule(14, "1\t2"))
    vehicules.append(Vehicule(15, "5\t2"))
    vehicules.append(Vehicule(16, "3\t4"))
    vehicules.append(Vehicule(17, "1\t1"))
    vehicules.append(Vehicule(18, "1\t5"))
    vehicules.append(Vehicule(19, "1\t1"))
# grid
grid = Grid(parking_lot_dimensions, vehicules)

# grid.place(grid.vehicules[0])
# grid.place(grid.vehicules[1])
# grid.place(grid.vehicules[2])
# grid.place(grid.vehicules[3])

# solution
grid.arrange()
