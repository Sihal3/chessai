from Board import *
from Piece import *

class Location(object):
    x = None
    y = None

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __init__(self, loc: str):
        # Takes in a board value, ex. A1, and returns an array [0,0]
        loc = loc.upper()[:2]
        rows = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, }
        self.__init__(rows[loc[0]], int(loc[1]))

class Square(Location):
    x = None
    y = None
    piece = None
    board = None

    def __init__(self, x: int, y: int, board: Board):
        self.x = x
        self.y = y
        self.board = board

    def __init__(self, x: int, y: int, board: Board, piece: Piece):
        self.x = x
        self.y = y
        self.board = board
        self.piece = piece

    def setPiece(self, piece: Piece):
        self.piece = piece

    def getPiece(self) -> Piece:
        return self.piece

    def removePiece(self):
        self.piece = None

    def isOccupied(self) -> bool:
        return True if self.piece else False

    def toString(self) -> str:
        # return [N] for knight
        s = "["
        if self.piece:
            s += self.piece.toString()
        else:
            s += " "
        s += "]"
