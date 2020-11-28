# PYSNAKE

'''
    Author:
    -------
    Jai Ganesh

    Date:
    -----
    CREATED : 25-DEC-2019
    AMENDED : 30-DEC-2019

    modules req:
    ------------
    -> pygame
    -> random
    -> time
'''

import pygame
from random import randrange, randint
import time

"""
Modificação de cores
Modificação alguma regra do jogo (ex: pontuação ou da forma de pontuar)
Mudar arquivos assets (imagem/som/gif/sprite) ou textos ou fonts
Adicionar mais teclas de comando (quanto tem direcional, adicionar WASD ao mesmo tempo)
Mudar o avanço do jogo (não é mudar o fps)
Criar elemento novo para o jogo
Mudar posição de inicio dos heróis ou dos elementos
"""


def yourScore(score):
    value = scoreFont.render(f'Your Score: {str(score)}', True, scoreTextColor)
    screen.blit(value, [0, 0])


def drawSnakeOrFood(color, x, y):
    pygame.draw.rect(screen, color, [x, y, snake_block, snake_block])


def snake(snakeBody):
    for block in snakeBody[:-1]:
        drawSnakeOrFood(snakeBodyColor, block[0], block[1])
    block = snakeBody[-1]
    drawSnakeOrFood(snakeHeadColor, block[0], block[1])


def createFood():
    foodX = round(randrange(0, (width - snake_block)) / 10) * 10
    foodY = round(randrange(0, (height - snake_block)) / 10) * 10
    return foodX, foodY


def checkEvents(x1_change, y1_change, gameOver):
    pause = False
    speedChange = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        elif event.type == pygame.KEYDOWN:
            if isLeftCommand(event.key):
                x1_change = -snake_block
                y1_change = 0
            elif isRightCommand(event.key):
                x1_change = snake_block
                y1_change = 0
            elif isUpCommand(event.key):
                x1_change = 0
                y1_change = -snake_block
            elif isDownCommand(event.key):
                x1_change = 0
                y1_change = snake_block
            elif event.key == pygame.K_p:
                pause = True
            elif event.key == pygame.K_s:
                pause = False
            elif event.key == pygame.K_RIGHTBRACKET:
                speedChange = speedChangeUnit
            elif event.key == pygame.K_LEFTBRACKET:
                speedChange = -speedChangeUnit
    print(f"returning from checkEvents with gameOver={gameOver}")
    return x1_change, y1_change, speedChange, gameOver, pause


def isUpCommand(key):
    return key == pygame.K_UP or key == pygame.K_w


def isDownCommand(key):
    return key == pygame.K_DOWN or key == pygame.K_s


def isLeftCommand(key):
    return key == pygame.K_LEFT or key == pygame.K_a


def isRightCommand(key):
    return key == pygame.K_RIGHT or key == pygame.K_d


def checkSnakeAte(snakeX, snakeY, foodX, foodY, snakeLength):
    ateFood = snakeX == foodX and snakeY == foodY
    if ateFood:
        foodX, foodY = createFood()
        snakeLength += 1
        print("yummy")
    return foodX, foodY, snakeLength, ateFood


def checkSnakeHitWalls(x1, y1):
    return x1 >= width or x1 < 0 or y1 >= height or y1 < 0


def incrementScore():
    global score
    score += 1


def resetScore():
    global score
    score = 0


def changeSnakeSpeed(change):
    global snake_speed
    snake_speed = max(1, snake_speed + change)


def checkPause(pause):
    if pause:
        message("Game Paused. press 'S' to continue ")
        pygame.display.update()
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                if event.key == pygame.K_s:
                    pause = False
    return pause


def checkQuitOrContinue(gameClose, gameOver, loopAgain):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                gameClose = False
                gameOver = True
            if event.key == pygame.K_c:
                loopAgain = True
    print(f"returning from checkQuitOrContinue with gameOver={gameOver}")
    return gameClose, gameOver, loopAgain


def checkGameClose(gameClose, gameOver, snakeLength):
    loopAgain = False
    while gameClose:
        screen.fill(gameOverBackgroundColor)
        message("You Lost! Press Q-Quit or C-Play Again")
        yourScore(score)
        pygame.display.update()
        gameClose, gameOver, loopAgain = checkQuitOrContinue(
            gameClose, gameOver, loopAgain)
        if loopAgain:
            gameLoop()
    return gameClose, gameOver


def message(msg):
    messg = fontStyle.render(msg, True, messageColor)
    screen.blit(messg, [width / 5, height / 3])

# Main game loop
def gameLoop():
    # Initial position of snake
    x1 = randint(0, width)
    y1 = randint(0, height)
    # To detect change in direction
    x1_change = 0
    y1_change = 0
    # To check when to quit game
    gameOver, gameClose = False, False
    # Snake about to hatch from egg
    snakeBody = []
    snakeLength = 1
    # Food position for baby snake
    foodX, foodY = createFood()

    # Loop until game is not over
    while not gameOver:
        # Check game over details
        gameClose, gameOver = checkGameClose(gameClose, gameOver, snakeLength)

        # Get change in snake movement
        eventReactions = checkEvents(x1_change, y1_change, gameOver)
        x1_change, y1_change, speedChange, gameOver, pause = eventReactions
        x1 += x1_change
        y1 += y1_change
        changeSnakeSpeed(speedChange)

        # Check Snake hits the wall
        gameClose = checkSnakeHitWalls(x1, y1)

        # Fill backfround with grass
        screen.fill(inGameBackgroundColor)

        # put snake's fav BLUEsect
        drawSnakeOrFood(foodColor, foodX, foodY)

        # Take snake's head for each loop until it's not eating
        snake_head = [x1, y1]
        snakeBody.append(snake_head)
        if len(snakeBody) > snakeLength:
            del snakeBody[0]

        # Check whether it bites itself
        for block in snakeBody[:-1]:
            if block == snake_head:
                resetScore()
                screen.fill(gameOverBackgroundColor)  # Not over, but flash red background

        # Ohhh!!! It's growing
        snake(snakeBody)
        yourScore(score)
        pygame.display.update()

        # Check whether snake is eating
        foodX, foodY, snakeLength, ateFood = checkSnakeAte(x1, y1, foodX, foodY, snakeLength)
        if ateFood:
            incrementScore()

        # Snake is so active!
        clock.tick(snake_speed)

    # GoodBye! Miss you poison!!!
    message("Quiting Game")
    pygame.display.update()
    time.sleep(2.5)
    pygame.quit()
    quit()

# Screen size
size = width, height = 800, 600

# Color codes
white = (255, 255, 255)
lightGray = (200, 200, 200)
chocolateBrown = (100, 30, 30)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (200, 0, 0)
green = (5, 102, 8)
blue = (50, 153, 213)

# Color resources
inGameBackgroundColor = green
gameOverBackgroundColor = red
scoreTextColor = yellow
messageColor = black
snakeHeadColor = white
snakeBodyColor = lightGray
foodColor = chocolateBrown

snake_block = 10 # Snake size
snake_speed = 20 # Snake speed
speedChangeUnit = 2

score = 0

# Pygame initial settings
pygame.init()
fontStyle = pygame.font.SysFont("bahnschrift", 25)
scoreFont = pygame.font.SysFont("comicsansms", 35)
icon = pygame.image.load('snake.png')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PySnake")
clock = pygame.time.Clock()

# Start Game
gameLoop()
