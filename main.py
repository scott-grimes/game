import pygame, sys, random
from Player import Player
from pygame.locals import *
import datetime
    
DIRT = 0
GRASS = 1
WATER = 2
COAL = 3
SPEED = 1

textures = {
            DIRT : pygame.image.load('data/images/dirt.png'),
            GRASS : pygame.image.load('data/images/grass.png'),
            WATER : pygame.image.load('data/images/water.png'),
            COAL : pygame.image.load('data/images/coal.png')
            }

resources = [DIRT,GRASS,WATER,COAL]




TILESIZE = 40
MAPWIDTH = 15
MAPHEIGHT = 10


tilemap =[[random.choice(resources) for w in range(MAPWIDTH)] for h in range(MAPHEIGHT)]

pygame.init()

player = Player()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE,MAPHEIGHT*TILESIZE))
pygame.display.set_caption('MVMMORPG')
PLAYER = pygame.image.load(player.image).convert_alpha()


def processCommands():
    lastMove = datetime.datetime.now()
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
    if (sum(pygame.key.get_pressed())>0):
        currentTime = datetime.datetime.now()
        
        while(currentTime < (lastMove+datetime.timedelta(milliseconds=player.speed))):
            currentTime = datetime.datetime.now()
        
        keys = pygame.key.get_pressed()
        if((keys[pygame.K_d]) and player.pos[0] < MAPWIDTH-1):
            player.pos[0]+=.1
        if((keys[pygame.K_a]) and player.pos[0] > 0):
            player.pos[0]-=.1
        if((keys[pygame.K_w]) and player.pos[1] > 0):
            player.pos[1]-=.1
        if((keys[pygame.K_s]) and player.pos[1] < MAPHEIGHT-1):
            player.pos[1]+=.1
        lastMove = datetime.datetime.now()

def updateScreen():
    for row in range(MAPHEIGHT):
        for column in range(MAPWIDTH):
            DISPLAYSURF.blit(textures[tilemap[row][column]],(column*TILESIZE,row*TILESIZE))
    DISPLAYSURF.blit(PLAYER,(player.pos[0]*TILESIZE,player.pos[1]*TILESIZE))
    pygame.display.update()
    
while True:
    processCommands() 
    updateScreen()       
            
    