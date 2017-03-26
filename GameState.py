#contains the game state of one zone in the game
#includes players, NPCS, Items, Collisions, and the background Image
from locals import *
from importExport import importZone
class GameState:
    
    def __init__(self,name):
        self.name = name #name of the zone we are in
        image,MAPWIDTH,MAPHEIGHT,COLLISIONS = importZone(zoneDict[name])
        self.MAPWIDTH =MAPWIDTH
        self.MAPHEIGHT = MAPHEIGHT
        self.COLLISIONS = COLLISIONS
        self.image = image
        self.Players = []
        self.NPCS = []
        self.Items = []
        