class Piece(object):

    PIECEVALS = {
        'K': 100, # king
        'Q': 9, # queen
        'R': 5, # rook
        'B': 3, # bishop
        'N': 3, # knight
        'P': 1, # pawn
    }

    def __init__(self, type, color, loc):
        self.type = type
        self.value = self.PIECEVALS[self.type]
        self.color = color
        self.position = loc



class Board(object):

    def __init__(self):
        self.boardinit()
        self.turn = 0

    def boardInit(self):
        # Initiates an 8x8 array and places the starting formation of pieces
        self.board = [[None]*8]*8
        self.addpiece('R', 'A1')

    def addPiece(self, type, color, loc):
        # Given a type of piece [K,Q,R] , the color of a piece, and the location to put it, add a piece on the 8x8 array
        if type(loc) is str:
            loc = self.locconv(loc)
        if self.board[loc[0]][loc[1]] is not None:
            raise ValueError("Board Space is Occupied")
        self.board[loc[0]][loc[1]] = Piece(type, color, loc)

    def loconv(self, loc):
        # Takes in a board value, ex. A1, and returns an array [0,0]
        loc = str(loc).upper()[:2]
        rows = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,}
        return [rows[loc[0]], int(loc[1])-1)]

    def moveconv(self, move):
        # takes in a move, Qd4, and converts it and checks legality, to an [[0,2],[2,3]]
        if len(move) == 4 or len(move) == 3:
            piece = move[1]
            endsquare = move[-2:]
        elif len(move) == 2:
            piece = 'P'
            endsquare = move[-2:]
        else:
            raise ValueError("Improper Move Format")

        startsquare = self.findpiece(piece, endsquare)

        if not self.checklegality(piece, startsquare, endsquare):
            raise ValueError("Illegal Move")


    def findpiece(self, piece, endsquare):
        type = "W" if turn == 0 else "B"


    def movepiece(self, move):
        # physically moves a piece on the board
        self.board[move[1]] = self.board[move[0]]
        self.board[move[0]] = None











