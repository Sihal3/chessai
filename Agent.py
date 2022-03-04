from random import randint

class RandomAgent(object):

    def __init__(self, board):
        self.board = board

    def getMove(self):
        legal_moves = self.board.getLegalMoves()
        if legal_moves:
            r = randint(0, len(legal_moves) - 1)
            return legal_moves[r]
        else:
            return None