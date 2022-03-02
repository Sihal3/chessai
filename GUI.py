import os
import io

"""
     TODO 
     1. Fix Promotion
     2. Add window sound
     3. Add animations
     4. Add info bar + flip button.
     5. Multiple piece styles
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
autoQueen = False

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
    move_return = None

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
                move_return = click(event, board, screen, move_return)
                visualDelta = bool(move_return)


        if visualDelta:
            render(screen, board, move_return)
            visualDelta = False

    # Done! Time to quit.
    pygame.quit()

def render(screen, board, move_return):
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

    # draw promoting menu
    if move_return == 'need_promote':
        draw_promote(screen, board)

    # Flip the display
    pygame.display.flip()

def sprite_gen():
    global SPRITES

    SPRITES = {}

    for s in ['wK', 'wQ', 'wR', 'wB', 'wN', 'wP', 'bK', 'bQ', 'bR', 'bB', 'bN', 'bP']:
        path = os.path.join('piece_sprites',pieceStyle, f'{s}.')
        if os.path.exists(path+'svg'):
            SPRITES[s] = svg_load((path+'svg'), SQUARE_SIZE).convert_alpha()
        elif os.path.exists(path+'png'):
            SPRITES[s] = pygame.image.load(path+'png').convert_alpha()
            SPRITES[s] = pygame.transform.smoothscale(SPRITES[s], (SQUARE_SIZE, SQUARE_SIZE))
        else:
            raise FileNotFoundError("Sprites not found.")

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
            svg_string = svg_string[:start + 4] + f' transform="scale({scale/50})"' + svg_string[start + 4:]

        windexStart = svg_string.find('width="', start)
        windexEnd = svg_string.find('"', windexStart+len('width="'))
        if windexStart > 0 and windexEnd > 0:
            svg_string = svg_string[:windexStart+len('width="')] + f'{scale}px' + svg_string[windexEnd:]

        hindexStart = svg_string.find('height="', start)
        hindexEnd = svg_string.find('"', hindexStart+len('height="'))
        if hindexStart > 0 and hindexEnd > 0:
            svg_string = svg_string[:hindexStart+len('height="')] + f'{scale}px' + svg_string[hindexEnd:]


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

def click(event, board, screen, move_return):
    global selectedLoc

    mouseLoc = Location(event.pos[0]//SQUARE_SIZE+1, 8-event.pos[1]//SQUARE_SIZE)

    if move_return == 'need_promote':
        x = (board.getPromotingPawn(board.getActiveTeam()).x)
        y = (8 if board.getActiveTeam() is Team.WHITE else 4)
        if mouseLoc.x == x and mouseLoc.y == y:
            modifier = 'Q'
        elif mouseLoc.x == x and mouseLoc.y == y-1:
            modifier = 'R'
        elif mouseLoc.x == x and mouseLoc.y == y-2:
            modifier = 'B'
        elif mouseLoc.x == x and mouseLoc.y == y-3:
            modifier = 'N'
        else:
            modifier = ''

        selectedLoc = None
        return board.move(board.getPromotingPawn(board.getActiveTeam()).loc, board.getPromotingPawn(board.getActiveTeam()).loc, modifier=modifier)

    if selectedLoc:

        return_value = board.move(selectedLoc, mouseLoc, modifier=('Q' if autoQueen else None))
        selectedLoc = None
        return return_value

    if board.getPiece(mouseLoc):
        selectedLoc = mouseLoc
        return 'highlighted'
    else:
        selectedLoc = None
        return 'unselected'

    return True

def draw_promote(screen, board):

    x = (board.getPromotingPawn(board.getActiveTeam()).x-1)
    y = (0 if board.getActiveTeam() is Team.WHITE else 4)
    pygame.draw.rect(screen, (230,230,230),
                     (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE*4), border_radius=SQUARE_SIZE//10)

    for i, piece in enumerate(['Q','R','B','N']):
        screen.blit(SPRITES[('w' if board.getActiveTeam() is Team.WHITE else 'b') + piece],
                (x * SQUARE_SIZE, (y+i) * SQUARE_SIZE))


if __name__ == "__main__":
    main()
