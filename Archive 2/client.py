import socket
import pickle
import pygame
import sys
from pygame.locals import *
from network import Network
from player import Player
import random

width = 611
height = 511

GROUNDY = height * 0.8
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
PIPE = 'gallery/sprites/pipe.png'
GAME_SPRITES = {}
GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180), 
                        pygame.image.load(PIPE).convert_alpha())
GAME_SPRITES['background1'] = pygame.image.load('gallery/sprites/background.png').convert()
GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert()

def redrawWindow(win, player, player2):
    win.blit(GAME_SPRITES['background1'], (0, 0))
    for upperPipe, lowerPipe in zip(player.upperpipes, player.lowerpipes):
        win.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
        win.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
    player2.draw(win, pygame.image.load('gallery/sprites/bird.png').convert_alpha())
    player.draw(win, pygame.image.load('gallery/sprites/bird.png').convert_alpha())
    win.blit(GAME_SPRITES['base'], (0,height*0.8))
    pygame.display.update()


def isCollide(playerx, playery, upperPipes, lowerPipes):
    bird_width = 34  # Adjust according to your bird sprite's width
    bird_height = 24  # Adjust according to your bird sprite's height

    for pipe in upperPipes:
        pipeWidth = GAME_SPRITES['pipe'][0].get_width()
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and playerx + bird_width > pipe['x'] and playerx < pipe['x'] + pipeWidth):
            print("Collided with upper pipe")
            return True

    for pipe in lowerPipes:
        pipeWidth = GAME_SPRITES['pipe'][1].get_width()
        if (playery + bird_height > pipe['y'] and playerx + bird_width > pipe['x'] and playerx < pipe['x'] + pipeWidth):
            print("Collided with lower pipe")
            return True

    return False


def main():
    run = True
    n = Network()
    p = n.getP()
    if not p:
        print("Failed to get initial player data.")
        return

    clock = pygame.time.Clock()

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    playerx = int(width / 5)
    playery = int(height / 2)
    GROUNDY = 511 * 0.8
    playerFlapAccv = -8  # velocity while flapping
    playerFlapped = False

    pipeVelX = -5

    while run:
        clock.tick(30)
        p2 = n.send(p)
        if p2 == "Game Over":
            return winner()

        if not p2:
            print("Failed to receive player data.")
            return loser()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                print("Game quit")
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playery = playery + min(playerVelY, GROUNDY - playery - 24)

        if p:
            crashTest = isCollide(playerx, playery, p.upperpipes, p.lowerpipes)  # This function will return true if the player is crashed
            if crashTest:
                p.msg = "crashed"
                n.send(p)
                return loser()

            for upperPipe, lowerPipe in zip(p.upperpipes, p.lowerpipes):
                pipeHeight = GAME_SPRITES['pipe'][0].get_height()
                upperPipe['x'] += pipeVelX
                lowerPipe['x'] += pipeVelX

            if 0 < p.upperpipes[0]['x'] < 5:
                newpipe = getRandomPipe()
                p.upperpipes.append(newpipe[0])
                p.lowerpipes.append(newpipe[1])

            if p.upperpipes[0]['x'] < -52:
                p.upperpipes.pop(0)
                p.lowerpipes.pop(0)

            p.update(playerx, playery)
            redrawWindow(win, p, p2)
        else:
            print("Player object is None.")
            return loser()


def getRandomPipe():
    pipeHeight = 320
    offset = height / 4  # decides the distance between the pipes
    y2 = offset + random.randrange(0, int(height - 112 - 1.2 * offset))
    pipeX = width + 10  # the place where the pipes are generated
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},  # upper Pipe
        {'x': pipeX, 'y': y2}  # lower Pipe
    ]
    return pipe


def winner():
    print("You win")
    pygame.quit()
    sys.exit()


def loser():
    print("You lose")
    pygame.quit()
    sys.exit()


main()
