import pygame, sys, datetime
from Player import Player
from importExport import importGameElement, exportGameElement
from pygame.locals import *
from pygame.colordict import THECOLORS as COLOR
from locals import *
from GameState import GameState


pygame.init()
player = Player()
GAMESTATE = None
PLAYER = None
BACKGROUND_IMAGE = pygame.image.load('data/images/loginScreen.png')

pygame.display.set_caption('MVMMORPG')
DISPLAYSURF = pygame.display.set_mode((525,350))

def loadNewLevel(zoneName):
    global GAMESTATE,PLAYER,MAPWIDTH,MAPHEIGHT,COLLISIONS,BACKGROUND_IMAGE
    
    GAMESTATE = GameState(zoneName)
    
    MAPWIDTH = GAMESTATE.MAPWIDTH
    MAPHEIGHT = GAMESTATE.MAPHEIGHT
    COLLISIONS = GAMESTATE.COLLISIONS
    BACKGROUND_IMAGE = pygame.image.load(GAMESTATE.image)
    PLAYER = pygame.image.load(player.image).convert_alpha()
    
def playerStatusMenu():
    #displays the players health and stuff
    pass

def processCommands():
    
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
            
    keys = pygame.key.get_pressed()
    
    #if a key is pressed
    if (sum(keys)>0): 
        
        #array of booleans representing movement keys pressed [W,S,A,D]
        movement_wanted = [keys[a] for a in movementKeys]
        
        #if a movement key is pressed...
        if(sum(movement_wanted) ): 
           
            #if the player has not moved in "player.movementDelay"
            if(pygame.time.get_ticks()>player.lastMove+player.movementDelay):
                
                #array of strings indicating pressed keys ['up','down','left','right']
                directions = [directionDict[i] for i, x in enumerate(movement_wanted) if x]
                
                #check each requested direction, if the user can move that way, update position
                for d in directions:
                    temp = player.newPosition(player.pos, d)
                    if(movementAllowed(temp)):
                        player.pos = [i for i in temp]
                        player.lastMove = pygame.time.get_ticks()
                
        
def movementAllowed(position):
    #returns true if a current position is not out of bounds or collides
    return  (position[0]>=0 and
            position[0]<=MAPWIDTH-1 and
            position[1]<=MAPHEIGHT-1 and
            position[1]>=0 and 
            not player.wouldCollide(position, COLLISIONS))

def updateScreen():
    DISPLAYSURF.blit(BACKGROUND_IMAGE,(0,0))
    if PLAYER:
        DISPLAYSURF.blit(PLAYER,(player.pos[0]*TILESIZE,+player.pos[1]*TILESIZE))
   
    pygame.display.update()
    
    
def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
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
    loadNewLevel('testMap')
    while True:
        processCommands() 
        updateScreen()   
          
def startScreen():
        DISPLAYSURF.blit(BACKGROUND_IMAGE,(0,0))
        while True:
            button("Login",195,105,160,40,COLOR['white'],COLOR['grey'],runGame)
            button("New User",195,190,160,40,COLOR['white'],COLOR['grey'],runGame)
            pygame.display.update()
            event = pygame.event.wait()
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        
sys.exit(startScreen())

    
               