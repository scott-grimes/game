class npc:
    
    def __init__(self,name,position,image,health,aggro):
        #aggro -1, not attackable
        #aggro 0, attackable but not aggressive
        #aggro 1, attackable and aggressive 
        
        self.name = name
        self.position = position
        self.image = image
        self.health = health
        self.aggro = aggro
        
    def die(self):
        #sends a message to the server to drop loot
        #gives user experience
        pass
    
    def click(self,mouse_button):
        #what happens when I click left or right?
        pass