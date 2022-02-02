from Board import *

class PieceType(Enum):
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5

    def __str__(self):
        return '{0}'.format(self.value)

    def value(self) -> int:
        if self.value == "PAWN":
            return 1
        elif self.value == "KNIGHT" || self.value == "BISHOP":
            return 3
        elif self.value == "ROOK":
            return 5
        elif self.value == "QUEEN":
            return 9
        else:
            return 100

class Team(Enum):
    WHITE = 0
    BLACK = 1

class Piece(object):
    type = None
    value = None
    color = None
    x = None
    y = None
    square = None


    def __init__(self, type: PieceType, color: Team, loc: Location()):
        self.type = type
        self.value = self.PIECEVALS[self.type]
        self.color = color
        self.square = loc
        self.x = square.x
        self.y = square.y