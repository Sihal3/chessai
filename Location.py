class Location(object):
    x = None
    y = None

    def __init__(self, x: int = None, y: int = None, loc: str = None):
        if x and y:
            self.x = x
            self.y = y
        elif loc:
            # Takes in a board value, ex. A1, and returns an array [0,0]
            loc = loc.upper()[:2]
            rows = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, }
            self.x = rows[loc[0]]
            self.y = int(loc[1])
        else:
            raise(ValueError)
