# import needed libraries
import random, time, pygame, sys
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480

# tetris box - 20 x 10 TILES
BOARDHEIGHT = 20
BOARDWIDTH = 10
BOXSIZE = 20 # can change
BLANK = '~' # represents blank spaces

SIDE_MARGIN = (WINDOWWIDTH - BOXSIZE * BOARDWIDTH) / 2
TOP_MARGIN = WINDOWHEIGHT - BOXSIZE * BOARDHEIGHT - 5

# COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (128,128,128)

AQUA = (0, 255,255)
BLUE = (0,0,255)
ORANGE = (255,120,0)
RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,150,0)
PURPLE = (128,0,128)

# PIECE COLORS
COLORS = {'I': AQUA, 'L':BLUE, 'J': ORANGE, 'Z': RED, 'O': YELLOW, 'S': GREEN, 'T': PURPLE}
BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY

# PIECE DESIGNS
TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

I_TEMPLATE= [['~~O~~',
              '~~O~~',
              '~~O~~',
              '~~O~~',
              '~~~~~'],
             ['~~~~~',
              '~~~~~',
              'OOOO~',
              '~~~~~',
              '~~~~~',]]

T_TEMPLATE = [['~~~~~',
               '~~O~~',
               '~OOO~',
               '~~~~~',
               '~~~~~'],
              ['~~~~~',
               '~~O~~',
               '~~OO~',
               '~~O~~',
               '~~~~~'],
              ['~~~~~',
               '~~~~~',
               '~OOO~',
               '~~O~~',
               '~~~~~'],
              ['~~~~~',
               '~~O~~',
               '~OO~~',
               '~~O~~',
               '~~~~~']]

Z_TEMPLATE= [['~~~~~',
              '~~~~~',
              '~OO~~',
              '~~OO~',
              '~~~~~'],
             ['~~~~~',
              '~~O~~',
              '~OO~~',
              '~O~~~',
              '~~~~~']]
S_TEMPLATE= [['~~~~~',
              '~~~~~',
              '~~OO~',
              '~OO~~',
              '~~~~~'],
             ['~~~~~',
              '~~O~~',
              '~~OO~',
              '~~~O~',
              '~~~~~']]
O_TEMPLATE = [['~~~~~',
              '~~~~~',
              '~OO~~',
              '~OO~~',
              '~~~~~']]
J_TEMPLATE= [['~~~~~',
              '~O~~~',
              '~OOO~',
              '~~~~~',
              '~~~~~'],
             ['~~~~~',
              '~~OO~',
              '~~O~~',
              '~~O~~',
              '~~~~~'],
             ['~~~~~',
              '~~~~~',
              '~OOO~',
              '~~~O~',
              '~~~~~'],
             ['~~~~~',
              '~~O~~',
              '~~O~~',
              '~OO~~',
              '~~~~~']]

L_TEMPLATE= [['~~~~~',
              '~~~O~',
              '~OOO~',
              '~~~~~',
              '~~~~~'],
             ['~~~~~',
              '~~O~~',
              '~~O~~',
              '~~OO~',
              '~~~~~'],
             ['~~~~~',
              '~~~~~',
              '~OOO~',
              '~O~~~',
              '~~~~~'],
             ['~~~~~',
              '~OO~~',
              '~~O~~',
              '~~O~~',
              '~~~~~']]

SHAPES = {'I': I_TEMPLATE,
          'T': T_TEMPLATE,
          'Z': Z_TEMPLATE,
          'S': S_TEMPLATE,
          'O': O_TEMPLATE,
          'J': J_TEMPLATE,
          'L': L_TEMPLATE
          }

# SPEED CONSTANTS
HORIZONTAL_SPEED = 0.15
VERTICAL_SPEED = 0.1

def main():
    global FPSCLOCK, DISPLAYSCREEN, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.SysFont('comicsansms', 18)
    BIGFONT = pygame.font.SysFont('comicsansms', 100)
    showTextScreen('Tetris')
    while True:
        pygame.mixer.music.load('gurennoyumiya.mp3') # play the tetris music
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1, 0.0)
        runGame()
        pygame.mixer.music.play() # game over music
        pygame.mixer.music.stop()
        showTextScreen('Game Over')

def runGame():
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    moveDown, moveLeft, moveRight = False, False, False
    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)

    currentPiece = getNewPiece()
    nextPiece = getNewPiece()

    while True:
        if currentPiece == None:
            currentPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time()

            if not isValidPosition(board, fallingPiece):
                return # aka game over

        checkForQuit()

        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_p or event.key == K_ESCAPE:
                    DISPLAYSCREEN.fill(BGCOLOR)
                    pygame.mixer.music.stop()
                    showTextScreen('Paused')
                    pygame.mixer.music.play(-1, 0.0)
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                    lastFallTime = time.time()

                elif (event.key == K_LEFT or event.key == K_a):
                    moveLeft = False
                elif (event.key == K_RIGHT or event.key == K_d):
                    moveRight = False
                elif (event.key == K_DOWN or event.key == K_s):
                    moveDown = False
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                    moveLeft = True
                    moveRight = False
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                    moveRight = True
                    moveLeft = False
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_DOWN or event.key == K_s):
                    moveDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()

                elif event.key == K_SPACE:
                    # instadrop
                    moveDown, moveLeft, moveRight = False, False, False
                    for i in range(1, BOARDHEIGHT):
                        if isValidPosition(board, fallingPiece, adjY=i):
                            continue
                        fallingPiece['y'] += i

                # rotating
                elif (event.key == K_UP or event.key == K_w):
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(SHAPES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(SHAPES[fallingPiece['shape']])

                elif (event.key == K_q or event.key == K_e):
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(SHAPES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(SHAPES[fallingPiece['shape']])


            if (moveLeft or moveRight) and time.time() - lastMoveSidewaysTime > HORIZONTAL_SPEED:
                if movingLeft and isValidPosition(board, fallingPiece, adjX = -1):
                    fallingPiece['x'] -= 1
                elif movingRight and isValidPosition(board, fallingPiece, adjX = 1):
                    fallingPiece['x'] += 1
                lastMoveSidewaysTime = time.time()

            if moveDown and time.time() - lastFallTime > VERTICAL_SPEED and isValidPosition(board, fallingPiece, adjY = 1):
                fallingPiece['y'] += 1
                lastMoveDownTime = time.time()

            if time.time() - lastFallTime > fallFreq:
                if not isValidPosition(board, fallingPiece, adjY = 1):
                    addToBoard(board, fallingPiece)
                    score += removeCompleteLines(board)
                    level, fallFreq = calculateLevelAndFallFreq(score)
                    fallingPiece = None
                else:
                    fallingPiece['y'] += 1
                    lastFallTime = time.time()

            DISPLAYSCREEN.fill(BGCOLOR)
            drawBoard(board)
            drawStatus(score, level)
            drawNextPiece(nextPiece)
            if fallingPiece != None:
                drawPiece(fallingPiece)

            pygame.display.update()
            FPSCLOCK.tick(FPS)

def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

def terminate():
    pygame.quit()
    sys.exit()

def checkForKeyPress():
    checkForQuit()
    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None

def showTextScreen(text):
    titleScreen, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSCREEN.blit(titleScreen, titleRect)

    titleScreen, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2)-3, int(WINDOWHEIGHT / 2)-3)
    DISPLAYSCREEN.blit(titleScreen, titleRect)

    pressKeyScreen, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 150)
    DISPLAYSCREEN.blit(pressKeyScreen, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_RETURN:
            terminate()
        pygame.event.post(event)

def calculateLevelAndFallFreq(score):
    level = int(score / 10) + 1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq

def getNewPiece():
    shape = random.choice(list(SHAPES.keys()))
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(SHAPES[shape]) - 1),
                'x': int(BOARDWIDTH/2) - int(TEMPLATEWIDTH/2),
                'y': -2,
                'color': COLORS[shape]}
    return newPiece

def addToBoard(board, piece):
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if SHAPES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y+piece['y']] = piece['color']

def getBlankBoard():
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board

def isOnBoard(x,y):
    return x>= 0 and x < BOARDWIDTH and y < BOARDHEIGHT

def isValidPosition(board, piece, adjX=0, adjY=0):
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or SHAPES[piece['shape']][piece['rotation']][y][x] == BLANK: # is valid
                continue
            if not isOnBoard(x+piece['x']+adjX, y+piece['y']+adjY): # off the board
                return False
            if board[x+piece['x']+adjX][y+piece['y']+adjY] != BLANK: # occupied space
                return False
    return True

def isCompleteLine(board, y):
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True

def removeCompleteLines(board):
    numLinesRemoved = 0
    y = BOARDHEIGHT - 1
    while y >= 0:
        if isCompleteLine(board, y):
            for line in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][line] = board[x][line-1]
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
        else:
            y -= 1
    return numLinesRemoved

def convertToPixelCoords(box_x, box_y):
    return (SIDE_MARGIN + (box_x * BOXSIZE)), (TOP_MARGIN + (box_y * BOXSIZE))

def drawBox(xbox, ybox, color, pixelx=None, pixely=None):
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(xbox, ybox)
    pygame.draw.rect(DISPLAYSCREEN, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))

def drawBoard(board):
    pygame.draw.rect(DISPLAYSCREEN, BORDERCOLOR, (SIDE_MARGIN - 3, TOP_MARGIN - 7, (BOARDWIDTH*BOXSIZE) + 8, (BOARDHEIGHT*BOXSIZE)+8), 5)
    pygame.draw.rect(DISPLAYSCREEN, BGCOLOR, (SIDE_MARGIN, TOP_MARGIN, (BOARDWIDTH * BOXSIZE), (BOARDHEIGHT * BOXSIZE)))
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x,y, board[x][y])

def drawStatus(score, level):
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSCREEN.blit(scoreSurf, scoreRect)

    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH-150, 50)
    DISPLAYSCREEN.blit(levelSurf, levelRect)

def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = SHAPES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

def drawNextPiece(piece):
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 80)
    DISPLAYSCREEN.blit(nextSurf, nextRect)
    drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=100)

if __name__ == '__main__':
    main()



















