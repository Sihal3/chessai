class Location(object):
    x = None
    y = None

    def __init__(self, x: int = None, y: int = None):
        if x is not None and y is not None:
            self.x = x
            self.y = y
        elif x is not None and isinstance(x,str):
            # Takes in a board value, ex. A1, and returns an array [0,0]
            x = x.upper()[:2]
            rows = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, }
            self.x = rows[x[0]]
            self.y = int(x[1])
        else:
            raise(ValueError)

    def __str__(self):
        return "Loc(" + str(self.x) + ", " + str(self.y) + ")"

    def toArr(self):
        return [self.x, self.y]

    def isOnBoard(self):
        if (self.x > 0 and self.x < 9 and self.y > 0 and self.y < 9):
            return True
        return False
