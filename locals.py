import pygame, random

TILESIZE = 32
MOVEMENT_DISTANCE = 1
HERO_MOVE_SPEED = 32  #squares of movement allowed per second
PLAYER_IMAGE_SIZE = (64,64)

zoneDict = {'testMap':'data/zones/testZone.txt'}

movementKeys = [pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d]

directionDict = {0:'up',1:'down',2:'left',3:'right'}

spriteDirectionDict={'up':0,'left':64,'down':64*2,'right':64*3
    }
