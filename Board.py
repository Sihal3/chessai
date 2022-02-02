from Piece import *

class Square(Location):
    x = None
    y = None
    piece = None


    def __init__(self, x: int, y: int, piece: Piece):
        self.x = x
        self.y = y
        self.piece = piece

    def setPiece(self, piece: Piece):
        self.piece = piece

    def getPiece(self) -> Piece:
        return self.piece

    def removePiece(self):
        self.piece = None

    def isOccupied(self) -> boolean:
        return True if self.piece else False

def Location(object):
    x = None
    y = None

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __init__(self, loc: String):
        # Takes in a board value, ex. A1, and returns an array [0,0]
        loc = loc.upper()[:2]
        rows = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, }
        self.__init__(rows[loc[0]], int(loc[1]))

class Board():

    board = None

    def __init__(self):
        self.boardInit()
        self.turn = 0

    def boardInit(self):
        # Initiates an 8x8 array and places the starting formation of pieces
        self.board = [[Square(x,y) for x in range(1,9)] for y in range(1,9)]
        self.addPiece('R', 'A1')

    def addPiece(self, type: PieceType, color: Team, loc: Location):
        # Given a type of piece [K,Q,R] , the color of a piece, and the location to put it, add a piece on the 8x8 array
        square = self.board.getSquare(loc)
        if square.isOccupied():
            raise ValueError("Board Space is Occupied")
        else:
            square.setPiece(new Piece(type, color, loc))

    def getSquare(self, x: int, y: int) -> Square:
        return self.board[x][y]

    def getSquare(self, loc: Location) -> Square:
        return self.board[loc.x][loc.y]

    def getPiece(self, loc: Location):
        return self.board.getSquare(loc).getPiece()

    def movePiece(self, oldLoc: Location, toLoc: Location):
        # physically moves a piece on the board
        self.board[move[1]] = self.board[move[0]]
        self.board[move[0]] = None



