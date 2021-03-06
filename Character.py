import pygame
from spritesheet import spritesheet
from locals import *

class Character(pygame.sprite.Sprite):
    
    def distance(self,otherCharacter):
        #computes the distance between this character and some other character
        oth = otherCharacter.tilePos
        me = self.tilePos
        return round(((oth[0]-me[0])**2+(oth[1]-me[1])**2)**.5,0)
    
    def directionTowards(self,otherCharacter):
        #returns the movements required to move this character towards the 
        #other character
        oth = otherCharacter.tilePos
        me = self.tilePos
        directions = []
        if(oth[0]>me[0]):
            directions.append('right')
        if(oth[0]<me[0]):
            directions.append('left')
        if(oth[1]>me[1]):
            directions.append('down')
        if(oth[1]<me[1]):
            directions.append('up')
        return directions 
    def tileToCoord(self,xy):
        "Convert tile coord to pixel coordinates."
        return [xy[0]*TILESIZE, xy[1]*TILESIZE-self.character_image_size[1]]
    
    def coordToTile(self,xy):
        "Convert a pixel coord into the tile position."
        return [xy[0]/TILESIZE, xy[1]/TILESIZE+self.character_image_size[1]]
    
    def resetAnimationFrame(self):
        self.frame_display_length = self.speed/self.num_animations
    
    def __init__(self, fromDB = None):
        #load a player from the database
        pygame.sprite.Sprite.__init__(self)
        self.Animate = False
        self.resetAnimationFrame()
        self.updateImage()
        transColor = self.image.get_at((0,0))
        self.image.set_colorkey(transColor)
        self.position = self.tileToCoord(self.tilePos)
        self.rect = self.image.get_rect()
        
        self.target = None
        self.lastMove = 0.0
        self.movement_queue = []
        self.combat_time_delay = 1000 #miliseconds between swings
        self.combat_distance = 2 #tiles
        self.lastAttack=0.0
        self.strength = 1
        self.dexterity = 1
        self.defense = 1
        self.dead = False

    def face(self,directions):
        if('down' in directions):
            self.facing = 'down'
        elif('up' in directions):
            self.facing = 'up'
        elif('right' in directions):
            self.facing = 'right'
        elif('left' in directions):
            self.facing = 'left'
        self.updateImage()
        
    def animate(self):
        #loads self.walk_animation based on the direction the user is facing
        #count is used to iterate through the animation images on the spritesheet
        #self.Animate is True when we want to animate, otherwise a still image is displayed
        self.Animate = True
        self.count = 0
        self.walk_animation = self.spriteSheet.load_strip(
            (0,spriteDirectionDict[self.facing],
             self.character_image_size[0],self.character_image_size[1]),self.num_animations)
        
        self.resetAnimationFrame()
        
    def updateImage(self):
        #if user is walking or attacking, Animate is True, 
        #and we will flip through images in our spritesheet
        #otherwise display static pictures based on direction facing
        
        #dt is frames since last draw
        
        if(self.Animate):
            #currentTime = pygame.time.get_ticks()
            #if(currentTime>self.lastAnimationFrame+self.animation_speed):
            #self.lastAnimationFrame = currentTime
            
            self.image = self.walk_animation[self.count]
            self.count+=1
                
            if(self.count>self.num_animations-1):
                self.count = 0
                self.Animate = False
            pass
        else:
        #user is not moving, display only the still image of the user
            yval = spriteDirectionDict[self.facing]*self.character_image_size[1]
            self.image = self.spriteSheet.image_at(
                (0,yval,
                 self.character_image_size[0],self.character_image_size[1]))
        
        
    def position(self):
        return list(self.position)

    def position(self, value):
        self.position = list(value)
        
        
    def collisionRect(self,tilePosition):
        #returns the collision Rect centered horizontally on our character
        #and alligned to the bottom
        newCoord = self.tileToCoord(tilePosition)
        return pygame.Rect(newCoord[0]+self.character_image_size[0]//4, newCoord[1]+self.character_image_size[1]//2, 
                           self.rect.width*.5, self.rect.height * .5)
        
    def update(self, dt):
        #updates the position of the user based on their tile coord
        #and their collision rect
        self.frame_display_length-=dt
        if(self.Animate):
            if(self.frame_display_length<0.0):
                self.position = self.animation_positions[self.count]
                self.resetAnimationFrame()
        else:
            self.position = self.tileToCoord(self.tilePos)
        self.rect.topleft = self.position
        
    
    def headed_towards(self, move):
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
        
    
                        
    def moveCharacter(self,collisions):
        #if character can move in the directions indicated, update the characters position
        directions = self.movement_queue
      
        if(len(directions)>0): 
            self.face(directions)
            currentTime = pygame.time.get_ticks()
            if(currentTime>self.lastMove+self.speed):
                oldPosition = self.tilePos[:]
                for move in directions:
                            new_tile,new_rect = self.headed_towards(move)
                            if(new_rect.collidelist(collisions) == -1):
                                self.tilePos = new_tile[:]
                
                self.lastMove = currentTime

        
    
        
    def attack(self):
        #attempts to attack the current target
        if self.target is None:
            return
        if self.distance(self.target)>self.combat_distance:
            return
        if self.target.dead:
            self.target = None
            return
        currentTime = pygame.time.get_ticks()
        if self.lastAttack+self.combat_time_delay<currentTime:
              self.lastAttack = currentTime
              self.target.defend(self)
              
    def defend(self,otherUser):
        
        self.health-= otherUser.strength
        print('Struck for {} by {}'.format(otherUser.name,otherUser.strength))
        print('Health: {}'.format(self.health))
        if(self.health<=0):
            print('I died!')
            self.dead = True
            
            

