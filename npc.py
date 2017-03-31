import pygame
from spritesheet import spritesheet
from locals import *
class NPC(pygame.sprite.Sprite):
    
    def __init__(self,id,name,position,roamArea,spriteimage,maxhealth,aggro):
        #aggro -1, not attackable
        #aggro 0, attackable but not aggressive
        #aggro 1, attackable and aggressive 
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.name = name
        self.position = position
        self.image = image
        self.maxhealth = maxhealth
        self.hp = self.maxhealth
        self.aggro = aggro
        
    def die(self):
        #sends a message to the server to drop loot
        #gives user experience
        pass
    
    def click(self,mouse_button):
        #what happens when I click left or right?
        pass