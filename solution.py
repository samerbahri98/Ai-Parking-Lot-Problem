inputs= False
### classes
class Dimension:
    def __init__(self, line) -> None:
        line_to_dimension = [int(dim) for dim in line.split("\t")]
        self.x = line_to_dimension[0]
        self.y = line_to_dimension[1]

    def rotate(self):
        self.x, self.y = self.y, self.x


class Vehicule:
    def __init__(self, id, dimensions) -> None:
        self.id = id
        self.dimensions = Dimension(dimensions)
        self.positions = Dimension("0\t0")


### inputs
vehicules=[]
number_of_vehicules=7
parking_lot_dimensions=Dimension("5\t7")
if(inputs):
    parking_lot_input = input("")
    parking_lot_dimensions = Dimension(parking_lot_input)
    number_of_vehicules_string = input("")
    number_of_vehicules = int(number_of_vehicules_string)
    for i in range(number_of_vehicules):
        vehicules.append(Vehicule(i+1,input("")))
else:
    #for testing
    vehicules.append(Vehicule(1,input("4\t2")))
    vehicules.append(Vehicule(1,input("3\t2")))
    vehicules.append(Vehicule(1,input("1\t2")))
    vehicules.append(Vehicule(1,input("2\t5")))
    vehicules.append(Vehicule(1,input("2\t2")))
    vehicules.append(Vehicule(1,input("2\t1")))
    vehicules.append(Vehicule(1,input("3\t1")))

### grid
grid = []

for i in range(parking_lot_dimensions.x):
    vector = []
    for j in range(parking_lot_dimensions.y):
        vector.append(-1)
    grid.append(vector)

cursor = Vehicule(1,"1\t1")



### solution
print("\n".join(["\t".join(map(str,v)) for v in grid]))