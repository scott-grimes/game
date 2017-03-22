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
            self.pos = [0.0,0.0]
        
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
        
        #initalize final elements    
        self.direction = 'up'
      
      
      