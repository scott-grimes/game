#contains the game state of one zone in the game
#includes players, NPCS, Items, Collisions, and the background Image
#updated from the server every tick
from locals import *
class GameState:
    
    def __init__(self,name):
        self.name = name #loads the collisions and images from our zone
        zoneBackground,MAPWIDTH,MAPHEIGHT,COLLISIONS = importZone(zoneDict[name])
        self.MAPWIDTH =MAPWIDTH
        self.MAPHEIGHT = MAPHEIGHT
        self.COLLISIONS = COLLISIONS
        self.zoneBackground = zoneBackground
    