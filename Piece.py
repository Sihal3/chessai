from enum import Enum
from Location import Location
from Board import Board

class PieceType(Enum):
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5

    def __str__(self):
        return '{0}'.format(self.name)

    def value(self) -> int:
        if self.name == "PAWN":
            return 1
        elif self.name == "KNIGHT" or self.name == "BISHOP":
            return 3
        elif self.name == "ROOK":
            return 5
        elif self.name == "QUEEN":
            return 9
        else:
            return 100

    def toString(self) -> str:
        if self.name == "PAWN":
            return 'P'
        elif self.name == "KNIGHT":
            return 'N'
        elif self.name == "BISHOP":
            return 'B'
        elif self.name == "ROOK":
            return 'R'
        elif self.name == "QUEEN":
            return 'Q'
        else:
            return 'K'

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
    board = None

    def toString(self) -> str:
        return self.type.toString()

def pinit (self, type: PieceType, color: Team, loc: Location, board: Board):
        self.type = type
        self.value = self.type.value
        self.color = color
        self.board = board
        self.square = self.board.getSquare(loc)
        self.x = self.square.x
        self.y = self.square.y

Piece.__init__ = pinit