import pygame
from spritesheet import spritesheet
from locals import *
class Player(pygame.sprite.Sprite):
    
    def tileToCoord(self,xy):
        "Convert tile coord to pixel coordinates."
        return [xy[0]*TILESIZE, xy[1]*TILESIZE]
    
    def coordToTile(self,xy):
        "Convert a pixel coord into the tile position."
        return [xy[0]/TILESIZE, xy[1]/TILESIZE]
    
    def __init__(self, fromDB = None):
        #load a player from the database
        pygame.sprite.Sprite.__init__(self)
        self.name = 'bob'
        self.gold = 0
        self.health = 10
        self.maxHealth = 10
        self.inventory = []
        self.spriteSheet = spritesheet('data/images/LPC Base Assets/sprites/people/soldier.png')
        self.tilePos = [25,21]
        self.zone = 'mapWithCollisions'
        self.facing = 'down'
        self.speed = 200 #can move one tile every this many miliseconds 
        
        self.Animate = False
        self.updateImage()
        transColor = self.image.get_at((0,0))
        self.image.set_colorkey(transColor)
        #initalize final elements    
        self.position = self.tileToCoord(self.tilePos)
        self.rect = self.image.get_rect()
        self.lastMove = 0
        
        #self.feet = pygame.Rect(0, 0, self.rect.width, self.rect.height * .5)
        #self.feet.midbottom = self.rect.midbottom
        
    def animate(self):
        #loads self.walk_animation based on the direction the user is moving
        #count is used to iterate through the animation images on the spritesheet
        #self.Animate is True when we want to animate, otherwise a still image is displayed
        self.Animate = True
        self.count = 0
        self.image = self.spriteSheet.image_at((0,spriteDirectionDict[self.facing],PLAYER_IMAGE_SIZE[0],PLAYER_IMAGE_SIZE[1]))
        self.walk_animation = self.spriteSheet.load_strip((0,spriteDirectionDict[self.facing],PLAYER_IMAGE_SIZE[0],PLAYER_IMAGE_SIZE[1]),9)
        pass
        
    def updateImage(self):
        #if user is walking, Animate is True, we will flip through images in our spritesheet
        if(self.Animate):
            self.image = self.walk_animation[self.count]
            self.count+=1
            if(self.count>8):
                self.count = 0
                self.Animate = False
            pass
        else:
        #user is not moving, display only the still image of the user
            self.image = self.spriteSheet.image_at((0,spriteDirectionDict[self.facing],PLAYER_IMAGE_SIZE[0],PLAYER_IMAGE_SIZE[1]))
        
   
    def face(self,movement_wanted):
        #movement wanted is an array of booleans [w,s,a,d] for direction arrow pressed
        face = 'down'
        if(movement_wanted[0]):
            face = 'up'
        if(movement_wanted[3]):
            face = 'right'
        if(movement_wanted[2]):
            face = 'left'
        if(movement_wanted[1]):
            face = 'down'
        self.facing = face
        self.updateImage()
        
    def position(self):
        return list(self.position)

    def position(self, value):
        self.position = list(value)
        
    def collisionRect(self,tilePosition):
        #returns the collision Rect centered horizontally on our character
        #and alligned to the bottom
        newCoord = self.tileToCoord(tilePosition)
        return pygame.Rect(newCoord[0]+16, newCoord[1]+32, self.rect.width*.5, self.rect.height * .5)
        
    def update(self, dt):
        self.position = self.tileToCoord(self.tilePos)
        self.rect.topleft = self.position
        #self.feet.midbottom = self.rect.midbottom
    
    def head_towards(self, move):
        """ 
        returns the feet rect in which the player would stand if they 
        headed in direction "move"
        """
        newPos = self.tilePos[:]
       
        if move == 'up':
            newPos[1]-=1
        if move == 'down':
            newPos[1]+=1
        if move == 'right':
            newPos[0]+=1
        if move == 'left':
            newPos[0]-=1
        collisionRect = self.collisionRect(newPos)
        return newPos , collisionRect
        
        