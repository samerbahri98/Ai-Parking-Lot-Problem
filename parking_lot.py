from copy import copy, deepcopy
inputs = False
# classes


class Coordinates:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x: int = x
        self.y: int = y

    def from_line(self, line: str):
        line_to_dimension = [int(dim) for dim in line.split("\t")]
        self.x = line_to_dimension[0]
        self.y = line_to_dimension[1]

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Coordinates):
            return self.x == __o.x and self.y == __o.y
        return False

    def rotate(self):
        self.x, self.y = self.y, self.x

    def __add__(self, v):
        self.x, self.y = self.x+v.x, self.y+v.y

    def reset(self) -> None:
        self.x, self.y = 0, 0


class Node:
    def __init__(self, position: Coordinates, rotated: bool) -> None:
        self.position: Coordinates = position
        self.rotated: bool = rotated
        self.vehicule: Vehicule = None
        self.layout: list(list(int)) = [[]]
        self.children: list(Node) = []
        self.index = 0

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Coordinates):
            return self.x == __o.x and self.y == __o.y
        return False

    def reject(self):
        self.vehicule.reset()
        self.vehicule.positionnate(self)
        if (self.vehicule.position.x + self.vehicule.dimensions.x > len(
                self.layout) or self.vehicule.position.y+self.vehicule.dimensions.y > len(self.layout[0])):
            return True
        for i in range(self.vehicule.position.x, self.vehicule.position.x+self.vehicule.dimensions.x):
            for j in range(self.vehicule.position.y, self.vehicule.position.y+self.vehicule.dimensions.y):
                if self.layout[i][j] != 0:
                    return True
        for i in range(self.vehicule.position.x, self.vehicule.position.x+self.vehicule.dimensions.x):
            for j in range(self.vehicule.position.y, self.vehicule.position.y+self.vehicule.dimensions.y):
                self.layout[i][j] = self.vehicule.id
        return False

    def complete(self):
        if (self.vehicule.next == None):
            return True

        potential_nodes = self.vehicule.get_potential_nodes()
        appended_nodes = []
        for node in potential_nodes:
            if node.position.x < len(self.layout) and node.position.y < len(self.layout[0]):
                is_new = True
                for current_node in self.children:
                    if current_node == current_node:
                        is_new = False
                        break
                if (is_new):
                    appended_nodes.append(node)

        self.children = self.children[:self.index] + \
            appended_nodes + self.children[self.index+1:]

    def output(self):
        print("\n".join(["\t".join(map(str, v)) for v in self.layout]))

    def explore(self):
        print(self.layout)
        if (self.reject()):
            return
        if (self.complete()):
            self.output()
            exit()
        for i in range(len(self.children)):
            self.children[i].layout = self.layout
            self.children[i].vehicule = deepcopy(self.vehicule).next
            self.children[i].children = deepcopy(self.children)
            self.children[i].index = i
            self.children[i].explore()


class Vehicule:
    def __init__(self, id, dimensions, next=None, previous=None) -> None:
        self.id: int = id
        self.dimensions: Coordinates = Coordinates()
        self.dimensions.from_line(dimensions)
        self.position: Coordinates = Coordinates()
        self.rotated: bool = False
        self.frontier: int = 0
        self.next = next
        self.previous = previous

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

    def positionnate(self, node: Node):
        self.position = node.position
        if node.rotated:
            self.rotate()

    def get_potential_nodes(self):
        left = Coordinates(self.position.x+self.dimensions.x, self.position.y)
        top = Coordinates(self.position.x, self.position.y+self.dimensions.y)
        return [Node(left, False), Node(left, True), Node(top, False), Node(top, True)]


vehicules = []
number_of_vehicules = 19
parking_lot_dimensions = Coordinates()
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


vehicules.sort(key=lambda v: v.dimensions.x * v.dimensions.y)
vehicules.reverse()

for i in range(len(vehicules)-1):
    vehicules[i].next = vehicules[i+1]
    vehicules[i].previous = vehicules[i-1]

layout = []
for i in range(parking_lot_dimensions.x):
    vector = []
    for j in range(parking_lot_dimensions.y):
        vector.append(0)
    layout.append(vector)

root1 = Node(Coordinates(), False)
root1.layout = layout
root1.vehicule = deepcopy(vehicules[0])
root1.index = 0

root2 = Node(Coordinates(), True)
root2.layout = layout
root2.vehicule = deepcopy(vehicules[0])
root2.index = 1
root1.children = [root1, root2]

root1.explore()
