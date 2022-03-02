import os
import io

"""
     TODO 
     1. Fix Promotion
     2. Add window sound
     3. Add animations
     4. Add info bar + flip button.
"""
import pygame
from Board import Board
from Piece import Piece, PieceType, Team
from Location import Location

# Set up the drawing window
BOARD_SIZE = 704
SQUARE_SIZE = (BOARD_SIZE // 8)
WHITE = (233, 211, 176)
BLACK = (180, 136, 99)
GREEN = (45, 138, 44, 150)
YELLOW = (247,235,118, 150)
SPRITES = {}
selectedLoc = None
pieceStyle = 'frugale'

def main():
    global BOARD_SIZE
    global SQUARE_SIZE

    pygame.init()
    pygame.display.set_caption('Chess() by Nihal')
    pygame.display.set_icon(pygame.image.load('icon.png'))

    screen = screen_init() # creates screen and also sprites
    clock = pygame.time.Clock()

    board = Board()

    # Run until the user asks to quit
    running = True
    visualDelta = True

    while running:

        clock.tick(100)

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #elif event.type == pygame.FULLSCREEN:
                #BOARD_SIZE = min(event.size[0], event.size[1])
                #SQUARE_SIZE = (BOARD_SIZE // 8)
                #screen = screen_init('fullscreen')
                #visualDelta = True
            elif event.type == pygame.VIDEORESIZE:
                BOARD_SIZE = min(event.size[0], event.size[1])
                SQUARE_SIZE = (BOARD_SIZE // 8)
                screen = screen_init()
                visualDelta = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                visualDelta = click(event, board, screen)

        if visualDelta:
            render(screen, board)
            visualDelta = False

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

    # draw past move highlight
    if board.moveLog:
        fromLoc, toLoc, _ = board.convertSAN(board.moveLog[-1])
        screen.blit(SPRITES['pH'], ((fromLoc.x - 1) * SQUARE_SIZE, (8 - fromLoc.y) * SQUARE_SIZE))
        screen.blit(SPRITES['pH'], ((toLoc.x - 1) * SQUARE_SIZE, (8 - toLoc.y) * SQUARE_SIZE))

    # draw selected highlight
    if selectedLoc:
        screen.blit(SPRITES['sH'], ((selectedLoc.x-1) * SQUARE_SIZE, (8-selectedLoc.y) * SQUARE_SIZE))
        if board.getPiece(selectedLoc).color is board.getActiveTeam():
            for move in board.getPiece(selectedLoc).getLegalMoves(mode='loc'):
                if board.getPiece(move):
                    screen.blit(SPRITES['tH'], ((move.x - 1) * SQUARE_SIZE, (8 - move.y) * SQUARE_SIZE))
                else:
                    screen.blit(SPRITES['cH'], ((move.x - 1) * SQUARE_SIZE, (8 - move.y) * SQUARE_SIZE))

    # draw pieces
    for piece in board.getPieces('both'):
        screen.blit(SPRITES[('w' if piece.color == Team.WHITE else 'b') + piece.type.toString()], ((piece.x-1)*SQUARE_SIZE, (8-piece.y)*SQUARE_SIZE))

    # Flip the display
    pygame.display.flip()

def sprite_gen():
    global SPRITES

    SPRITES = {}

    for s in ['wK', 'wQ', 'wR', 'wB', 'wN', 'wP', 'bK', 'bQ', 'bR', 'bB', 'bN', 'bP']:
        SPRITES[s] = svg_load(os.path.join('piece_sprites',pieceStyle, f'{s}.svg'), SQUARE_SIZE).convert_alpha()

    # highlights

    # selectedSquareHighlight
    SPRITES['sH'] = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    SPRITES['sH'].fill(GREEN)
    SPRITES['sH'].convert_alpha()

    # possibleMovesCircleHighlight
    SPRITES['cH'] = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(SPRITES['cH'], GREEN, (SQUARE_SIZE/2, SQUARE_SIZE/2), SQUARE_SIZE/6)
    SPRITES['cH'].convert_alpha()

    # possibleTakesCircleHighlight
    SPRITES['tH'] = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    SPRITES['tH'].fill(GREEN)
    pygame.draw.circle(SPRITES['tH'], (0, 0, 0, 0), (SQUARE_SIZE/2, SQUARE_SIZE/2), SQUARE_SIZE/1.8)
    #pygame.draw.circle(SPRITES['tH'], GREEN, (SQUARE_SIZE/2, SQUARE_SIZE/2), SQUARE_SIZE/2)
    #pygame.draw.circle(SPRITES['tH'], (0, 0, 0, 0), (SQUARE_SIZE/2, SQUARE_SIZE/2), SQUARE_SIZE/2.7)
    SPRITES['tH'].convert_alpha()

    # pastMoveHighlight
    SPRITES['pH'] = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    SPRITES['pH'].fill(YELLOW)
    SPRITES['pH'].convert_alpha()



def svg_load(filename, scale):
    svg_string = open(filename, "rt").read()
    start = svg_string.find('<svg')
    if start > 0:
        if os.name == 'nt':
            svg_string = svg_string[:start + 4] + f' transform="scale({scale/50})" width="{scale}px" height="{scale}px" ' + svg_string[start + 32:]
        else:
            svg_string = svg_string[:start + 4] + f' width="{scale}px" height="{scale}px" ' + svg_string[start + 32:]
    return pygame.image.load(io.BytesIO(svg_string.encode()))

def screen_init(s=None):
    global BOARD_SIZE
    global SQUARE_SIZE

    # discrete board size to avoid white borders
    if BOARD_SIZE % 8 != 0:
        BOARD_SIZE -= BOARD_SIZE % 8
        SQUARE_SIZE = (BOARD_SIZE // 8)

    #init screen
    #if s == 'fullscreen':
     #   screen = pygame.display.set_mode([BOARD_SIZE, BOARD_SIZE], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.FULLSCREEN)
    #else:
    screen = pygame.display.set_mode([BOARD_SIZE, BOARD_SIZE], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

    # load piece sprites
    sprite_gen()

    return screen

def click(event, board, screen):
    global selectedLoc

    mouseLoc = Location(event.pos[0]//SQUARE_SIZE+1, 8-event.pos[1]//SQUARE_SIZE)

    if selectedLoc:
        b = board.move(selectedLoc, mouseLoc)
        selectedLoc = None
        if b:
            return True

    if board.getPiece(mouseLoc):
        selectedLoc = mouseLoc
    else:
        selectedLoc = None

    return True

if __name__ == "__main__":
    main()
