import pygame
import pygame_gui
import sys
import math

#pygame initialization

ROWS = 8
COLUMNS = 8

settings = {
    "size": (600,400),
    "fps": 60}

TILESIZE = 100

WIDTH = COLUMNS * TILESIZE
HEIGHT = ROWS * TILESIZE
SIZE = (WIDTH, HEIGHT)

# colours
BOARD_BLACK = (31, 20, 2)
BOARD_WHITE = (245, 241, 232)
PIECE_BLACK = (76, 69, 56)
PIECE_WHITE = (216, 190, 147)
SELECTED = (40, 194, 96)

INSTRUCTIONS = "<strong>How to play</strong><br>" \
               "A piece can be moved forwards, backwards or sideways in an unobstructed line. <br>" \
               "To beat an enemy piece, it has to be encircled from two sides in a straight line. <br>" \
               "Whoever beats more pieces or blocks all enemy pieces wins." \
               " <br>" \
               " <br>" \
               "<br><strong>About the image: </strong><br>" \
               "Amazonomachy<br>" \
               "Roman mosaic emblema (marble and limestone), 2nd half of the 4th century AD. <br>" \
               "Picture © Marie-Lan Nguyen / Wikimedia Commons"


pygame.init()
pygame.display.set_caption("Ludus latrunculorum")

# Classes for the game board

class Board(object):
    '''
    Parent for the game board. Consists of 8x8 fields
    '''
    def __init__(self):
        self.xAxis = ("A", "B", "C", "D", "E", "F", "G", "H")
        self.yAxis = (1, 2, 3, 4, 5, 6, 7, 8)

    def getCoord(self):
        coordinates = [self.xAxis, self.yAxis]
        return coordinates

    def getX(self):
        return self.xAxis

    def getY(self):
        return self.yAxis

    def provideLoc(self, i, j):
        location = [Board.getX(self)[i], Board.getY(self)[j]]
        return location

    def occupiedFields(self, whitePieces, blackPieces):
        occupancies = []
        for i in whitePieces:
            occupancies.append(Piece.getPieceLoc(i))
        for i in blackPieces:
            occupancies.append(Piece.getPieceLoc(i))
        return occupancies

    def __str__(self):
        return "{}, {}".format(self.xAxis, self.yAxis)


class Piece(object):
    '''
    parent class for game pieces

    location -> current location on the board
    '''
    def __init__(self, location):
        self.location = location

    def getPieceLoc(self):
        return self.location

    def getPieceAtLoc(self, location):
        if location[0] == self.location[0] and location[1] == self.location[1]:
            return self

    def __str__(self):
        return "Piece at " + str(self.location)

    def currentLocations(self):
        pieceLocs = []
        for j in self:
            pieceLocs.append(j.getPieceLoc())
        return pieceLocs

    def remove(self, element):
        self.remove(element)
        return self

# movements
    def isValid(self, aBoard, targetLoc, whitePieces, blackPieces):
        # function to check movement validity, returns True or False
        # if check passed, movement can be executed (realized in movement function)
        occupancies = Board.occupiedFields(aBoard, whitePieces, blackPieces)
        path = []
        x = self.getPieceLoc()[0]
        xaxis = Board.getX(aBoard)
        xindex = xaxis.index(x)

        if self.getPieceLoc()[0] == targetLoc[0]:
            #print("check path for X coord...")
            if self.getPieceLoc()[1] < targetLoc[1]:
                for i in range(self.getPieceLoc()[1], targetLoc[1]):
                    path.append(Board.provideLoc(aBoard, xindex, i))
            else:
                for i in range(targetLoc[1]-1, self.getPieceLoc()[1]-1):
                    path.append(Board.provideLoc(aBoard, xindex, i))

            if any(elem in path for elem in occupancies):
                return False
            else:
                return True

        elif self.getPieceLoc()[1] == targetLoc[1]:
            #print("check path for Y coord...")
            a = Board.getX(aBoard).index(self.getPieceLoc()[0])
            b = Board.getX(aBoard).index(targetLoc[0])
            if a < b:
                for i in range(a+1, b+1):
                    path.append(Board.provideLoc(aBoard, i, (self.getPieceLoc()[1]-1)))
            else:
                for i in range(b, a):
                    path.append(Board.provideLoc(aBoard, i, (self.getPieceLoc()[1]-1)))

            if any(elem in path for elem in occupancies):
                return False
            else:
                return True
        else:
            return False


    def move(self, aBoard, targetLoc, whitePieces, blackPieces):
        '''

        :param self: the piece
        :param targetLoc: List, [0] = A-H, [1] = 0-8
        :return: changes the location attribute of the piece instance to targetLoc, if validity test is passed
        '''
        prevLoc = self.getPieceLoc()
        if self.isValid(aBoard, targetLoc, whitePieces, blackPieces):
            self.location = targetLoc
            #print("Moved piece from {} to {}".format(prevLoc, self.location))
            return True
        else:
            #print("invalid movement")
            return False

    def getNeighbors(self, aBoard):
        neighbors = []
        x = self.getPieceLoc()[0]
        xaxis = Board.getX(aBoard)
        xindex = xaxis.index(x)
        try:
            if xindex == 0:
                neighbors.append(Board.provideLoc(aBoard, xindex + 1, (self.getPieceLoc()[1] - 1)))
                neighbors.append([x, self.getPieceLoc()[1] - 1])
                neighbors.append([x, self.getPieceLoc()[1] + 1])
            elif xindex == 7:
                neighbors.append(Board.provideLoc(aBoard, xindex - 1, (self.getPieceLoc()[1] - 1)))
                neighbors.append([x, self.getPieceLoc()[1] - 1])
                neighbors.append([x, self.getPieceLoc()[1] + 1])
            else:
                neighbors.append(Board.provideLoc(aBoard, xindex - 1, (self.getPieceLoc()[1] - 1)))
                neighbors.append(Board.provideLoc(aBoard, xindex + 1, (self.getPieceLoc()[1] - 1)))
                neighbors.append([x, self.getPieceLoc()[1] - 1])
                neighbors.append([x, self.getPieceLoc()[1] + 1])
        except IndexError:
            pass
        for i in neighbors:
            if i[1] == 0 or i[1] == 9:
                neighbors.remove(i)
        #print(neighbors)
        return neighbors

# serve beatings

    def checkIfBeaten(self, aBoard, other):
        '''
        ("A", "B", "C", "D", "E", "F", "G", "H")
        :param aBoard: Board is needed to provide X-Coordinates
        :param other: The other colour, to compare against to
        :return: True if beaten
        '''

        x = self.getPieceLoc()[0]
        y = self.getPieceLoc()[1]
        try:
            if [x, y+1] in Piece.currentLocations(other) and [x, y-1] in Piece.currentLocations(other):
                #print("{} might be beaten (up down)".format(self))
                return True
        except IndexError:
            pass
        xaxis = Board.getX(aBoard)
        xindex = xaxis.index(x)
        try:
            if xindex == 0 or xindex == 7:
                return False
            elif [xaxis[xindex+1], y] in Piece.currentLocations(other) and [xaxis[xindex-1], y] in Piece.currentLocations(other):
                #print("{} might be beaten (left right)".format(self))
                return True
        except IndexError:
            return False


    def removeBeatenPieces(self, aBoard, other):
        '''
        :param aBoard: needed for check function (see above)
        :param other: needed for check function (see above)
        :return: nothing, just removes a piece
        '''
        for piece in self:
            if Piece.checkIfBeaten(piece, aBoard, other):
                text = "{} is beaten<br>".format(piece)
                self.remove(piece)
                return text


class WhitePiece(Piece):
    '''
    class for white games pieces
    '''

    def __init__(self, location, ID):
        Piece.__init__(self, location)
        self.ID = ID

    def getPieceID(self):
        return self.ID

    def __str__(self):
        return "White Piece, ID " + str(self.ID) + " at " + str(self.location)

    def __repr__(self):
        return "White Piece, ID " + str(self.ID) + " at " + str(self.location)

class BlackPiece(Piece):
    '''
    class for black game pieces
    '''

    def __init__(self, location, ID):
        Piece.__init__(self, location)
        self.ID = ID

    def getPieceID(self):
        return self.ID

    def __str__(self):
        return "Black Piece, ID " + str(self.ID) + " at " + str(self.location)

    def __repr__(self):
        return "Black Piece, ID " + str(self.ID) + " at " + str(self.location)


# general set up functions

class Game(object):

    def __init__(self, n):
        self.n = n
        self.board = Board()
        self.turn = 1
        self.whitePieces = []
        self.blackPieces = []
        self.distributePieces()
        self.gameOver = False

    def getTurn(self):
        return self.turn

    def incrementTurn(self):
        self.turn += 1

    def getBoard(self):
        return self.board

    def setWhitePieces(self, whitePieces):
        self.whitePieces = whitePieces

    def setBlackPieces(self, blackPieces):
        self.blackPieces = blackPieces

    def getWhitePieces(self):
        return self.whitePieces

    def getBlackPieces(self):
        return self.blackPieces


    def distributePieces(self):
        '''
        initial placement of number of n game pieces for each player
        :param n - > int
        :param aBoard - > Board object
        :return: lists with the piece objects that fight it out on the board
        '''
        all_white_pieces = []
        all_black_pieces = []
        count = 0
        j = 0
        for x in range(self.n//2):
            all_white_pieces.append(WhitePiece(Board.provideLoc(self.getBoard(), j, 0), count))
            all_black_pieces.append(BlackPiece(Board.provideLoc(self.getBoard(), j, 7), count))
            count += 1
            j += 1
        j = 0
        for x in range(self.n//2, self.n):
            all_white_pieces.append(WhitePiece(Board.provideLoc(self.getBoard(), j, 1), count))
            all_black_pieces.append(BlackPiece(Board.provideLoc(self.getBoard(), j, 6), count))
            count += 1
            j += 1
        self.setBlackPieces(all_black_pieces)
        self.setWhitePieces(all_white_pieces)

    def whitePieceLocs(self):
        locations = []
        for piece in self.getWhitePieces():
            locations.append(piece.getPieceLoc())
        return locations

    def blackPieceLocs(self):
        locations = []
        for piece in self.getBlackPieces():
            locations.append(piece.getPieceLoc())
        return locations

    def checkEncirclement(self):
        if len(self.getWhitePieces()) < 6 or len(self.getBlackPieces()) < 6:
            if self.getTurn() % 2 != 1:
                total = 0
                for piece in self.getWhitePieces():
                    if all(x in self.getBoard().occupiedFields(self.getWhitePieces(), self.getBlackPieces()) for x in piece.getNeighbors(self.getBoard())):
                        total += 1
                if total == len(self.getWhitePieces()):
                    print("ALL WHITE PIECES ARE BLOCKED")
                    return True
            else:
                total = 0
                for piece in self.getBlackPieces():
                    if all(x in self.getBoard().occupiedFields(self.getWhitePieces(), self.getBlackPieces()) for x in piece.getNeighbors(self.getBoard())):
                        total += 1
                if total == len(self.getBlackPieces()):
                    print("ALL BLACK PIECES ARE BLOCKED")
                    return True

    def checkForGameOver(self):
        # TODO check also for tie
        if self.getBlackPieces() == []:
            print("WHITE WON")
            self.gameOver = True
        elif self.getWhitePieces() == []:
            print("BLACK WON")
            self.gameOver = True
        elif self.checkEncirclement():
            self.gameOver = True


#state functions

class States(object):
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None

class Menu(States):
    def __init__(self):
        States.__init__(self)
        self.next = "game"
        self.bg = pygame.image.load("bg.png")
        self.buttons = {}
        self.generateScreen()
        self.createElements()
        self.font = pygame.font.SysFont('Arial', 18)
        self.licence = self.font.render("v0.1.0", True, (250,0,0))

    def cleanup(self):
        print("cleaning up Menu state")
    def startup(self):
        print("starting Menu state")
        self.generateScreen()
        self.createElements()

    def generateScreen(self):
        self.screen = pygame.display.set_mode(SIZE)
        self.manager = pygame_gui.UIManager(SIZE)

    def get_event(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.buttons["start"]:
                    self.done = True
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.buttons["quit"]:
                    pygame.quit()
                    sys.exit()
        self.manager.process_events(event)

    def update(self, screen, dt):
        self.draw(screen, dt)

    def draw(self, screen, dt):
        screen.blit(self.bg, (0, 0))
        screen.blit(self.licence, (750,780))
        self.manager.update(dt)
        self.manager.draw_ui(screen)
        pygame.display.update()

    def createElements(self):
        start = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                             text='Start Game',
                                             manager=self.manager)
        self.buttons["start"] = start
        quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 325), (100, 50)),
                                             text='Quit Game',
                                             manager=self.manager)
        self.buttons["quit"] = quit
        instructions = pygame_gui.elements.ui_text_box.UITextBox(INSTRUCTIONS,
                                                                 relative_rect=pygame.Rect((150, 450), (500, 300)),
                                                                 manager=self.manager)
        self.buttons["instructions"] = instructions


class GameState(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'menu'
        self.buttons = {}
        self.log_string = "TURN NUMBER 1: WHITE <br>WELCOME"
        self.dt = app.getDT()

    def cleanup(self):
        print('cleaning up Game state stuff')
        self.log_string = "TURN NUMBER 1: WHITE <br>WELCOME"

    def startup(self):
        print('starting Game state stuff')
        self.session = Game(16)
        self.generateScreen()
        self.createElements()

    def generateScreen(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT + 150))
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT + 150))

    def get_event(self, event):
        if event.type == pygame.K_ESCAPE:
            self.done = True
        if self.session.gameOver:
            self.done = True
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.buttons["quit"]:
                    self.done = True
        self.manager.process_events(event)
        self.gameTurn(event)

    def update(self, screen, dt):
        self.draw(screen)
        self.manager.update(dt)
        self.manager.draw_ui(screen)

    def draw(self, screen):
        self.drawBoard(self.session.getBoard(), screen)
        self.drawPieces(self.session, screen)
        self.manager.draw_ui(screen)

    def createElements(self):
        quit_to_menu = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((660, 850), (125, 50)),
                                                    text='Quit to menu',
                                                    manager=self.manager)
        self.buttons["quit"] = quit_to_menu
        log = pygame_gui.elements.ui_text_box.UITextBox(self.log_string,
                                                        relative_rect=pygame.Rect((0, 800), (650, 150)),
                                                        manager=self.manager)
        self.buttons["log"] = log


    def drawBoard(self, board, screen):
        for i in range(len(board.getX())):
            for j in range(len(board.getY())):
                if i % 2 == 0 and j % 2 != 0:
                    pygame.draw.rect(screen, BOARD_BLACK, (i * TILESIZE, j * TILESIZE, TILESIZE, TILESIZE))
                elif i % 2 != 0 and j % 2 == 0:
                    pygame.draw.rect(screen, BOARD_BLACK, (i * TILESIZE, j * TILESIZE, TILESIZE, TILESIZE))
                else:
                    pygame.draw.rect(screen, BOARD_WHITE, (i * TILESIZE, j * TILESIZE, TILESIZE, TILESIZE))

    def convertedLoc(self, location):
        xMappings = {"A": int((WIDTH - TILESIZE * 7) - (TILESIZE / 2)),
                     "B": int((WIDTH - TILESIZE * 6) - (TILESIZE / 2)),
                     "C": int((WIDTH - TILESIZE * 5) - (TILESIZE / 2)),
                     "D": int((WIDTH - TILESIZE * 4) - (TILESIZE / 2)),
                     "E": int((WIDTH - TILESIZE * 3) - (TILESIZE / 2)),
                     "F": int((WIDTH - TILESIZE * 2) - (TILESIZE / 2)),
                     "G": int((WIDTH - TILESIZE) - (TILESIZE / 2)),
                     "H": int((WIDTH - TILESIZE / 2))}
        yMappings = {1: int((WIDTH - TILESIZE / 2)),
                     2: int((WIDTH - TILESIZE) - (TILESIZE / 2)),
                     3: int((WIDTH - TILESIZE * 2) - (TILESIZE / 2)),
                     4: int((WIDTH - TILESIZE * 3) - (TILESIZE / 2)),
                     5: int((WIDTH - TILESIZE * 4) - (TILESIZE / 2)),
                     6: int((WIDTH - TILESIZE * 5) - (TILESIZE / 2)),
                     7: int((WIDTH - TILESIZE * 6) - (TILESIZE / 2)),
                     8: int((WIDTH - TILESIZE * 7) - (TILESIZE / 2))}

        xPixel = xMappings[location[0]]
        yPixel = yMappings[location[1]]
        return xPixel, yPixel

    def convertPieceLoc(self, piece):
        return self.convertedLoc(piece.getPieceLoc())

    def convertToLoc(self, pos):
        location = []
        flooredPos = [math.floor(pos[0] / TILESIZE) * TILESIZE, math.floor(pos[1] / TILESIZE) * TILESIZE]
        xMappings = {0: "A",
                     TILESIZE: "B",
                     TILESIZE * 2: "C",
                     TILESIZE * 3: "D",
                     TILESIZE * 4: "E",
                     TILESIZE * 5: "F",
                     TILESIZE * 6: "G",
                     TILESIZE * 7: "H"}
        location.append(xMappings[flooredPos[0]])
        location.append(8-(flooredPos[1]//TILESIZE))
        return location

    def drawWhitePiece(self, whitePiece, screen):
        pos = self.convertPieceLoc(whitePiece)
        pygame.draw.circle(screen, PIECE_WHITE, pos, int(TILESIZE / 2) - 10)

    def drawBlackPiece(self, blackPiece, screen):
        pos = self.convertPieceLoc(blackPiece)
        pygame.draw.circle(screen, PIECE_BLACK, pos, int(TILESIZE / 2) - 10)

    def drawPieces(self, game, screen):
        for blackPiece in game.getBlackPieces():
            self.drawBlackPiece(blackPiece, screen)
        for whitePiece in game.getWhitePieces():
            self.drawWhitePiece(whitePiece, screen)

    def drawSelectedPiece(self, selection, screen):
        pos = self.convertedLoc(selection)
        pygame.draw.circle(screen, SELECTED, pos, int(TILESIZE / 2) - 10)

    def updateLog(self, text, screen):
        self.log_string = text + self.log_string
        self.buttons["log"].kill()
        self.buttons["log"] = pygame_gui.elements.ui_text_box.UITextBox(self.log_string,
                                                                        relative_rect=pygame.Rect((0, 800), (650, 150)),
                                                                        manager=self.manager)
        self.buttons["log"].redraw_from_text_block()
        self.manager.update(app.getDT())
        self.manager.draw_ui(screen)
        pygame.display.update()

    def selectPiece(self, screen, event):
        selection = []
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.buttons["quit"]:
                    self.done = True
                    return False
        self.manager.process_events(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            selection = self.convertToLoc(event.pos)

        if not self.validPieceSelection(selection):
            return False
        else:
            self.drawSelectedPiece(selection, screen)
            self.updateLog("SELECTED: " + str(selection) + "<br>", screen)
            return self.convertToID(selection)

    def convertToID(self, selection):
        if self.session.getTurn() % 2 != 0:
            for piece in self.session.getWhitePieces():
                if selection == piece.getPieceLoc():
                    id = piece.getPieceID()
                    #print("ID: " + str(id))
                    return piece
        else:
            for piece in self.session.getBlackPieces():
                if selection == piece.getPieceLoc():
                    id = piece.getPieceID()
                    #print("ID: " + str(id))
                    return piece

    def validPieceSelection(self, selection):
        if self.session.getTurn() % 2 != 0:
            if selection not in self.session.whitePieceLocs():
                return False
            else:
                return True
        else:
            if selection not in self.session.blackPieceLocs():
                return False
            else:
                return True

    def selectTarget(self):
        event = pygame.event.poll()
        while event.type != pygame.MOUSEBUTTONDOWN:
            event = pygame.event.poll()
        target = self.convertToLoc(event.pos)
        #print("TARGET: " + str(target))
        return target

    def gameTurn(self, event):
        pygame.display.update()
        if self.session.getTurn() % 2 != 0:
            selection = self.selectPiece(self.screen, event)
            if not selection:
                return False
            target = self.selectTarget()
            if target == Piece.getPieceLoc(selection):
                return False
            if not Piece.move(selection, self.session.getBoard(), target,
                              self.session.getWhitePieces(), self.session.getBlackPieces()):
                return None
            else:
                text_0 = "Moved piece to {}<br>".format(target)
                self.updateLog(text_0, self.screen)
                text_1 = Piece.removeBeatenPieces(self.session.getBlackPieces(), self.session.getBoard(),
                                     self.session.getWhitePieces())
                text_2 = Piece.removeBeatenPieces(self.session.getWhitePieces(), self.session.getBoard(),
                                         self.session.getBlackPieces())
                if text_1 is not None:
                    self.updateLog(text_1, self.screen)
                elif text_2 is not None:
                    self.updateLog(text_2, self.screen)
                pygame.display.update()
                self.session.checkForGameOver()
                self.session.incrementTurn()
                self.updateLog("TURN Number " + str(self.session.getTurn()) + ": BLACK<br>", self.screen)

        else:
            selection = self.selectPiece(self.screen, event)
            if not selection:
                return False
            target = self.selectTarget()
            if target == Piece.getPieceLoc(selection):
                return False
            if not Piece.move(selection, self.session.getBoard(), target,
                              self.session.getWhitePieces(), self.session.getBlackPieces()):
                return None
            else:
                text_0 = "Moved piece to {}<br>".format(target)
                self.updateLog(text_0, self.screen)
                text_1 = Piece.removeBeatenPieces(self.session.getWhitePieces(), self.session.getBoard(),
                                     self.session.getBlackPieces())
                text_2 = Piece.removeBeatenPieces(self.session.getBlackPieces(), self.session.getBoard(),
                                         self.session.getWhitePieces())
                if text_1 is not None:
                    self.updateLog(text_1, self.screen)
                elif text_2 is not None:
                    self.updateLog(text_2, self.screen)
                pygame.display.update()
                self.session.checkForGameOver()
                self.session.incrementTurn()
                self.updateLog("TURN Number " + str(self.session.getTurn()) + ": WHITE<br>", self.screen)




class Control:
    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        self.size = SIZE
        self.screen = pygame.display.set_mode(self.size)
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(self.fps)/1000.0

    def getDT(self):
        return self.dt

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def flip_state(self):
        self.state.done = False
        previous, self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        self.state.previous = previous

    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, dt)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            self.state.get_event(event)

    def main_game_loop(self):
        while not self.done:
            delta_time = self.clock.tick(self.fps)/1000.0
            self.event_loop()
            self.update(delta_time)
            pygame.display.update()



app = Control(**settings)
state_dict = {
    'menu': Menu(),
    'game': GameState()
}
app.setup_states(state_dict, 'menu')
app.main_game_loop()
pygame.quit()
sys.exit()
