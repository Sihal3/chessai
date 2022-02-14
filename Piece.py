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

    _pawnMoves = [[0,0],
                  [0,1],
                  [0,2],
                  [0,-1],
                  [0,-2],
                  [1,1],
                  [-1, 1],
                  [1,-1],
                  [-1,1]]

    _knightMoves = [[0,0],
                    [1,2],
                    [2,1],
                    [2,-1],
                    [1,-2],
                    [-1,-2],
                    [-2,-1],
                    [-2,1],
                    [-1,2]]

    _bishopMoves = [[0,0],
                    [-7,-7],
                    [-6,-6],
                    [-5,-5],
                    [-4,-4],
                    [-3,-3],
                    [-2,-2],
                    [-1,-1],
                    [-7,7],
                    [-6,6],
                    [-5,5],
                    [-4,4],
                    [-3,3],
                    [-2,2],
                    [-1,1],
                    [7,-7],
                    [6,-6],
                    [5,-5],
                    [4,-4],
                    [3,-3],
                    [2,-2],
                    [1,-1],
                    [7,7],
                    [6,6],
                    [5,5],
                    [4,4],
                    [3,3],
                    [2,2],
                    [1,1]]

    _rookMoves = [[0,0],
                  [-7,0],
                  [-6,0],
                  [-5,0],
                  [-4,0],
                  [-3,0],
                  [-2,0],
                  [-1,0],
                  [7,0],
                  [6,0],
                  [5,0],
                  [4,0],
                  [3,0],
                  [2,0],
                  [1,0],
                  [0,-7],
                  [0,-6],
                  [0,-5],
                  [0,-4],
                  [0,-3],
                  [0,-2],
                  [0,-1],
                  [0,7],
                  [0,6],
                  [0,5],
                  [0,4],
                  [0,3],
                  [0,2],
                  [0,1]]

    _queenMoves = _bishopMoves+_rookMoves[1:]

    _kingMoves = [[0,0],
                  [-1,-1],
                  [-1,0],
                  [-1,1],
                  [0,1],
                  [1,1],
                  [1,0],
                  [1,-1],
                  [0,-1]]


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

    @property
    def moveIdentity(self):
        if self.name == "PAWN":
            return self._pawnMoves
        elif self.name == "KNIGHT":
            return self._knightMoves
        elif self.name == "BISHOP":
            return self._bishopMoves
        elif self.name == "ROOK":
            return self._rookMoves
        elif self.name == "QUEEN":
            return self._queenMoves
        else:
            return self._kingMoves

    # def moveIdentity(self) -> list:


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
    hasMoved = False

    def __str__(self):
        return self.type.toString()

    def move(self, loc: Location):
        self.square = self.board.getSquare(loc)
        self.loc = loc
        self.x = self.square.x
        self.y = self.square.y
        self.hasMoved = True

    @property
    def forwardSquare(self):
        return self.board.getSquare(self.forwardLoc)

    @property
    def forwardLoc(self):
        if self.color == Team.WHITE:
            forward = 1
        else:
            forward = -1
        return Location(self.x, self.y+forward)

    def isOpponent(self, pOrTeam):
        if type(pOrTeam) == Piece:
            pOrTeam = pOrTeam.color
        if pOrTeam is self.color:
            return False
        else:
            return True


def pinit (self, type: PieceType, color: Team, loc: Location, board: Board):
        self.type = type
        self.value = self.type.value
        self.color = color
        self.board = board
        self.square = self.board.getSquare(loc)
        self.loc = loc
        self.x = self.square.x
        self.y = self.square.y

def getLegalMoves (self):
    moveList = []
    if self.type == PieceType.PAWN:
        if self.color == Team.WHITE:
            forward = 1
        else:
            forward = -1
        if(not self.forwardSquare.isOccupied()):
            moveList.append(self.forwardLoc.toArr())
            if(not self.hasMoved and not self.board.getSquare(self.x, self.y+forward*2).isOccupied()):
                moveList.append([self.x, self.y+(forward*2)])
        for loc in [Location(self.x+1, self.y+forward), Location(self.x-1, self.y+forward)]:
            if(self.board.getSquare(loc).isOccupied() and self.board.getPiece(loc).isOpponent(self)):
                moveList.append(loc.toArr())
    return moveList




Piece.__init__ = pinit
Piece.getLegalMoves = getLegalMoves