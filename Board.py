class Board():
    pass

from Location import *
from Piece import *
from Square import *

class Board():
    board = None
    turn = 0

    def __init__(self):
        self.boardInit()

    def boardInit(self):
        # Initiates an 8x8 array and places the starting formation of pieces
        self.board = [[Square(x,y,self) for x in range(1,9)] for y in range(1,9)]

        for i in [1,8]:
            self.newPiece(PieceType.ROOK, Team((i+1)%2), Location(1,i))
            self.newPiece(PieceType.KNIGHT, Team((i+1)%2), Location(2,i))
            self.newPiece(PieceType.BISHOP, Team((i+1)%2), Location(3,i))
            self.newPiece(PieceType.QUEEN, Team((i+1)%2), Location(4,i))
            self.newPiece(PieceType.KING, Team((i+1)%2), Location(5,i))
            self.newPiece(PieceType.BISHOP, Team((i+1)%2), Location(6,i))
            self.newPiece(PieceType.KNIGHT, Team((i+1)%2), Location(7,i))
            self.newPiece(PieceType.ROOK, Team((i+1)%2), Location(8,i))

        for i in [2,7]:
            for j in range(1,9):
                self.newPiece(PieceType.PAWN, Team(i%2), Location(j,i))

    def newPiece(self, type: PieceType, color: Team, loc: Location):
        # Given a type of piece [K,Q,R] , the color of a piece, and the location to put it, add a piece on the 8x8 array
        square = self.getSquare(loc)
        if square.isOccupied():
            raise ValueError("Board Space is Occupied")
        else:
            square.setPiece(Piece(type, color, loc, self))

    def getSquare(self, x: int, y: int) -> Square:
        return self.board[x-1][y-1]

    def getSquare(self, loc: Location) -> Square:
        return self.board[loc.x-1][loc.y-1]

    def getPiece(self, loc: Location) -> Piece:
        return self.board.getSquare(loc).getPiece()

    def toString(self) -> str:
        b = ""
        for i in range(1,9):
            for j in range(1,9):
                b += self.getSquare(Location(j,i)).toString()
            b += "\n"
        return b

    #def movePiece(self, oldLoc: Location, toLoc: Location):
        # physically moves a piece on the board
       # self.board[move[1]] = self.board[move[0]]
        #self.board[move[0]] = None





