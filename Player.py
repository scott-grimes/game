import pygame
from locals import *
class Player(pygame.sprite.Sprite):
    def __init__(self, fromDB = None):
        #load a player from the database
        pygame.sprite.Sprite.__init__(self)
        if fromDB is None:
            self.name = 'bob'
            self.gold = 0
            self.health = 10
            self.maxHealth = 10
            self.inventory = []
            self.image = 'data/images/player.png'
            self.position = [0, 0]
            self.zone = 'testZone'
        
        #construct a new player
        else:
            self.name = fromDB.name
            self.gold = fromDB.gold
            self.health = fromDB.health
            self.maxHealth = fromDB.maxHealth
            self.inventory = fromDB.inventory
            self.image = fromDB.inventory 
            self.speed = fromDB.speed
            self.position = fromDB.position
            self.level = fromDB.level
            self.zone = fromDB.zone
        self.image = pygame.image.load('data/images/player.png').convert_alpha()
        
        #initalize final elements    
        self.facing = 'up'
        self.velocity = [0,0]
        self.old_position = self.position
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width * .5, 8)

        
    
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
    
    def changeVelocity(self,direction):
       
        if(direction == 'right'):
            self.position[0]+=HERO_MOVE_SPEED
                    
        if(direction =='left'):
            self.position[0]-=HERO_MOVE_SPEED
                    
        if(direction == 'up'):
            self.position[1]-=HERO_MOVE_SPEED
                    
        if(direction == 'down'):
            self.position[1]+=HERO_MOVE_SPEED
       
      
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
        
    def position(self):
        return list(self.position)

    def position(self, value):
        self.position = list(value)
    def update(self, dt):
        self.old_position = self.position[:]
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
    
    def move_back(self, dt):
        """ If called after an update, the sprite can move back to give the
            illusion of the sprite not moving.
        """
        self.position = self.oldposition
        self.rect.topleft = self.position
        