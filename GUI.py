import os
import io
import random
"""
     TODO 
     1. Fix Promotion. Check.
     2. Add window sound. Check.
     3. Add animations
     4. Add info bar + flip button + resign, restart, draw
     5. end screen
     5. Multiple piece styles. On Hold.
"""
import pygame
from Board import Board
from Piece import Piece, PieceType, Team
from Location import Location
from Agent import RandomAgent

# Set up the drawing window
BOARD_SIZE = 704
SQUARE_SIZE = (BOARD_SIZE // 8)
WHITE = (233, 211, 176)
BLACK = (180, 136, 99)
GRAY = (127,159,159)
GREEN = (45, 138, 44, 150)
PURPLE = (164, 164, 205)
YELLOW = (247,235,118, 150)
rows = ['a','b','c','d','e','f','g','h']
SPRITES = {}
TEXTS = {}
SOUNDS = {}
selectedLoc = None
pieceStyle = 'frugale'
autoQueen = False
animating = []  #hold tuples of (piece, startLoc, endLoc)
orientation = None
players = ['random','manual'] # [top, bottom]
agent_delay = (0.5,2)  # around 1 second for AI to respond


def main():
    global BOARD_SIZE
    global SQUARE_SIZE
    global orientation
    global SOUNDS

    # initialize window
    pygame.init()
    pygame.display.set_caption('Chess() by Nihal')
    pygame.display.set_icon(pygame.image.load('icon.png'))

    # choose board orientation
    orientation = Team(random.randint(0,1))

    # create screen and clock
    screen = screen_init() # creates screen and also sprites
    clock = pygame.time.Clock()

    # create board object
    board = Board()

    #William the random agent
    william = RandomAgent(board)

    # import sounds
    SOUNDS['move'] = pygame.mixer.Sound(os.path.join('sounds', 'move-self.wav'))
    SOUNDS['take'] = pygame.mixer.Sound(os.path.join('sounds', 'capture.wav'))
    SOUNDS['castle'] = pygame.mixer.Sound(os.path.join('sounds', 'castle.wav'))
    SOUNDS['check'] = pygame.mixer.Sound(os.path.join('sounds', 'move-check.wav'))
    SOUNDS['game_over'] = pygame.mixer.Sound(os.path.join('sounds', 'game-end.wav'))


    # Run until the user asks to quit
    running = True
    visualDelta = True
    move_return = None
    since_move=0
    delay = 0

    while running:

        #if not animating:
        dt = clock.tick(60)

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

        # do random agent

        if getMovingAgent(board) == 'random':
            if not board.gameOver:
                since_move += dt
                if not delay:
                    delay = random.uniform(agent_delay[0], agent_delay[1]) * 1000

                if since_move > delay:
                    move = william.getMove()
                    if move:
                        move_return = board.move(move)
                        visualDelta = True
                        since_move = 0
                        delay = 0

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
            pygame.draw.rect(screen, BLACK if (i + j) % 2 == (orientation.value+1)%2 else WHITE,
                                  (i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # draw notations
    for i, rank in enumerate(['a','b','c','d','e','f','g','h']):
        screen.blit(TEXTS[rank], ((i+1)*SQUARE_SIZE-round(SQUARE_SIZE/7), 7*SQUARE_SIZE+round(SQUARE_SIZE*11/15)))
    for i in range(1,9):
        screen.blit(TEXTS[str(i)], (round(SQUARE_SIZE/15), (8-i if orientation is Team.WHITE else i-1) * SQUARE_SIZE))


    # draw past move highlight
    if board.moveLog:
        fromLoc, toLoc, _ = board.convertSAN(board.moveLog[-1])
        screen.blit(SPRITES['pH'], translateLoc(fromLoc))
        screen.blit(SPRITES['pH'], translateLoc(toLoc))

    # draw selected highlight
    if selectedLoc:
        screen.blit(SPRITES['sH'], translateLoc(selectedLoc))
        if board.getPiece(selectedLoc).color is board.getActiveTeam():
            for _, toLoc, _ in board.getPiece(selectedLoc).getLegalMoves(mode='loc'):
                if board.getPiece(toLoc):
                    screen.blit(SPRITES['tH'], translateLoc(toLoc))
                else:
                    screen.blit(SPRITES['cH'], translateLoc(toLoc))

    # draw pieces
    for piece in board.getPieces('both'):
        screen.blit(SPRITES[('w' if piece.color == Team.WHITE else 'b') + piece.type.toString()], translateLoc(piece))

    # draw promoting menu
    if move_return == 'need_promote':
        draw_promote(screen, board)

    #play sound
    if move_return in ['moved', 'promoted']:
        pygame.mixer.Sound.play(SOUNDS['move'])
    elif move_return == 'captured':
        pygame.mixer.Sound.play(SOUNDS['take'])
    elif move_return == 'castled':
        pygame.mixer.Sound.play(SOUNDS['castle'])
    elif move_return == 'checked':
        pygame.mixer.Sound.play(SOUNDS['check'])
    elif move_return in ['1-0', '0-1', '0.5-0.5']:
        pygame.mixer.Sound.play(SOUNDS['game_over'])

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

def font_gen():
    global TEXTS

    # import font
    font = pygame.font.Font(os.path.join('fonts', 'Segoe UI.ttf'), SQUARE_SIZE//5)

    for i, file in enumerate(rows):
        TEXTS[file] = font.render(file, True, WHITE if i % 2 == orientation.value else BLACK)
    for i in range(1,9):
        TEXTS[str(i)] = font.render(str(i), True, BLACK if i%2==0 else WHITE)


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

    # font gen
    font_gen()

    return screen

def click(event, board, screen, move_return):

    if event.pos[0] < BOARD_SIZE:
        return board_click(event, board, screen, move_return)

def board_click(event, board, screen, move_return):
    global selectedLoc

    if orientation is Team.WHITE:
        mouseLoc = Location(event.pos[0]//SQUARE_SIZE+1, 8-event.pos[1]//SQUARE_SIZE)
    else:
        mouseLoc = Location(event.pos[0]//SQUARE_SIZE+1, event.pos[1]//SQUARE_SIZE+1)

    if getMovingAgent(board) == 'manual':
        if move_return == 'need_promote':
            x = (board.getPromotingPawn(board.getActiveTeam()).x)

            if mouseLoc.x == x and mouseLoc.y in [1,8]:
                modifier = 'Q'
            elif mouseLoc.x == x and mouseLoc.y in [2,7]:
                modifier = 'R'
            elif mouseLoc.x == x and mouseLoc.y in [3,6]:
                modifier = 'B'
            elif mouseLoc.x == x and mouseLoc.y in [4,5]:
                modifier = 'N'
            else:
                modifier = ''

            selectedLoc = None
            return board.move(board.getPromotingPawn(board.getActiveTeam()).loc, board.getPromotingPawn(board.getActiveTeam()).loc, modifier=modifier)

    if selectedLoc:

        if getMovingAgent(board) == 'manual':
            return_value = board.move(selectedLoc, mouseLoc, modifier=('Q' if autoQueen else None))
            selectedLoc = None
            return return_value
        else:
            selectedLoc = None

    if board.getPiece(mouseLoc):
        selectedLoc = mouseLoc
        return 'highlighted'
    else:
        selectedLoc = None
        return 'unselected'

    return True

def draw_promote(screen, board):

    mask = pygame.Surface((BOARD_SIZE, BOARD_SIZE), pygame.SRCALPHA)
    mask.fill((0,0,0,150))

    screen.blit(mask, (0,0))

    x = (board.getPromotingPawn(board.getActiveTeam()).x-1)
    y = (0 if board.getActiveTeam() is orientation else 4)

    for i in range(4):
        pygame.draw.rect(screen, PURPLE,
                     (x * SQUARE_SIZE, (y+i) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), border_radius=SQUARE_SIZE//4)

    for i, piece in enumerate(['Q','R','B','N']):
        screen.blit(SPRITES[('w' if board.getActiveTeam() is Team.WHITE else 'b') + piece],
                (x * SQUARE_SIZE, (i if board.getActiveTeam() is orientation else 7-i) * SQUARE_SIZE))

def translateLoc(loc, y=None):
    if y:
        if orientation is Team.WHITE:
            return ((loc - 1) * SQUARE_SIZE, (8 - y) * SQUARE_SIZE)
        else:
            return ((loc - 1) * SQUARE_SIZE, (y - 1) * SQUARE_SIZE)
    if orientation is Team.WHITE:
        return ((loc.x - 1) * SQUARE_SIZE, (8 - loc.y) * SQUARE_SIZE)
    else:
        return ((loc.x - 1) * SQUARE_SIZE, (loc.y-1) * SQUARE_SIZE)

def getMovingAgent(board):
    return players[(board.getActiveTeam().value + orientation.value+1) % 2]

if __name__ == "__main__":
    main()
