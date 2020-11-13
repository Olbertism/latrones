# Free Fly Version, erster Draft, OOP

import pygame
import math

#pygame initialization
TILESIZE = 100
ROWS = 8
COLUMNS = 8

WIDTH = COLUMNS * TILESIZE
HEIGHT = ROWS * TILESIZE
SIZE = (WIDTH, HEIGHT)

BOARD_BLACK = (31, 20, 2)
BOARD_WHITE = (245, 241, 232)

PIECE_BLACK = (76, 69, 56)
PIECE_WHITE = (216, 190, 147)

pygame.init()

screen = pygame.display.set_mode(SIZE)





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

    def occupiedFields(self):
        occupancies = []
        for i in WHITE_PIECES:
            occupancies.append(Piece.getPieceLoc(i))
        for i in BLACK_PIECES:
            occupancies.append(Piece.getPieceLoc(i))
        return occupancies

    def occupiedWhite(self):
        occupancies = []
        for i in WHITE_PIECES:
            occupancies.append(Piece.getPieceLoc(i))
        return occupancies

    def occupiedBlack(self):
        occupancies = []
        for i in BLACK_PIECES:
            occupancies.append(Piece.getPieceLoc(i))
        return occupancies


    def __str__(self):
        return "{}, {}".format(self.xAxis, self.yAxis)


#classes for the game pieces and their corresponding actions

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
        PieceLocs = []
        for j in self:
            PieceLocs.append(Piece.getPieceLoc(j))
        return PieceLocs

    def remove(self, element):
        self.remove(element)
        return self




# movements

    def isValid(self, aBoard, targetLoc):
        # function to check movement validity, returns True or False
        # if check passed, movement can be executed (realized in movement function)
        occupancies = Board.occupiedFields(aBoard)
        path = []

        x = Piece.getPieceLoc(self)[0]
        xaxis = Board.getX(aBoard)
        xindex = xaxis.index(x)

        if Piece.getPieceLoc(self)[0] == targetLoc[0]:
            if Piece.getPieceLoc(self)[1] < targetLoc[1]:
                for i in range(Piece.getPieceLoc(self)[1], targetLoc[1]):
                    path.append(Board.provideLoc(aBoard, xindex, i)) # der 0er hier verweist immer auf A

            else:
                for i in range(targetLoc[1], Piece.getPieceLoc(self)[1]-1):
                    path.append(Board.provideLoc(aBoard, xindex, i))
            if any(elem in path for elem in occupancies):
                return False
            else:
                return True
        elif Piece.getPieceLoc(self)[1] == targetLoc[1]:
            x = Board.getX(aBoard).index(Piece.getPieceLoc(self)[0])
            y = Board.getX(aBoard).index(targetLoc[0])
            if x < y:
                for i in range(x+1, y+1):
                    path.append(Board.provideLoc(aBoard, i, 1))
            else:
                for i in range(y+1, x+1):
                    path.append(Board.provideLoc(aBoard, i, 1))
            if any(elem in path for elem in occupancies):
                return False
            else:
                return True
        else:
            print("Invalid movement!")


    def move(self, aBoard, targetLoc):
        '''

        :param self: the piece
        :param targetLoc: List, [0] = A-H, [1] = 0-8
        :return: changes the location attribute of the piece instance to targetLoc, if validity test is passed
        '''
        x = self.location
        if Piece.isValid(self, aBoard, targetLoc):
            self.location = targetLoc
            print("Moved piece from {} to {}".format(x, self.location))
        else:
            print("invalid movement")


# serve beatings

    def checkIfBeaten(self, aBoard, other):
        '''
        ("A", "B", "C", "D", "E", "F", "G", "H")
        :param aBoard: Board is needed to provide X-Coordinates
        :param other: The other colour, to compare against to
        :return: True if beaten
        '''

        x = Piece.getPieceLoc(self)[0]
        y = Piece.getPieceLoc(self)[1]
        if [x, y+1] in other and [x, y-1] in other:
            print("might be beaten (up down)")
            return True
        xaxis = Board.getX(aBoard)
        xindex = xaxis.index(x)
        try:
            if [xaxis[xindex+1], y] in Piece.currentLocations(other) and [xaxis[xindex-1], y] in Piece.currentLocations(other):
                print("{} might be beaten (left right)".format(self))
                return True
        except IndexError:
            pass


    def removeBeatenPieces(self, aBoard, other):
        '''

        :param aBoard: needed for check function (see above)
        :param other: needed for check function (see above)
        :return: nothing, just removes a piece
        '''
        for piece in self:
            if Piece.checkIfBeaten(piece, aBoard, other):
                print("we need to remove {}".format(piece))
                self.remove(piece)



class WhitePiece(Piece):
    '''
    class for white games pieces
    '''

    def __init__(self, location, ID):
        Piece.__init__(self, location)
        self.ID = ID

    def getPieceID(self):
        return self.ID

    def show(self):
        global screen
        pass

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

    def gameTurn(self):
        if self.getTurn() % 2 != 0:
            selection = []
            target = []

            # while selection == []:
            #     if e.type == pygame.MOUSEBUTTONDOWN:
            #         selection = convertToLoc(e.pos)
            #         for piece in session.getWhitePieces():
            #             if selection == piece.getPieceLoc():
            #                 selection = piece.getPieceID()
            #                 print(selection)
            #
            #
            #
            # while target == []:
            #     if e.type == pygame.MOUSEBUTTONDOWN:
            #         target = convertToLoc(e.pos)



            Piece.move(self.getWhitePieces()[int(selection)], self.getBoard(), [target[0], target[1]])

            Piece.removeBeatenPieces(BLACK_PIECES, BOARD, WHITE_PIECES)
            self.incrementTurn()
        else:
            aPiece = input("Black turn. Pick a piece by its ID (0-15):")
            # assert aPiece == type(int)
            target_x = input("Enter a target x-coordinate (A-H):")
            target_y = input("Enter target y-coordinate (1-8):")
            Piece.move(BLACK_PIECES[int(aPiece)], BOARD, [target_x, int(target_y)])
            Piece.removeBeatenPieces(WHITE_PIECES, BOARD, BLACK_PIECES)
            self.incrementTurn()

    def playGame(self):
        user_input = ""
        while user_input != "q":
            user_input = input("type s to make a turn, q to quit:")
            if user_input == "s":
                self.gameTurn()

    def checkForGameOver(self):
        if self.getBlackPieces() == [] or self.getWhitePieces() == []:
            self.gameOver = True


session = Game(16)

WHITE_PIECES = session.getWhitePieces()
BLACK_PIECES = session.getBlackPieces()
BOARD = session.getBoard()
TURN_COUNT = session.getTurn()








#pygame functions

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

    def cleanup(self):
        print("cleaning up Menu state")
    def startup(self):
        print("starting Menu state")

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            print("Menu State keydown")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.done = True

    def update(self, screen, dt):
        self.draw(screen)

    def draw(self, screen):
        screen.fill((255, 0, 0))

class Game(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'menu'

    def cleanup(self):
        print('cleaning up Game state stuff')
    def startup(self):
        print('starting Game state stuff')

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            print('Game State keydown')
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.done = True
    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        screen.fill((0,0,255))

class Control:
    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

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

def drawBoard(board):
    for i in range(len(board.getX())):
        for j in range(len(board.getY())):
            if i % 2 == 0 and j % 2 != 0:
                pygame.draw.rect(screen, BOARD_BLACK, (i*TILESIZE, j*TILESIZE, TILESIZE, TILESIZE))
            elif i % 2 != 0 and j % 2 == 0:
                pygame.draw.rect(screen, BOARD_BLACK, (i*TILESIZE, j*TILESIZE, TILESIZE, TILESIZE))
            else:
                pygame.draw.rect(screen, BOARD_WHITE, (i * TILESIZE, j * TILESIZE, TILESIZE, TILESIZE))

def convertedLoc(location):
    xMappings = {"A": int((WIDTH-TILESIZE*7)-(TILESIZE/2)),
                 "B": int((WIDTH-TILESIZE*6)-(TILESIZE/2)),
                 "C": int((WIDTH-TILESIZE*5)-(TILESIZE/2)),
                 "D": int((WIDTH-TILESIZE*4)-(TILESIZE/2)),
                 "E": int((WIDTH-TILESIZE*3)-(TILESIZE/2)),
                 "F": int((WIDTH-TILESIZE*2)-(TILESIZE/2)),
                 "G": int((WIDTH-TILESIZE)-(TILESIZE/2)),
                 "H": int((WIDTH-TILESIZE/2))}
    yMappings = {1: int((WIDTH-TILESIZE/2)),
                 2: int((WIDTH-TILESIZE)-(TILESIZE/2)),
                 3: int((WIDTH-TILESIZE*2)-(TILESIZE/2)),
                 4: int((WIDTH-TILESIZE*3)-(TILESIZE/2)),
                 5: int((WIDTH-TILESIZE*4)-(TILESIZE/2)),
                 6: int((WIDTH-TILESIZE*5)-(TILESIZE/2)),
                 7: int((WIDTH-TILESIZE*6)-(TILESIZE/2)),
                 8: int((WIDTH-TILESIZE*7)-(TILESIZE/2))}

    xPixel = xMappings[location[0]]
    yPixel = yMappings[location[1]]
    return xPixel, yPixel

def convertPieceLoc(piece):
    return convertedLoc(piece.getPieceLoc())

def convertToLoc(pos):
    location = []
    flooredPos = [math.floor(pos[0]/TILESIZE) * TILESIZE, math.floor(pos[1]/TILESIZE) * TILESIZE]
    xMappings = {0: "A",
                 TILESIZE: "B",
                 TILESIZE*2: "C",
                 TILESIZE*3: "D",
                 TILESIZE*4: "E",
                 TILESIZE*5: "F",
                 TILESIZE*6: "G",
                 TILESIZE*7: "H"}
    location.append(xMappings[flooredPos[0]])
    location.append(flooredPos[1])
    return location



def drawWhitePiece(whitePiece):
    pos = convertPieceLoc(whitePiece)
    pygame.draw.circle(screen, PIECE_WHITE, pos, int(TILESIZE/2)-10)

def drawBlackPiece(blackPiece):
    pos = convertPieceLoc(blackPiece)
    pygame.draw.circle(screen, PIECE_BLACK, pos, int(TILESIZE / 2) - 10)

def drawPieces(game):
    for blackPiece in game.getBlackPieces():
        drawBlackPiece(blackPiece)
    for whitePiece in game.getWhitePieces():
        drawWhitePiece(whitePiece)


drawBoard(session.getBoard())
drawPieces(session)
pygame.display.update()

#pygame main loop


#
# while True:
#     e = pygame.event.poll()
#     session.gameTurn()
#     pygame.display.update()
#     if e.type == pygame.MOUSEBUTTONDOWN:
#         print(e.pos)
#
#     if e.type == pygame.QUIT:
#         break

# while not session.gameOver:
#     if e.type == pygame.MOUSEBUTTONDOWN:
#         #do something
#         pass


pygame.quit()


print(BLACK_PIECES)
print(WHITE_PIECES)
print(BOARD)

print(BOARD.occupiedFields())

print(WHITE_PIECES)
print(session.playGame())



# JUNK


    # def setUpGame(self):
    #     aBoard = self.createBoard()
    #     pieces_start_set = self.distributePieces()
    #     return pieces_start_set, aBoard


# def currentLocations(WHITE_PIECES, BLACK_PIECES):
#     blackPieceLocs = []
#     whitePieceLocs = []
#     for i in BLACK_PIECES:
#         blackPieceLocs.append(i.getPieceLoc())
#     for j in WHITE_PIECES:
#         whitePieceLocs.append(j.getPieceLoc())
#     return blackPieceLocs, whitePieceLocs

# def whiteCurrentLocations(WHITE_PIECES):
#     whitePieceLocs = []
#     for j in WHITE_PIECES:
#         whitePieceLocs.append(j.getPieceLoc())
#     return whitePieceLocs



# game init variables. somewhat global, somewhat static, tread carefully
