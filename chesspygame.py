import os
import io

import pygame
import game_runner
from Board import Board
from Piece import Piece, PieceType, Team

# Set up the drawing window
BOARD_SIZE = 704
SQUARE_SIZE = (BOARD_SIZE // 8)
WHITE = (233, 211, 176)
BLACK = (180, 136, 99)
SPRITES = {}


def main():
    global BOARD_SIZE
    global SQUARE_SIZE

    pygame.init()

    screen = screen_init() # creates screen and also sprites

    board = Board()

    # Run until the user asks to quit
    running = True
    while running:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                BOARD_SIZE = min(event.size[0], event.size[1])
                SQUARE_SIZE = (BOARD_SIZE // 8)
                screen = screen_init()

        render(screen, board)

    # Done! Time to quit.
    pygame.quit()

def render(screen, board):
    # Fill the background with white
    screen.fill((255, 255, 255))

    # draw squares
    for i in range(8):
        for j in range(8):
            pygame.draw.rect(screen, BLACK if (i + j) % 2 == 1 else WHITE,
                                  (i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # draw pieces
    for piece in board.getPieces('both'):
        screen.blit(SPRITES[('w' if piece.color == Team.WHITE else 'b') + piece.type.toString()], ((piece.x-1)*SQUARE_SIZE, (8-piece.y)*SQUARE_SIZE))

    # Flip the display
    pygame.display.flip()

def sprite_gen():
    global SPRITES

    SPRITES = {}

    for s in ['wK', 'wQ', 'wR', 'wB', 'wN', 'wP', 'bK', 'bQ', 'bR', 'bB', 'bN', 'bP']:
        SPRITES[s] = svg_load(os.path.join('frugale', f'{s}.svg'), SQUARE_SIZE).convert_alpha()


def svg_load(filename, scale):
    svg_string = open(filename, "rt").read()
    start = svg_string.find('<svg')
    if start > 0:
        svg_string = svg_string[:start+4] + f' width="{scale}px" height="{scale}px" ' + svg_string[start+32:]
    return pygame.image.load(io.BytesIO(svg_string.encode()))

def screen_init():
    global BOARD_SIZE
    global SQUARE_SIZE

    # discrete board size to avoid white borders
    if BOARD_SIZE % 8 != 0:
        BOARD_SIZE -= BOARD_SIZE % 8
        SQUARE_SIZE = (BOARD_SIZE // 8)

    #init screen
    screen = pygame.display.set_mode([BOARD_SIZE, BOARD_SIZE], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

    # load piece sprites
    sprite_gen()

    return screen



if __name__ == "__main__":
    main()
