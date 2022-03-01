
# imports my other  classes
from Location import Location
from Board import Board
from Piece import Piece, PieceType, Team

def main():

    chess = Board()
    print("Let's begin the game.")

    while(not chess.gameOver):
        print(chess)
        move = input(f"Enter {chess.getActiveTeam().name}'s move: ")
        chess.move(move)


if __name__ == "__main__":
    main()
