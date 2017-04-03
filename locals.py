import pygame, random

TILESIZE = 32
PLAYER_IMAGE_SIZE = (64,64)

zoneDict = {'testMap':'data/zones/testZone.txt'}

movementKeys = [pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d]

directionDict = {0:'up',1:'down',2:'left',3:'right'}

spriteDirectionDict={'up':0,'left':1,'down':2,'right':3
    }

#id, [name, image location, image size, number of animations, 
#aggro flag, aggro distance, milisseconds to move one tile
NPCS = {
    '0001':['slime','data/images/LPC Base Assets/sprites/monsters/slime.png',[32,32],3,1,5,800]
    
    }