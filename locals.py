import pygame, random

TILESIZE = 32
MOVEMENT_DISTANCE = 1
HERO_MOVE_SPEED = 1  # pixels per second

zoneDict = {'testMap':'data/zones/testZone.txt'}

movementKeys = [pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d]

directionDict = {0:'up',1:'down',2:'left',3:'right'}

textures = {
    
            }

levelDict = {'test': 'testMap.p'
    }


