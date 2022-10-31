import pygame


# returns board back to empty / initializes it
def init_board():
    return [['', '', ''], ['', '', ''], ['', '', '']]


pygame.init()

# initializes variables
grey = (130, 130, 130)
pink = (255, 192, 203)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
black = (0, 0, 0)
board = init_board()
dis = pygame.display.set_mode((900, 700))
font = pygame.font.SysFont("malgungothic", 25)


# main menu
def start():
    dis.fill(pink)
    pygame.display.set_caption("Tic-Tac-Toe")

    # loads title image
    image = pygame.image.load("bigtic.png")
    dis.blit(image, [(dis.get_width() - image.get_width()) / 2, (dis.get_height() / 2) - 300])

    # loads start image
    image = pygame.image.load("start.png")
    rectStart = dis.blit(image, [(dis.get_width() - image.get_width()) / 2, (dis.get_height() / 2)])

    pygame.display.update()

    # when the start image is changed its true otherwise it's false
    startchanged = False

    # loops forever until some event happens
    while True:

        # loops through all events that happen
        for event in pygame.event.get():

            # quit when event type is quit
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEMOTION:

                # checks if the mouse is in the start image
                if rectStart.collidepoint(pygame.mouse.get_pos()):
                    image = pygame.image.load("hoverStart.png")
                    rectStart = dis.blit(image, [(dis.get_width() - image.get_width()) / 2, (dis.get_height() / 2)])
                    startchanged = True
                    pygame.display.update()
                else:
                    # only if the start image changed images change it back to old image
                    if startchanged:
                        image = pygame.image.load("start.png")
                        rectStart = dis.blit(image, [(dis.get_width() - image.get_width()) / 2, (dis.get_height() / 2)])
                        startchanged = False
                        pygame.display.update()

            # changes image when pressed down over start image
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rectStart.collidepoint(pygame.mouse.get_pos()):
                    image = pygame.image.load("hoverStart.png")
                    rectStart = dis.blit(image, [(dis.get_width() - image.get_width()) / 2, (dis.get_height() / 2)])
                    pygame.display.update()

            # changes image when released and then starts game
            elif event.type == pygame.MOUSEBUTTONUP:
                if rectStart.collidepoint(pygame.mouse.get_pos()):
                    image = pygame.image.load("start.png")
                    rectStart = dis.blit(image, [(dis.get_width() - image.get_width()) / 2, (dis.get_height() / 2)])
                    pygame.display.update()
                    global board
                    board = init_board()
                    game_loop()


# displays a message on screen
def message(msg, color):
    mes = font.render(msg, True, color)
    dis.blit(mes, [dis.get_width() / 3, dis.get_height() / 3])


# displays what player is going to be placed
def displayPlayer(player):
    saying = "Player: " + player
    msg = font.render(saying, True, (255, 255, 255))
    pygame.draw.rect(dis, pink, [(dis.get_width() - msg.get_width()) / 2, 10, msg.get_width(), msg.get_height()])
    dis.blit(msg, [(dis.get_width() - msg.get_width()) / 2, 10])


def draw_board(color, color2):
    dx = dis.get_width()
    dy = dis.get_height() - 90
    pygame.draw.rect(dis, color2, [dx / 3, 80, 10, dy])
    pygame.draw.rect(dis, color2, [dx * (2 / 3), 80, 10, dy])
    pygame.draw.rect(dis, color2, [10, (dy / 3) + 70, dx - 20, 10])
    pygame.draw.rect(dis, color2, [10, dy * (2 / 3) + 70, dx - 20, 10])
    tl = pygame.draw.rect(dis, color, [10, 80, (dx / 3) - 10, (dy / 3) - 10])
    tm = pygame.draw.rect(dis, color, [(dx / 3) + 10, 80, (dx / 3) - 9, (dy / 3) - 10])
    tr = pygame.draw.rect(dis, color, [(dx * (2 / 3)) + 10, 80, dx / 3 - 20, (dy / 3) - 10])
    ml = pygame.draw.rect(dis, color, [10, (dy / 3) + 80, (dx / 3) - 10, dy / 3 - 10])
    mm = pygame.draw.rect(dis, color, [(dx / 3) + 10, (dy / 3) + 80, (dx / 3) - 9, (dy / 3) - 10])
    mr = pygame.draw.rect(dis, color, [dx * (2 / 3) + 10, (dy / 3) + 80, dx / 3 - 20, dy / 3 - 10])
    bl = pygame.draw.rect(dis, color, [10, dy * (2 / 3) + 80, dx / 3 - 10, (dy / 3) + 10])
    bm = pygame.draw.rect(dis, color, [(dx / 3) + 10, (dy * (2 / 3)) + 80, (dx / 3) - 9, (dy / 3) - 10])
    br = pygame.draw.rect(dis, color, [dx * (2 / 3) + 10, (dy * (2 / 3)) + 80, dx / 3 - 20, dy / 3 - 10])
    pygame.display.update()
    rectangles = [[tl, tm, tr], [ml, mm, mr], [bl, bm, br]]
    return rectangles


def winner(b):
    level = 0
    # checks horizontal
    for y in b:
        if not y[0] == '':
            if y[0] == y[1] and y[0] == y[2]:
                return [[level, 0], [level, 1], [level, 2]]
        level += 1

    # checks vertical
    for i in range(0, 3, 1):
        if not b[0][i] == '':
            if b[0][i] == b[1][i] and b[0][i] == b[2][i]:
                return [[0, i], [1, i], [2, i]]

    # checks diagonals
    if b[0][0] == b[1][1] and b[0][0] == b[2][2]:
        return [[0, 0], [1, 1], [2, 2]]
    if b[0][2] == b[1][1] and b[0][2] == b[2][0]:
        return [[0, 2], [1, 1], [2, 0]]


# Creates a new shape on screen and adds it to the board
def draw_new_shape(rect, color, width, clicks, x, y):
    # if the click count is even then it will draw an x other wise an o
    if clicks % 2 == 0:
        pygame.draw.line(dis, color, rect.topleft, rect.bottomright, width)
        pygame.draw.line(dis, color, rect.topright, rect.bottomleft, width)
        board[x][y] = 'x'
        return '0'
    else:
        pygame.draw.circle(dis, black, rect.center, rect.width / 4)
        pygame.draw.circle(dis, pink, rect.center, rect.width / 4.2)
        board[x][y] = 'o'
        return 'x'


# redraws shapes on the board
def draw_old_shape(rect, color, width, b):
    # gets the color of the background to use in the circle
    inside = dis.get_at([0, 0])

    # loops through board and redraws the shapes
    for x in range(0, 3, 1):
        for y in range(0, 3, 1):
            if b[x][y] == 'x':
                pygame.draw.line(dis, color, rect[x][y].topleft, rect[x][y].bottomright, width)
                pygame.draw.line(dis, color, rect[x][y].topright, rect[x][y].bottomleft, width)
            elif b[x][y] == 'o':
                pygame.draw.circle(dis, black, rect[x][y].center, rect[x][y].width / 4)
                pygame.draw.circle(dis, inside, rect[x][y].center, rect[x][y].width / 4.2)


# checks where the mouse is and sees if it is in a rectangle
def check_collision(b, rect, pos, clicks):
    for x in range(0, 3, 1):
        for y in range(0, 3, 1):

            # if  the mouse is in a rectangle, draw a new shape and return what player is up next
            if rect[x][y].collidepoint(pos) and b[x][y] == '':
                player = draw_new_shape(rect[x][y], black, 5, clicks, x, y)
                return player
    # no collisions happened and will return nothing
    return None


# game loop for 2 people, runs main game logic
def game_loop():
    # initialize variables
    click_count = 0
    game_end = False
    dis.fill(pink)
    rectangles = draw_board(pink, grey)
    player = 'x'

    # fills background and then runs the displayPlayer method

    displayPlayer(player)

    # loops through until the game ends
    while not game_end:

        # when there is an event that happens loop through those events
        for event in pygame.event.get():

            # if the event is quit then quit
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # if the event is mouse button up
            elif event.type == pygame.MOUSEBUTTONUP:

                # checks the collision where the mouse button is and the returns what player is next
                player = check_collision(board, rectangles, pygame.mouse.get_pos(), click_count)

                # if player has a value then increase click count and update the player
                if player:
                    click_count += 1
                    displayPlayer(player)

                # if click count is higher than 4 start checking for winners
                if click_count >= 4:

                    # checks for a winner using winner method and returns coords
                    coords = winner(board)

                    # if there is a coord value there is a winner and end the game and run endgame method
                    if coords:
                        game_end = True
                        endgame(coords, rectangles)

        # if click count reaches 9 the board is filled with a stalemate and run endgame method
        if click_count == 9:
            game_end = True
            endgame(None, None)

        pygame.display.update()


# used after game loop is ended, gives user options to quit, replay, and go to menu and also displays winner
def endgame(coords, rect):
    # white is a color code and action is to be updated when an action has been taken
    action = False
    white = (255, 255, 255)

    # if there is nothing in coords then is a stalemate
    if not coords:

        global board

        # redraws the board and changes to red and black
        dis.fill(red)
        rect = draw_board(red, black)
        draw_old_shape(rect, black, 5, board)

        # display stalemate messages and options to quit and such
        msg = font.render("STALEMATE", True, white)
        dis.blit(msg, [dis.get_width() / 2, dis.get_height() / 2])
        msg = font.render("Hit R to restart or Q to quit", True, white)
        dis.blit(msg, [dis.get_width() / 2, dis.get_height() / 1.5])
        msg = font.render("M for menu", True, white)
        dis.blit(msg, [dis.get_width() / 2, dis.get_height() / 1.25])

        pygame.display.update()

        # loops through while an action has not been taken
        while not action:

            # loops through all events
            for event in pygame.event.get():

                # if a key gets pressed
                if event.type == pygame.KEYDOWN:

                    # if the key is r restart the game
                    if event.key == pygame.K_r:
                        action = True
                        board = init_board()
                        game_loop()

                    # if the key is q quit the game
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()

                    # if the key is m return to start
                    elif event.key == pygame.K_m:
                        start()

                # if the event is quit quit the game
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    # if it isnt a stalemate then it has to be a win
    else:
        
        global board
        
        # draw a line through the spots that made the win
        pygame.draw.line(dis, red, rect[coords[0][0]][coords[0][1]].center, rect[coords[2][0]][coords[2][1]].center, 9)

        # get the winning char
        win = board[coords[0][0]][coords[0][1]]

        # display winning message and options
        msg = font.render("Winner: " + win, True, (255, 255, 255))
        dis.blit(msg, [dis.get_width() / 2 - 30, (dis.get_height() / 2) - 20])
        msg = font.render("Press R to play again or Q to quit.", True, (255, 255, 255))
        dis.blit(msg, [dis.get_width() / 2 - 100, dis.get_height() / 2])
        msg = font.render("M for menu", True, (255, 255, 255))
        dis.blit(msg, [dis.get_width() / 2 - 40, dis.get_height() / 2 + 30])

        pygame.display.update()

        # loops through until an action has been taken
        while not action:

            # loops through all events
            for event in pygame.event.get():

                # based on same options in the stalemate, do those things when a key is pressed
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_r:
                        action = True
                        board = init_board()
                        game_loop()

                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()

                    elif event.key == pygame.K_m:
                        start()

                # quit when event is quit
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    quit()


# start the program
start()
