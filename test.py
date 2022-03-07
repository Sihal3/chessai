from stockfish import Stockfish
import os
from Board import Board
"""
stockfish = Stockfish(path=os.path.join('stockfish','stockfish'), depth=18, parameters={"Threads": 2, "Minimum Thinking Time": 30})

stockfish.set_position(["e2e4", "e7e6"])

print(stockfish.get_best_move())
"""

chess = Board()
print(chess.to_FEN())