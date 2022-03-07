import os
import io
import random
import sys
"""
     TODO 
     1. Fix Promotion. Check.
     2. Add window sound. Check.
     3. Add animations. No need.
     4. Multiple piece styles. No need.
     5. Add info bar + flip button + resign, restart, draw
     6. end screen
     7. Add smarter, yet deterministic agent.
     8. Go full RL.
"""
import pygame
from Board import Board
from Piece import Piece, PieceType, Team
from Location import Location
from Agent import RandomAgent, StockfishAgent
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

# Set up the drawing window
BOARD_SIZE = 704
MENU_BAR_SIZE = (BOARD_SIZE // 16)
MENU_SIZE = (BOARD_SIZE // 3)
is_menu_open = False
SQUARE_SIZE = (BOARD_SIZE // 8)
WHITE = (233, 211, 176)
BLACK = (180, 136, 99)
GRAY = (61, 58, 55)
LIGHT_GRAY = (159,156,153,102)
GREEN = (45, 138, 44, 150)
PURPLE = (164, 164, 205)
YELLOW = (247,235,118,150)
rows = ['a','b','c','d','e','f','g','h']
SPRITES = {}
TEXTS = {}
BUTTON_OFFSETS = {}
BUTTONS = {}
SOUNDS = {}
selectedLoc = None
pieceStyle = 'frugale'
autoQueen = False
animating = []  #hold tuples of (piece, startLoc, endLoc)
set_orientation = 'random'
orientation = None
starting_orientation = None
players = ['stockfish','manual'] # [top, bottom]
agent_delay = (0.5,2)  # around 1 second for AI to respond
audio = True
stockfish_params = {
    'depth' : 18,
    'elo' : 2000,
    'thinking_time' : 400,
}


def main():
    global BOARD_SIZE
    global SQUARE_SIZE
    global SOUNDS

    # initialize window
    pygame.init()
    pygame.display.set_caption('Chess() by Nihal')
    pygame.display.set_icon(pygame.image.load(os.path.join('resources','icon.png')))

    # choose board orientation
    reset_orientation()

    # create screen and clock
    screen = screen_init()  # creates screen and also sprites
    clock = pygame.time.Clock()

    # create board object
    board = Board()

    # create agent arrays
    agents = {'random' : RandomAgent(board),
              'stockfish' : StockfishAgent(board, **stockfish_params)}

    # import sounds
    SOUNDS['move'] = pygame.mixer.Sound(os.path.join('resources','sounds', 'move-self.wav'))
    SOUNDS['take'] = pygame.mixer.Sound(os.path.join('resources','sounds', 'capture.wav'))
    SOUNDS['castle'] = pygame.mixer.Sound(os.path.join('resources','sounds', 'castle.wav'))
    SOUNDS['check'] = pygame.mixer.Sound(os.path.join('resources','sounds', 'move-check.wav'))
    SOUNDS['game_over'] = pygame.mixer.Sound(os.path.join('resources','sounds', 'game-end.wav'))


    # Run until the user asks to quit
    running = True
    visualDelta = True
    move_return = None
    since_move = 0
    delay = 0
    move = None

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
                if event.button == 1:
                    move_return = click(event, board, screen, move_return)
                    visualDelta = bool(move_return)

        # do agent
        if getMovingAgent(board) in agents.keys():
            if not board.gameOver:

                if not move and since_move:
                    move = agents[getMovingAgent(board)].getMove()

                since_move += dt
                if not delay:
                    delay = random.uniform(agent_delay[0], agent_delay[1]) * 1000

                if since_move > delay:
                    if move:
                        move_return = board.move(move)
                        visualDelta = True
                        since_move = 0
                        delay = 0
                        move = None

        if visualDelta:
            render(screen, board, move_return)
            visualDelta = False


    # Done! Time to quit.
    pygame.quit()

def render(screen, board, move_return):
    # Fill the background with white
    screen.fill(GRAY)

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

    # draw menu
    draw_menu(screen, board)

    #play sound
    if audio:
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

def draw_menu(screen, board):

    if is_menu_open:
        pass
    else:
        for key in BUTTON_OFFSETS:
            screen.blit(TEXTS[key], BUTTON_OFFSETS[key])

def sprite_gen():
    global SPRITES

    SPRITES = {}

    for s in ['wK', 'wQ', 'wR', 'wB', 'wN', 'wP', 'bK', 'bQ', 'bR', 'bB', 'bN', 'bP']:
        path = os.path.join('resources','piece_sprites',pieceStyle, f'{s}.')
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
    global BUTTON_OFFSETS
    global BUTTONS

    # import font
    font = pygame.font.Font(os.path.join('resources','fonts', 'Segoe UI.ttf'), SQUARE_SIZE//5)
    icons = pygame.font.Font(os.path.join('resources','fonts', 'chessglyph.ttf'), round(SQUARE_SIZE/1.7))

    for i, file in enumerate(rows):
        TEXTS[file] = font.render(file, True, WHITE if i % 2 == orientation.value else BLACK)
    for i in range(1,9):
        TEXTS[str(i)] = font.render(str(i), True, BLACK if i%2==0 else WHITE)

    TEXTS['settings'] = icons.render('·', True, LIGHT_GRAY)
    TEXTS['flip'] = icons.render('f', True, LIGHT_GRAY)
    TEXTS['resign'] = icons.render('Y', True, LIGHT_GRAY)
    TEXTS['reset'] = icons.render('L', True, LIGHT_GRAY)
    TEXTS['right_arrow'] = icons.render('…', True, LIGHT_GRAY)
    TEXTS['draw'] = pygame.transform.smoothscale(icons.render('+', True, LIGHT_GRAY),TEXTS['right_arrow'].get_size())

    # recompute button offsets
    BUTTON_OFFSETS = {
        'settings': (BOARD_SIZE + round(SQUARE_SIZE / 13), -round(SQUARE_SIZE / 10)),
        'flip': (BOARD_SIZE + round(SQUARE_SIZE / 14), round(SQUARE_SIZE / 2.5)),
        'right_arrow': (BOARD_SIZE + round(SQUARE_SIZE / 10), round(SQUARE_SIZE * 3.575)),
        'draw': (BOARD_SIZE + round(SQUARE_SIZE / 13), round(SQUARE_SIZE * 6.25)),
        'resign': (BOARD_SIZE + round(SQUARE_SIZE / 14), round(SQUARE_SIZE * 6.8)),
        'reset': (BOARD_SIZE + round(SQUARE_SIZE / 14), round(SQUARE_SIZE * 7.3)),
    }

    if not os.name == 'nt':
        for key, item in BUTTON_OFFSETS.items():
            BUTTON_OFFSETS[key] = (item[0],item[1]+round(SQUARE_SIZE / 10))

    # store rect of button locations
    for key in BUTTON_OFFSETS:
        BUTTONS[key] = TEXTS[key].get_bounding_rect().move(BUTTON_OFFSETS[key])



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
    global MENU_BAR_SIZE
    global MENU_SIZE

    # discrete board size to avoid white borders
    if BOARD_SIZE % 8 != 0:
        BOARD_SIZE -= BOARD_SIZE % 8
        SQUARE_SIZE = (BOARD_SIZE // 8)
        MENU_BAR_SIZE = (BOARD_SIZE // 16)
        MENU_SIZE = (BOARD_SIZE // 3)

    #init screen
    #if s == 'fullscreen':
     #   screen = pygame.display.set_mode([BOARD_SIZE, BOARD_SIZE], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.FULLSCREEN)
    #else:
    screen = pygame.display.set_mode([BOARD_SIZE+(MENU_SIZE if is_menu_open else MENU_BAR_SIZE), BOARD_SIZE], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

    # load piece sprites
    sprite_gen()

    # font gen
    font_gen()

    return screen

def click(event, board, screen, move_return):

    if event.pos[0] < BOARD_SIZE:
        return board_click(event, board, screen, move_return)
    else:
        return menu_click(event, board, screen, move_return)

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

def menu_click(event, board, screen, move_return):

    if BUTTONS['flip'].collidepoint(event.pos):
        flipBoard()
        return True
    if BUTTONS['reset'].collidepoint(event.pos):
        reset(board)
        return True
    if BUTTONS['resign'].collidepoint(event.pos):
        if getMovingAgent(board) == 'manual':
            board.move('resign')
            return True
    if BUTTONS['draw'].collidepoint(event.pos):
        if getMovingAgent(board) == 'manual':
            board.move('draw')
            return True
    if BUTTONS['settings'].collidepoint(event.pos):
        reset(board)
        return True
    if BUTTONS['right_arrow'].collidepoint(event.pos) and board.gameOver:
        pass


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
    return players[(board.getActiveTeam().value + starting_orientation.value+1) % 2]

def flipBoard():
    global orientation

    orientation = orientation.opponent()
    font_gen()

def reset_orientation():
    global orientation
    global starting_orientation

    if set_orientation == 'random':
        starting_orientation = Team(random.randint(0,1))
        orientation = starting_orientation
    elif set_orientation.lower() == 'white':
        starting_orientation = Team(0)
        orientation = Team(0)
    elif set_orientation.lower() == 'black':
        starting_orientation = Team(1)
        orientation = Team(1)

def reset(board):
    board.reset()
    reset_orientation()

if __name__ == "__main__":
    main()
