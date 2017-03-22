import pygame, sys
from pygame.locals import *

DIRT = 0
GRASS = 1
WATER = 2
COAL = 3

inventory = []

textures = {
            DIRT : pygame.image.load('data/dirt.png'),
            GRASS : pygame.image.load('data/grass.png'),
            WATER : pygame.image.load('data/water.png'),
            COAL : pygame.image.load('data/coal.png')
            }



tilemap =[
            [GRASS, COAL, DIRT],
            [GRASS, GRASS, DIRT],
            [GRASS, COAL, GRASS],
            [DIRT, GRASS, GRASS],
            [DIRT, DIRT, COAL],   
            ]

TILESIZE = 40
MAPWIDTH = 3
MAPHEIGHT = 5

pygame.init()


DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE,MAPHEIGHT*TILESIZE))
pygame.display.set_caption('MVMMORPG')
PLAYER = pygame.image.load('data/player.png').convert_alpha()
playerPos = [0,0]

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==KEYDOWN:
            if((event.key==K_RIGHT) and playerPos[0] < MAPWIDTH-1):
                playerPos[0]+=1
            if((event.key==K_LEFT) and playerPos[0] > 0):
                playerPos[0]-=1
            if((event.key==K_UP) and playerPos[1] > 0):
                playerPos[1]-=1
            if((event.key==K_DOWN) and playerPos[1] < MAPHEIGHT-1):
                playerPos[1]+=1
    for row in range(MAPHEIGHT):
        for column in range(MAPWIDTH):
            DISPLAYSURF.blit(textures[tilemap[row][column]],(column*TILESIZE,row*TILESIZE))
    DISPLAYSURF.blit(PLAYER,(playerPos[0]*TILESIZE,playerPos[1]*TILESIZE))
    pygame.display.update()
