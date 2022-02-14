class Board():
    pass

from Location import Location
from Piece import PieceType, Piece, Team
from Square import Square

class Board():

    # self.board var, it's the 8x8 matrix with Square objects.
    board = None
    # turn counter to know whether it's black or white's move
    turn = 1


    def __init__(self):
        self.boardInit()

    def boardInit(self):
        # Initiates an 8x8 array and places the starting formation of pieces
        self.board = [[Square(x,y,self) for y in range(1,9)] for x in range(1,9)]

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

    def getSquare(self, x: int = None, y: int = None) -> Square:
        if x is not None and y is not None:
            return self.board[x-1][y-1]
        elif x is not None:
            if type(x) == str:
                loc = Location(x)
            else:
                loc = x
            return self.board[loc.x-1][loc.y-1]
        else:
            raise ValueError("Improper parameters.")

    def getPiece(self, loc: Location) -> Piece:
        return self.getSquare(loc).getPiece()

    def __str__(self):
        b = ""
        for i in range(8,0,-1):
            for j in range(1,9):
                b += str(self.getSquare(Location(j,i)))
            b += "\n"
        return b

    def movePiece(self, fromLoc: Location = None, toLoc: Location = None):
        if isinstance(fromLoc, str):
            toLoc = fromLoc.upper()[-2:]
            rows = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, }
            toLoc = Location(rows[toLoc[0]], int(toLoc[1]))
        elif isinstance(fromLoc, Location):
            self._move(fromLoc, toLoc)
        else:
            raise ValueError("Improper parameters.")

        self.turn = self.turn + 1

    def _move(self, fromLoc: Location, toLoc: Location):
        piece = self.getSquare(fromLoc).getPiece()
        piece.move(toLoc)
        self.getSquare(toLoc).setPiece(piece)
        self.getSquare(fromLoc).removePiece()

    def getMovingTeam(self) -> Team:
        if (self.turn)&2==1:
            return Team.WHITE
        else:
            return Team.BLACK

    def getMoveSyntax(self):
        return """
                You can enter moves in standard format, as in Qe7, Rd5, Bxd4.
                The 'x' is optional, and you can either include or not include the 'P' for pawn moves.
                You can also enter moves with starting and ending square, like e2e4.
                Castling can be signified with O-O or O-O-O.
               """



