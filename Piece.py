from enum import Enum

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
        elif self.value == "KNIGHT" or self.value == "BISHOP":
            return 3
        elif self.value == "ROOK":
            return 5
        elif self.value == "QUEEN":
            return 9
        else:
            return 100

    def toString(self) -> str:
        if self.value == "PAWN":
            return 'P'
        elif self.value == "KNIGHT":
            return 'N'
        elif self.value == "BISHOP":
            return 'B'
        elif self.value == "ROOK":
            return 'R'
        elif self.value == "QUEEN":
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


    def __init__(self, type: PieceType, color: Team, loc: Location, board: Board):
        self.type = type
        self.value = self.PIECEVALS[self.type]
        self.color = color
        self.board = board
        self.square = self.board.getSquare(loc)
        self.x = self.square.x
        self.y = self.square.y

    def toString(self) -> str:
        return self.type.toString()