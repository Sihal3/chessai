from Board import Board
from Piece import PieceType, Team, Piece
from Location import Location

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
        return True if self.piece is not None else False

    def __str__(self):
        # return [N] for knight
        s = "["
        if self.piece is not None:
            s += str(self.piece)
        else:
            s += " "
        s += "]"
        return s
