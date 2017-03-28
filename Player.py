import pygame
from locals import *
class Player:
    def __init__(self, fromDB = None):
        #load a player from the database
        if fromDB is None:
            self.name = 'bob'
            self.gold = 0
            self.health = 10
            self.maxHealth = 10
            self.inventory = []
            self.image = 'data/images/player.png'
            self.speed = 50 #miliseconds delay while walking
            self.pos = [25,25]
            self.level = 'levelName'
        
        #construct a new player
        else:
            self.name = fromDB.name
            self.gold = fromDB.gold
            self.health = fromDB.health
            self.maxHealth = fromDB.maxHealth
            self.inventory = fromDB.inventory
            self.image = fromDB.inventory 
            self.speed = fromDB.speed
            self.pos = fromDB.pos
            self.level = fromDB.pos
        
        #initalize final elements    
        self.facing = 'up'
        self.lastMove = 0.0
        self.movementDelay = 100
        
    
    def wouldCollide(self,position,collisions):
        #returns true if a given movement would cause a collision with "collision" matrix
        #collision is a matrix which contains the tiles the user is not allowed to stand on
        collisionRects = []
        position = (position[0]*TILESIZE,position[1]*TILESIZE)
        for y, row in enumerate(collisions):
            for x, ele in enumerate(row):
                if(ele is 1):
                    collisionRects.append(pygame.Rect(x*TILESIZE,y*TILESIZE,TILESIZE,TILESIZE))
        playerRect = pygame.Rect(position,(TILESIZE,TILESIZE))      
        
        if len(playerRect.collidelistall(collisionRects)) is 0:
            return False
        return True
    
    def newPosition(self,current,direction):
        #returns what the users new position would be if they moved in "direction"
        answer = [i for i in current]
        if(direction == 'right'):
            answer[0]+=MOVEMENT_DISTANCE
                    
        if(direction =='left'):
            answer[0]-=MOVEMENT_DISTANCE
                    
        if(direction == 'up'):
            answer[1]-=MOVEMENT_DISTANCE
                    
        if(direction == 'down'):
            answer[1]+=MOVEMENT_DISTANCE
        return answer
      
    def face(self,movement_wanted):
        #movement wanted is an array of booleans [w,s,a,d] for direction arrow pressed
        face = 'down'
        if(movement_wanted[3]):
            face = 'right'
        if(movement_wanted[2]):
            face = 'left'
        if(movement_wanted[0]):
            face = 'up'
        if(movement_wanted[1]):
            face = 'down'
        self.facing = face
    
    def getImage(self):
        #returns the image of the user based on the direction
        return self.image
        