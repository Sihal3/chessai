from Board import *
from Piece import *
from Location import *

class Square(Location):
    x = None
    y = None
    piece = None
    board = None

    def __init__(self, x: int, y: int, board: Board, piece: Piece = None):
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
        return s
