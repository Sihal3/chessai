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

    def moves(self):
        if self.name == "PAWN":
            return [[0,0],
                  [0,1],
                  [0,2],
                  [0,-1],
                  [0,-2],
                  [1,1],
                  [-1, 1],
                  [1,-1],
                  [-1,1]]
        elif self.name == "KNIGHT":
            return [[0,0],
                    [1,2],
                    [2,1],
                    [2,-1],
                    [1,-2],
                    [-1,-2],
                    [-2,-1],
                    [-2,1],
                    [-1,2]]
        elif self.name == "BISHOP":
            return [[0,0],
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
        elif self.name == "ROOK":
            return [[0,0],
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
        elif self.name == "QUEEN":
            return [[0,0],
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
                    [1,1],
                    [-7, 0],
                    [-6, 0],
                    [-5, 0],
                    [-4, 0],
                    [-3, 0],
                    [-2, 0],
                    [-1, 0],
                    [7, 0],
                    [6, 0],
                    [5, 0],
                    [4, 0],
                    [3, 0],
                    [2, 0],
                    [1, 0],
                    [0, -7],
                    [0, -6],
                    [0, -5],
                    [0, -4],
                    [0, -3],
                    [0, -2],
                    [0, -1],
                    [0, 7],
                    [0, 6],
                    [0, 5],
                    [0, 4],
                    [0, 3],
                    [0, 2],
                    [0, 1]]
        else:
            return [[0,0],
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

    def opponent(self):
        return Team((self.value+1)%2)

class Piece(object):
    type = None
    value = None
    color = None
    x = None
    y = None
    square = None
    board = None
    hasMoved = False
    taken = False
    en_passantable = False

    def __str__(self):
        s = ''
        if(self.color == Team.WHITE):
            s += '\033[31m'
        else:
            s += '\033[34m'
        s += self.type.toString()
        s += '\033[m'
        return s

    def move(self, loc: Location):
        self.square = self.board.getSquare(loc)
        self.loc = loc
        self.x = self.square.x
        self.y = self.square.y

    def take(self):
        taken = True
        turnTaken = self.board.turn

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

# checks if square can be moved to, in that square is either empty or takeable.
def openLoc(self, loc):
    if (not self.board.isOccupied(loc) or self.board.getPiece(loc).isOpponent(self)):
        return True
    return False

def getAttackingMoves(self):
    moveList = []
    if self.type == PieceType.PAWN:
        if self.color == Team.WHITE:
            forward = 1
        else:
            forward = -1

        for loc in [Location(self.x + 1, self.y + forward), Location(self.x - 1, self.y + forward)]:
            if (loc.isOnBoard()):
                moveList.append(loc)

    elif self.type == PieceType.KNIGHT:
        for move in self.type.moves():
            loc = Location(self.x + move[0], self.y + move[1])
            if loc.isOnBoard():
                moveList.append(loc)

    elif self.type == PieceType.BISHOP:
        # to the right
        for i in [1, 2, 3, 4]:
            for x in range(1, 8):
                if i == 1:
                    loc = Location(self.x + x, self.y + x)
                elif i == 2:
                    loc = Location(self.x - x, self.y + x)
                elif i == 3:
                    loc = Location(self.x + x, self.y - x)
                else:
                    loc = Location(self.x - x, self.y - x)

                if not loc.isOnBoard():
                    break
                if self.board.isOccupied(loc):
                    moveList.append(loc)
                    break
                moveList.append(loc)

    elif self.type == PieceType.ROOK:
        for i in [1, 2, 3, 4]:
            for x in range(1, 8):
                if i == 1:
                    loc = Location(self.x + x, self.y)
                elif i == 2:
                    loc = Location(self.x - x, self.y)
                elif i == 3:
                    loc = Location(self.x, self.y + x)
                else:
                    loc = Location(self.x, self.y - x)

                if not loc.isOnBoard():
                    break
                if self.board.isOccupied(loc):
                    moveList.append(loc)
                    break
                moveList.append(loc)

    elif self.type == PieceType.QUEEN:
        for i in range(1, 9):
            for x in range(1, 8):
                if i == 1:
                    loc = Location(self.x + x, self.y)
                elif i == 2:
                    loc = Location(self.x - x, self.y)
                elif i == 3:
                    loc = Location(self.x, self.y + x)
                elif i == 4:
                    loc = Location(self.x, self.y - x)
                elif i == 5:
                    loc = Location(self.x + x, self.y + x)
                elif i == 6:
                    loc = Location(self.x - x, self.y + x)
                elif i == 7:
                    loc = Location(self.x + x, self.y - x)
                else:
                    loc = Location(self.x - x, self.y - x)

                if not loc.isOnBoard():
                    break
                if self.board.isOccupied(loc):
                    moveList.append(loc)
                    break
                moveList.append(loc)

    else:
        for move in self.type.moves():
            loc = Location(self.x + move[0], self.y + move[1])
            if (loc.isOnBoard()):
                moveList.append(loc)

    return moveList

def getLegalMoves(self, mode='str'):
    moveList = []
    if self.type == PieceType.PAWN:
        if self.color == Team.WHITE:
            forward = 1
        else:
            forward = -1

        if(self.forwardSquare.isOnBoard() and not self.forwardSquare.isOccupied()):
            moveList.append(self.forwardLoc)
            loc = Location(self.x, self.y+forward*2)
            if(loc.isOnBoard() and not self.hasMoved and not self.board.isOccupied(loc)):
                moveList.append(loc)
        for loc in self.getAttackingMoves():
            if(self.board.isOccupied(loc) and self.board.getPiece(loc).isOpponent(self)):
                moveList.append(loc)

            # check for en passant
            eploc = Location(loc.x, loc.y-forward)
            if self.board.isOccupied(eploc) and self.board.getPiece(eploc).isOpponent(self) and self.board.getPiece(eploc).en_passantable:
                moveList.append(loc)

    elif self.type == PieceType.KING:
        for move in self.getAttackingMoves():
            if self.openLoc(move):
                if not self.board.underAttack(move, self.color):
                    moveList.append(move)

        # castling
        if self.board.canKCastle(self.color):
            moveList.append(Location(7,self.y))
        if self.board.canQCastle(self.color):
            moveList.append(Location(3,self.y))

    else:
        for move in self.getAttackingMoves():
            if self.openLoc(move):
                moveList.append(move)

    moveList = self.board.removeFaults(moveList, self.loc, self.color)

    if mode == 'loc':
        return moveList
    elif mode == 'str':
        myloc = self.loc.toNotation()
        return [str(myloc+loc.toNotation()) for loc in moveList]
    elif mode == 'arr':
        [[loc.x, loc.y] for loc in moveList]
    else:
        return None

def convertType(self, l):
    if l == 'Q':
        self.type = PieceType.QUEEN
        return True
    elif l == 'R':
        self.type = PieceType.ROOK
        return True
    elif l == 'B':
        self.type = PieceType.BISHOP
        return True
    elif l == 'N':
        self.type = PieceType.KNIGHT
        return True
    else:
        return False

Piece.__init__ = pinit
Piece.getLegalMoves = getLegalMoves
Piece.openLoc = openLoc
Piece.getAttackingMoves = getAttackingMoves
Piece.convertType = convertType