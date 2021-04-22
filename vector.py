class Vector:
    def __init__(self, x=0, y=0):
        if isinstance(x, tuple):
            self.x = x[0]
            self.y = x[1]
        else:
            self.x = x
            self.y = y

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return Vector(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        return Vector(self.x - other, self.y - other)

    def __mod__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x % other.x, self.y % other.y)
        return Vector(self.x % other, self.y % other)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)
        return Vector(self.x * other, self.y * other)

    def __floordiv__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x // other.x, self.y // other.y)
        return Vector(self.x // other, self.y // other)

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "{} {}".format(self.x, self.y)

    def __hash__(self):
        return hash(str(self))

    def tup(self):
        return self.x, self.y