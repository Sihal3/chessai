
# imports my other  classes
from Location import Location
from Board import Board

# creates the board object that is the source of the game
chess = Board()
# outputs it to console (i added __str__ functions to print nice)
print(chess)
# test move, e4
chess.movePiece(Location("e2"), Location('e4'))
# checking results of test move
print(chess.getPiece('e4').getLegalMoves())
print(chess)

