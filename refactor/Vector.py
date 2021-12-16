

class Vector:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = x

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
