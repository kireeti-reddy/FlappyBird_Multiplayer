import pygame
import pygame
from pygame.locals import *

class Player():
    def __init__(self, playerx, playery, upperpipes, lowerpipes, msg):
        #self.pl= pygame.image.load('gallery/sprites/bird.png').convert_alpha()

        self.upperpipes = upperpipes
        self.lowerpipes = lowerpipes
        self.msg = msg
        self.playerx = playerx
        self.playery = playery
        self.rect = (self.playerx, self.playery)
        self.pipeVelX = -5
        self.pipeVelY = -2
        self.playerVelY = -9
        self.playerMaxVelY = 10
        self.playerMinVelY = -8
        self.playerAccY = 1
        self.GROUNDY = 511 * 0.8

        self.playerFlapAccv = -8 # velocity while flapping
        self.playerFlapped = False # It is true only when the bird is flapping

    def draw(self, win, image):
        win.blit(image, (self.rect[0], self.rect[1]))

    def move(self):

        self.update()

    def update(self, playerx, playery):
        self.rect = (playerx, playery)