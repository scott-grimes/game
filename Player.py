from Character  import *

class Player(Character):
    def __init__(self):
        self.name = 'bob'
        self.gold = 0
        self.health = 10
        self.maxHealth = 10
        self.inventory = []
        self.character_image_size = [64,64]
        self.num_animations = 9
        self.spriteSheet = spritesheet('data/images/LPC Base Assets/sprites/people/soldier.png')
        self.tilePos = [25,21]
        self.zone = 'mapWithCollisions'
        self.facing = 'down'
        self.speed = 400 #can move one tile every this many miliseconds 
        
        super(Player, self).__init__()    