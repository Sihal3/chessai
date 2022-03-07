class Board():
    pass

from Location import Location
from Piece import PieceType, Piece, Team
from Square import Square
import re

class Board():

    # self.board var, it's the 8x8 matrix with Square objects.
    board = None
    # turn counter to know whether it's black or white's move
    turn = 0
    moveLog = []
    pastBoards = []
    gameOver = False
    moveMode = 'san'
    takenPieces = []
    timeSincePawnMove = 0
    needPromote = False

    SAN_REGEX = re.compile(r"^([NBKRQ])?([a-h])?([1-8])?[\-x]?([a-h][1-8])(=?[nbrqkNBRQK])?[\+#]?\Z")


    def __init__(self):
        self.boardInit()

    def reset(self):
        board = None
        turn = 0
        moveLog = []
        pastBoards = []
        gameOver = False
        takenPieces = []
        timeSincePawnMove = 0

    def swapMoveMode(self):
        if self.moveMode == 'uci':
            self.moveMode = 'san'
            return True
        elif self.moveMode == 'san':
            self.moveMode = 'uci'
            return True
        return False

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

        self.pastBoards.append(str(self))

    def newPiece(self, type: PieceType, color: Team, loc: Location):
        # Given a type of piece [K,Q,R] , the color of a piece, and the location to put it, add a piece on the 8x8 array
        square = self.getSquare(loc)
        if square.isOccupied():
            raise ValueError("Board Space is Occupied")
        else:
            square.setPiece(Piece(type, color, loc, self))

    def getSquare(self, x: int = None, y: int = None) -> Square:
        try:
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
        except IndexError:
            return None

    def getPiece(self, loc: Location) -> Piece:
        return self.getSquare(loc).getPiece()

    def __str__(self):
        b = ""
        for i in range(8,0,-1):
            b += "\n"
            for j in range(1,9):
                b += str(self.getSquare(Location(j,i)))
        return b

    def move(self, fromLoc: Location = None, toLoc: Location = None, modifier=None):

        if(not self.gameOver):
            team = self.getActiveTeam()

            if isinstance(fromLoc, tuple) and not toLoc:
                fromLoc, toLoc, modifier = fromLoc
            elif isinstance(fromLoc, Location):
                pass
            elif isinstance(fromLoc, str) and not toLoc:

                # offering a draw or resigning
                if fromLoc == 'draw':
                    print("Draw accepted.")
                    self.gameOver = True
                    return '0.5-0.5'
                if fromLoc == 'resign':
                    print("You resigned.")
                    self.gameOver = True
                    if self.getActiveTeam() is Team.WHITE:
                        return '0-1'
                    else:
                        return '1-0'

                if self.moveMode == 'uci':
                    fromLoc, toLoc, modifier = self.convertUCI(fromLoc, team)
                elif self.moveMode == 'san':
                    fromLoc, toLoc, modifier = self.convertSAN(fromLoc, team)
                    if not (toLoc):
                        print(f'{fromLoc} Move invalid, please try again.')
                        return False

            else:
                print("Improper parameters.")

            if self.needPromote or (fromLoc.toNotation() + toLoc.toNotation()+(modifier if modifier else '')) in self.getLegalMoves(team):
                piece = self.getPiece(fromLoc)

                if not self.needPromote:
                    takenPiece = self.getPiece(toLoc)
                    self._move(fromLoc, toLoc)
                    piece.hasMoved = True
                    self.moveLog.append(fromLoc.toNotation() + toLoc.toNotation()+ (modifier if modifier else ''))
                    return_value = 'moved'
                    if takenPiece is not None:
                        takenPiece.take()
                        self.timeSincePawnMove = 0
                        self.takenPieces.append(takenPiece)
                        return_value = 'captured'

                    # castling, moving the rook now
                    if piece.type == PieceType.KING and fromLoc.dSquaredTo(toLoc) > 2:
                        if toLoc.x == 7:
                            self._move(Location(8,piece.y), Location(6,piece.y))
                        elif toLoc.x == 3:
                            self._move(Location(1,piece.y), Location(4,piece.y))
                        else:
                            print("ERROR, I thought this was castling...")
                        return_value = 'castled'

                # promoting
                if self.needPromote:
                    piece = self.getPromotingPawn(team)
                if piece.type == PieceType.PAWN and piece.y % 7 == 1:  # if on the final row and a pawn
                    if modifier and piece.convertType(modifier.upper()):
                        return_value = 'promoted'
                        if self.needPromote:
                            self.moveLog[-1] = self.moveLog[-1]+modifier
                        self.needPromote = False
                    else:
                        print("Promotion not specified. Please input in next move, ex. e8e8Q.")
                        self.needPromote = True
                        return 'need_promote'

                # 50 move rule
                if piece.type == PieceType.PAWN:
                    self.timeSincePawnMove = 0

                # en passant
                for p in self.getPieces(team.opponent()):
                    if p.type == PieceType.PAWN and p.en_passantable:
                        p.en_passantable = False
                if piece.type == PieceType.PAWN:
                    if fromLoc.dSquaredTo(toLoc) == 4:
                        piece.en_passantable = True
                    if fromLoc.dSquaredTo(toLoc) == 2 and takenPiece is None:
                        eploc = Location(toLoc.x, 5 if piece.color == Team.WHITE else 4)
                        takenPiece = self.getPiece(eploc)
                        self.getSquare(eploc).removePiece()
                        takenPiece.take()
                        self.timeSincePawnMove = 0
                        self.takenPieces.append(takenPiece)
                        return_value = 'captured'

                # three-fold-repitition
                if self.turn%2 == 1:
                    self.pastBoards.append(str(self))


                self.timeSincePawnMove = self.timeSincePawnMove + 1
                self.turn = self.turn + 1

                # GAME END STATES

                # check
                if (self.inCheck(team.opponent())):
                    return_value = 'checked'

                # checkmate
                if (self.inCheck(team.opponent()) and not self.getLegalMoves(team.opponent())):
                    print("And that's mate. Good game.")
                    self.gameOver = True
                    if self.getActiveTeam() is Team.WHITE:
                        return '1-0'
                    else:
                        return '0-1'
                # stalemate
                elif (not self.getLegalMoves(team.opponent())):
                    print("And that's stalement. A draw.")
                    self.gameOver = True
                    return '0.5-0.5'
                # 50 move rule
                if self.timeSincePawnMove > 99:
                    print("By the 50-move-rule, this is a draw.")
                    self.gameOver = True
                    return '0.5-0.5'
                # three-fold repitition
                for board in self.pastBoards:
                    if self.pastBoards.count(board) > 2:
                        print("Three-Fold Repetition has occurred, this match is a draw.")
                        self.gameOver = True
                        return '0.5-0.5'

                return return_value
            else:
                print("Illegal Move. Try again.")
                return False
        else:
            print("Game is Over.")
            return False


    def _move(self, fromLoc: Location, toLoc: Location):
        piece = self.getPiece(fromLoc)
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
                Enter moves in UCI format, specifying starting square and ending square like this:
                e2e4. In case of a promotion, add the letter of the promoting piece type. c7c8Q.
                Castling will be signified by the standard O-O and O-O-O, or with the king starting and ending square. 
                Type 'draw' or 'resign' to do those, if you want. 
               """

    def onTheMap(self, loc):
        if(type(loc) == Location):
            if(loc.x > 0 and loc.x < 9 and loc.y > 0 and loc.y < 9):
                return True
        return False

    def isOccupied(self, loc, y=None):
        if type(loc) != Location and type(loc) == int and type(y) == int:
            loc = Location(loc,y)
        return self.getSquare(loc).isOccupied()

    def underAttack(self, loc, team):
        if(type(loc) == str):
            loc = Location(loc)
        for row in self.board:
            for square in row:
                if square.getPiece() is not None:
                    piece = square.getPiece()
                    if piece.isOpponent(team):
                        for _, move, _ in piece.getAttackingMoves():
                            if loc.x == move.x and loc.y == move.y:
                                return True
        return False

    def inCheck(self, team):
        return self.underAttack(self.getKing(team).loc, team)

    def getKing(self, team):
        # find king
        for piece in self.getPieces(team):
            if piece.type is PieceType.KING:
                return piece
        return None

    def getLegalMoves(self, t=None, mode='str'):
        if t is None:
            team = self.getActiveTeam()
        else:
            team = t

        if self.needPromote:
            pLoc = self.getPromotingPawn(team).loc
            moveList = [(pLoc, pLoc ,'q'),(pLoc, pLoc ,'r'),(pLoc, pLoc ,'b'),(pLoc, pLoc ,'n')]
            if mode == 'loc':
                return moveList
            elif mode == 'str':
                return [str(locs[0].toNotation() + locs[1].toNotation())+locs[2] for locs in moveList]
            elif mode == 'arr':
                return [[[locs[0].y, locs[0].y], [locs[1].x, locs[1].y]] for locs in moveList]

        movelist = []
        for piece in self.getPieces(team):
            movelist = movelist + piece.getLegalMoves(mode)
        return movelist


    def getPieces(self, team):
        # find king
        pieces = []
        if isinstance(team, Team):
            for row in self.board:
                for square in row:
                    if square.getPiece() is not None:
                        if square.getPiece().color is team:
                            pieces.append(square.getPiece())
        elif team == 'both':
            for row in self.board:
                for square in row:
                    if square.getPiece() is not None:
                        pieces.append(square.getPiece())
        return pieces

    def getActiveTeam(self):
        return Team(self.turn%2)

    def removeFaults(self, moveList, team):
        newMoveList = []
        for fromLoc, toLoc, m in moveList:

            takenPiece = self.getPiece(toLoc)

            self._move(fromLoc, toLoc)
            if(not self.inCheck(team)):
                newMoveList.append((fromLoc,toLoc,m))
            self._move(toLoc, fromLoc)

            if takenPiece is not None:
                self.getSquare(toLoc).setPiece(takenPiece)

        return newMoveList

    def convertUCI(self, move, team=None):
        if move == 'O-O' or move == '0-0':
            return (Location(5, 1 if team == Team.WHITE else 8), Location(7, 1 if team == Team.WHITE else 8))
        if move == 'O-O-O' or move == '0-0-0':
            return (Location(5, 1 if team == Team.WHITE else 8), Location(3, 1 if team == Team.WHITE else 8))
        if len(move) == 4:
            return (Location(move[0:2]), Location(move[2:4]), '')
        elif len(move) == 5:
            return (Location(move[0:2]), Location(move[2:4]), move[-1])

    def convertSAN(self, move, team=None):
        if move in ['o-o', 'O-O', '0-0']:
            return (Location(5, 1 if team == Team.WHITE else 8), Location(7, 1 if team == Team.WHITE else 8),'')
        if move in ['o-o-o', 'O-O-O', '0-0-0']:
            return (Location(5, 1 if team == Team.WHITE else 8), Location(3, 1 if team == Team.WHITE else 8),'')

        match = self.SAN_REGEX.match(move) # a genius RegEx expression I found online that matches all move types

        #catch match failures
        if not match:
            return ("Unable to match input.", False, False)

        # Get target square.
        toLoc = Location(match.group(4))

        # Get the promotion piece type.
        p = match.group(5)

        # Filter by original square.
        if match.group(2) and match.group(3):
            fromLoc = Location(match.group(2)+match.group(3))
            return (fromLoc, toLoc, p)

        # Filter by piece type.
        pieces = []
        type = PieceType.fromString(match.group(1)) if match.group(1) else PieceType.PAWN
        for piece in self.getPieces(team):
            if not match.group(2) or piece.x == Location.rows.index(match.group(2))+1:
                if not match.group(3) or piece.y == int(match.group(3)):
                    if piece.type == type:
                        if (piece.loc, toLoc, '') in piece.getLegalMoves(mode='loc') or (piece.loc, toLoc, 'Q') in piece.getLegalMoves(mode='loc'):
                            pieces.append(piece)

        if len(pieces) == 1:
            return (pieces[0].loc, toLoc, p)
        elif len(pieces) > 1:
            return ('Ambiguity detected. Please add more specificity on piece origin (rank or file).', False, False)
        elif len(pieces) < 1:
            return ("That is not a legal move.", False, False)



    def canKCastle(self, team):

        if not self.KCastleAvailable(team):
            return False

        king = self.getKing(team)
        # check intervening squares
        locs = [Location(5, king.y), Location(6, king.y), Location(7, king.y)]
        for i, loc in enumerate(locs):
            if self.underAttack(loc, team):
                return False
            if i != 0:
                if self.isOccupied(loc):
                    return False

        return True

    def KCastleAvailable(self, team):
        king = self.getKing(team)

        if king.hasMoved:
            return False

        # if kingside rook is present and has not moved
        kRook = self.getPiece(Location(8, king.y))
        if kRook is None or kRook.hasMoved:
            return False

        return True

    def QCastleAvailable(self, team):
        king = self.getKing(team)

        if king.hasMoved:
            return False

        # if queenside rook is present and has not moved
        qRook = self.getPiece(Location(1, king.y))
        if qRook is None or qRook.hasMoved:
            return False

        return True

    def canQCastle(self, team):

        if not self.QCastleAvailable(team):
            return False

        king = self.getKing(team)
        # check intervening squares
        locs = [Location(5, king.y), Location(4, king.y), Location(3, king.y), Location(2, king.y)]
        for i, loc in enumerate(locs):
            if i != 3:
                if self.underAttack(loc, team):
                    return False
            if i != 0:
                if self.isOccupied(loc):
                    return False

        return True

    def getPromotingPawn(self, team):
        for piece in self.getPieces(team):
            if piece.type == PieceType.PAWN and piece.y % 7 == 1:
                return piece

    def to_FEN(self):
        fen = ''

        # board
        empty_counter = 0
        en_passant = None
        for i in range(7,-1,-1):
            for j in range(8):
                piece = self.board[j][i].getPiece()
                if piece:
                    if empty_counter:
                        fen += str(empty_counter)
                        empty_counter = 0
                    if piece.color is Team.WHITE:
                        fen += piece.type.toString()
                    else:
                        fen += piece.type.toString().lower()

                    #en-passant
                    if piece.en_passantable:
                        if piece.color is Team.WHITE:
                            en_passant = Location(piece.x, piece.y-1)
                        else:
                            en_passant = Location(piece.x, piece.y+1)

                else:
                    empty_counter += 1
            if empty_counter:
                fen += str(empty_counter)
                empty_counter = 0
            if i != 0:
                fen += '/'

        # whose turn?
        fen += ' ' + ('w' if self.getActiveTeam() is Team.WHITE else 'b') + ' '

        # castling
        fen += 'K' if self.KCastleAvailable(Team.WHITE) else ''
        fen += 'Q' if self.QCastleAvailable(Team.WHITE) else ''
        fen += 'k' if self.KCastleAvailable(Team.BLACK) else ''
        fen += 'q' if self.QCastleAvailable(Team.BLACK) else ''
        fen += ' '

        # en passant
        if en_passant:
            fen += en_passant.toNotation() + ' '
        else:
            fen += '- '

        # halfmoves since pawn/capture
        fen += str(self.timeSincePawnMove) + ' '

        # turn number
        fen += str(self.turn//2+1)

        return fen


