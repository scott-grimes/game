import pygame, sys, datetime, pytmx, pyscroll
from Character import *
from pygame.locals import *
from pygame.colordict import THECOLORS as COLOR
from locals import *
from GameState import GameState
import pyscroll.data
from pyscroll.group import PyscrollGroup

# screen resize
def init_screen(width, height):
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    return screen

#wrapper to get map with path name and extention
def get_map(mapName):
    return 'data/zones/'+mapName+'.tmx'

   

class MainGame(object):
    
    def __init__(self):
        #true while running
        self.running = False
        
        #creat player, load zone the player is in
        self.player = Player()
        self.load_zone(self.player.zone)
        
        # add player to the group of sprites
        self.group.add(self.player)
        self.enemy = NPC('0001')
        self.group.add(self.enemy)
        
    
    def rightClickMenu(self):
        print(pygame.mouse.get_pos())
    
    def draw(self, surface):
        # center the screen on the player
        self.group.center(self.player.rect.center)

        # draw everything
        self.group.draw(surface)  
        
        
    def handle_input(self):
        
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                init_screen(event.w, event.h)
                self.map_layer.set_size((event.w, event.h))
        if(pygame.mouse.get_pressed()[2]):
            self.rightClickMenu()
        #get all the keys which are pressed
        keys = pygame.key.get_pressed()
        
        #if a key is pressed...
        if (sum(keys)>0): 
            
            #array of booleans representing movement keys pressed [W,S,A,D]
            movement_wanted = [keys[a] for a in movementKeys]
            
            #array of strings indicating pressed keys ['up','down','left','right']
            directions = [directionDict[i] for i, x in enumerate(movement_wanted) if x]
            
            self.moveCharacter(self.player,directions)
                
                
    def moveCharacter(self,character,directions):
        #if character can move in the directions indicated, update the characters position
        
        if(len(directions)>0):
            character.face(directions)
            currentTime = pygame.time.get_ticks()
            if(currentTime>character.lastMove+character.speed):
                
                for move in directions:
                            new_tile,new_rect = character.head_towards(move)
                            if(new_rect.collidelist(self.collisions) == -1):
                                character.tilePos = new_tile[:]
                character.animate()
                character.lastMove = currentTime
        
            
    def load_zone(self, zoneName):
            
            mapfile = get_map(zoneName)
            tmx_data = pytmx.util_pygame.load_pygame(mapfile)
            map_data = pyscroll.data.TiledMapData(tmx_data)
            self.collisions = []
            for object in tmx_data.objects:
                self.collisions.append(pygame.Rect(
                    object.x, object.y,
                    object.width, object.height))

            # create camera (aka renderer)
            self.map_layer = pyscroll.BufferedRenderer(map_data, screen.get_size(), clamp_camera=True)
            
            
        
            # pyscroll supports layered rendering.  our map has 3 'under' layers
            # layers begin with 0, so the layers are 0, 1, and 2.
            # since we want the sprite to be on top of layer 1, we set the default
            # layer for sprites as 2
            self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=2)
            
                
    def moveNPCs(self,dt):
        for char in self.group:
                if char is not self.player:
                    #set aggro targets if there are none
                    distance = char.distance(self.player)
                    if(char.target is None and distance<char.aggroDistance):
                        char.target = self.player
                        
                    #move NPC if nessesary   
                    if(char.target is not None):
                        #find distance to aggro target
                        distance = char.distance(char.target)
                        if(distance>1):
                            directions = char.directionTowards(char.target)
                            self.moveCharacter(char,directions)
                            
        pass
    
    
    def update(self,dt):
        self.group.update(dt)
        self.moveNPCs(dt)
          
    
                
    def run(self):
        clock = pygame.time.Clock()
        self.running = True

        from collections import deque
        times = deque(maxlen=30)

        try:
            while self.running:
                dt = clock.tick(120) / 1000.
                times.append(clock.get_fps())
                #print(sum(times) / len(times))
                self.handle_input()
                self.update(dt)
                self.draw(screen)
                pygame.display.flip()

        except KeyboardInterrupt:
            self.running = False
        

     
def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)
    
def runGame():
    try:
        game = MainGame()
        game.run()
    except:
        pygame.quit()
        raise
    
          
def startScreen():
        BACKGROUND_IMAGE = pygame.image.load('data/images/loginScreen.png')
        screen.blit(BACKGROUND_IMAGE,(0,0))
        while True:
            button("Login",195,105,160,40,COLOR['white'],COLOR['grey'],runGame)
            button("New User",195,190,160,40,COLOR['white'],COLOR['grey'],runGame)
            pygame.display.update()
            event = pygame.event.wait()
            if event.type==QUIT:
                pygame.quit()
                sys.exit()




if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('MVMMORPG')
    screen = init_screen(800, 600)

    try:
        startScreen()
    except:
        pygame.quit()
        raise
    
               