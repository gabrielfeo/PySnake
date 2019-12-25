# PYSNAKE

'''
    Author:
    -------
    Jai Ganesh

    Date:
    -----
    25-DEC-2019

    modules req:
    ------------
    -> pygame
    -> random
    -> time
'''

import pygame
from random import randrange
import time

def yourScore(score):
    value = scoreFont.render("Your Score: " + str(score), True, yellow)
    screen.blit(value, [0, 0])


def drawSnakeOrFood(color, x, y):
    pygame.draw.rect(screen, color, [x, y, snake_block, snake_block])


def snake(snakeBody):
    for block in snakeBody[:-1]:
        drawSnakeOrFood(white, block[0], block[1])
    block = snakeBody[-1]
    drawSnakeOrFood(black, block[0], block[1])


def createFood():
    foodX = round(randrange(0, (width - snake_block)) / 10) * 10
    foodY = round(randrange(0, (height - snake_block)) / 10) * 10
    return foodX, foodY


def findDirection(x1_change, y1_change, gameOver):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x1_change = -snake_block
                y1_change = 0
            if event.key == pygame.K_RIGHT:
                x1_change = snake_block
                y1_change = 0
            if event.key == pygame.K_UP:
                x1_change = 0
                y1_change = -snake_block
            if event.key == pygame.K_DOWN:
                x1_change = 0
                y1_change = snake_block
    return (x1_change, y1_change, gameOver)


def checkSnakeAte(snakeX, snakeY, foodX, foodY, snakeLength):
    if snakeX == foodX and snakeY == foodY:
        foodX, foodY = createFood()
        snakeLength += 1
        print("yummy")
    return foodX, foodY, snakeLength


def checkSnakeHitWalls(x1, y1):
    return x1 >= width or x1 < 0 or y1 >= height or y1 < 0


def checkQuitOrContinue(gameClose, gameOver, loopAgain):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                gameClose = False
                gameOver = True
            if event.key == pygame.K_c:
                loopAgain = True
    return gameClose, gameOver, loopAgain


def checkGameClose(gameClose, gameOver, snakeLength):
    loopAgain = False
    while gameClose:
        screen.fill(green)
        message("You Lost! Press Q-Quit or C-Play Again", white)
        yourScore(snakeLength - 1)
        pygame.display.update()
        gameClose, gameOver, loopAgain = checkQuitOrContinue(
            gameClose, gameOver, loopAgain)
        if loopAgain:
            gameLoop()
    return gameClose, gameOver


def message(msg, color):
    messg = fontStyle.render(msg, True, color)
    screen.blit(messg, [width / 5, height / 3])

# Main game loop 
def gameLoop():
    # Initial position of snake
    x1 = width / 2
    y1 = height / 2
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
        x1_change, y1_change, gameOver = findDirection(x1_change, y1_change, gameOver)
        x1 += x1_change
        y1 += y1_change

        # Check Snake hits the wall
        gameClose = checkSnakeHitWalls(x1, y1)

        # Fill backfround with grass
        screen.fill(green)

        # put snake's fav BLUEsect
        drawSnakeOrFood(blue, foodX, foodY)

        # Take snake's head for each loop until it's not eating
        snake_head = [x1, y1]
        snakeBody.append(snake_head)
        if len(snakeBody) > snakeLength:
            del snakeBody[0]

        # Check whether it bites itself
        for block in snakeBody[:-1]:
            if block == snake_head:
                gameClose = True

        # Ohhh!!! It's growing
        snake(snakeBody)
        yourScore(snakeLength - 1)
        pygame.display.update()

        # Check whether snake is eating
        foodX, foodY, snakeLength = checkSnakeAte(x1, y1, foodX, foodY, snakeLength)

        # Snake is so active!
        clock.tick(snake_speed)
        
    # GoodBye! Miss you poison!!!
    message("Quiting Game", white)
    pygame.display.update()
    time.sleep(2.5)
    pygame.quit()
    quit()

# Screen size
size = width, height = 800, 600

# Color codes
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (5,102,8)
blue = (50, 153, 213)

snake_block = 10 # Snake size
snake_speed = 10 # Snake speed

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
