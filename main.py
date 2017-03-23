import pygame, sys, datetime
from Player import Player
from pygame.locals import *
from pygame.colordict import THECOLORS as COLOR
from locals import *

pygame.init()

player = Player()

DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE,MAPHEIGHT*TILESIZE))
pygame.display.set_caption('MVMMORPG')
PLAYER = pygame.image.load(player.image).convert_alpha()


def processCommands():
    
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
            
    keys = pygame.key.get_pressed()
    
    if (sum(keys)>0): #if a key is pressed
        
        if(sum(keys[a] for a in movementKeys) ): #if a movement key is pressed...
           
            if(pygame.time.get_ticks()>player.lastMove+player.movementDelay):
                if((keys[pygame.K_d]) and player.pos[0] < MAPWIDTH-1):
                    player.pos[0]+=.5
                if((keys[pygame.K_a]) and player.pos[0] > 0):
                    player.pos[0]-=.5
                if((keys[pygame.K_w]) and player.pos[1] > 0):
                    player.pos[1]-=.5
                if((keys[pygame.K_s]) and player.pos[1] < MAPHEIGHT-1):
                    player.pos[1]+=.5
                player.lastMove = pygame.time.get_ticks()
        

def updateScreen():
    for row in range(MAPHEIGHT):
        for column in range(MAPWIDTH):
            DISPLAYSURF.blit(textures[tilemap[row][column]],(column*TILESIZE,row*TILESIZE))
    DISPLAYSURF.blit(PLAYER,(player.pos[0]*TILESIZE,player.pos[1]*TILESIZE))
    pygame.display.update()
    
    
def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(mouse)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(DISPLAYSURF, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(DISPLAYSURF, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    DISPLAYSURF.blit(textSurf, textRect)
    
def runGame():
    while True:
        processCommands() 
        updateScreen()   
          
def startScreen():
        while True:
            button("hi",10,10,100,100,COLOR['white'],COLOR['red'],runGame)
            pygame.display.update()
            event = pygame.event.wait()
            
        
    
sys.exit(startScreen())

    
               