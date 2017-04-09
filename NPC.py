from Character  import *

class NPC(Character):
    def __init__(self, id):
        npc_data = NPCS[id]
        self.name = npc_data[0]
        spriteSheetLocation = npc_data[1]
        self.character_image_size = npc_data[2]
        self.num_animations = npc_data[3]
        self.aggro = npc_data[4]
        self.aggroDistance = npc_data[5]
        self.speed = npc_data[6]
        self.inventory = []
        self.spriteSheet = spritesheet(spriteSheetLocation)
        self.tilePos = [15,23]
        self.facing = 'down'
        super(NPC, self).__init__()  