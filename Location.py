class Location(object):
    x = None
    y = None
    rows = ['a','b','c','d','e','f','g','h']


    def __init__(self, x: int = None, y: int = None):
        if type(x) == int and type(y) == int:
            self.x = x
            self.y = y
        elif type(x) == str:
            # Takes in a board value, ex. a1, and returns an array [0,0]
            x = x.lower()[:2]
            self.x = self.rows.index(x[0])+1
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

    def dSquaredTo(self,loc):
        return (loc.x-self.x)**2+(loc.y-self.y)**2

    def toNotation(self):
        return self.rows[self.x-1] + str(self.y)

