from random import randint
from models import Engine
import os

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

class StockfishAgent(object):

    stockfish = None
    thinking_time = None

    def __init__(self, board, depth=18, elo=None, thinking_time=None):
        self.board = board

        if os.name == 'nt':
            self.stockfish = Engine(path=os.path.join('resources','stockfish', 'stockfish.exe'), depth=depth,
                              parameters={"Threads": 2, "Minimum Thinking Time": 30})
        else:
            self.stockfish = Engine(path=os.path.join('resources','stockfish', 'stockfish'), depth=depth,
                                       parameters={"Threads": 2, "Minimum Thinking Time": 30})

        if elo:
            self.stockfish.set_elo_rating(elo)
        self.thinking_time = thinking_time

    def getMove(self):
        self.stockfish.set_position(self.board.moveLog)
        if self.thinking_time:
            return self.stockfish.get_best_move_time(self.thinking_time)
        return self.stockfish.get_best_move()

class LeelaAgent(object):
    leela = None
    thinking_time = None

    def __init__(self, board, depth=18, elo=None, thinking_time=None):
        self.board = board

        if os.name == 'nt':
            self.leela = Engine(path=os.path.join('resources', 'lc0', 'lc0.exe'), depth=depth,
                                       parameters={"Threads": 2})
        else:
            self.leela = Engine(path=os.path.join('resources','lc0', 'lc0'), depth=depth,
                                       parameters={"Threads": 2})

        if elo:
            self.leela.set_elo_rating(elo)
        self.thinking_time = thinking_time

    def getMove(self):
        self.leela.set_position(self.board.moveLog)
        if self.thinking_time:
            return self.leela.get_best_move_time(self.thinking_time)
        return self.leela.get_best_move()

class MaiaAgent(object):
    leela = None
    thinking_time = None

    def __init__(self, board, depth=18, elo=None, thinking_time=None):
        self.board = board

        if os.name == 'nt':
            self.leela = Engine(path=os.path.join('resources', 'lc0', 'lc0.exe'), depth=depth,
                                       parameters={"Threads": 2})
        else:
            self.leela = Engine(path=os.path.join('resources','lc0', 'lc0'), depth=depth,
                                       parameters={"Threads": 2})

        if elo:
            self.leela.set_elo_rating(elo)
        self.thinking_time = thinking_time

    def getMove(self):
        self.leela.set_position(self.board.moveLog)
        if self.thinking_time:
            return self.leela.get_best_move_time(self.thinking_time)
        return self.leela.get_best_move()