import pygame, random

TILESIZE = 40
MAPWIDTH = 15
MAPHEIGHT = 10

DIRT = 0
GRASS = 1
WATER = 2
COAL = 3

movementKeys = [pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d]

textures = {
            DIRT : pygame.image.load('data/images/dirt.png'),
            GRASS : pygame.image.load('data/images/grass.png'),
            WATER : pygame.image.load('data/images/water.png'),
            COAL : pygame.image.load('data/images/coal.png')
            }


resources = [DIRT,GRASS,WATER,COAL]


tilemap =[[random.choice(resources) for w in range(MAPWIDTH)] for h in range(MAPHEIGHT)]
