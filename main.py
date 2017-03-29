import pygame, sys, datetime
from Player import Player
from importExport import importGameElement, exportGameElement
from pygame.locals import *
from pygame.colordict import THECOLORS as COLOR
from locals import *
from GameState import GameState
import pytmx, pyscroll
from pytmx.util_pygame import load_pygame
import pyscroll.data
from pyscroll.group import PyscrollGroup

# wwrapper to allow screen resizing
def init_screen(width, height):
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    return screen

def get_map(fileName):
    return 'data/zones/'+fileName+'.tmx'

def coord(x,y):
        "Convert tile coord to pixel coordinates."
        return [-(x-7)*TILESIZE, -(y-7)*TILESIZE]
       


pygame.init()

class MainGame(object):
    
    def __init__(self):
        #true while running
        self.running = False
        self.player = Player()
        self.player.position = [800,700]
        #load zone map
        tmx_data = load_pygame(get_map(self.player.zone))
        
        #set up collisions
        self.walls = list()
        for object in tmx_data.objects:
            print(object)
            self.walls.append(pygame.Rect(
                object.x, object.y,
                object.width, object.height))
            

        # create new data source for pyscroll
        map_data = pyscroll.data.TiledMapData(tmx_data)
        
        # create new renderer (camera)
        self.map_layer = pyscroll.BufferedRenderer(map_data, screen.get_size(), clamp_camera=False)
        self.map_layer.zoom = 1
        
        # pyscroll supports layered rendering.  our map has 3 'under' layers
        # layers begin with 0, so the layers are 0, 1, and 2.
        # since we want the sprite to be on top of layer 1, we set the default
        # layer for sprites as 2
        self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=2)
    
        
        # add our hero to the group
        self.group.add(self.player)
    
    def draw(self, surface):

        # center the map/screen on our Hero
        self.group.center(self.player.rect.center)

        # draw the map and all sprites
        self.group.draw(surface)  
        
        
    def handle_input(self):
        # event = poll()
        # while event:
        #if event.type == QUIT:
        # self.running = False
        #break
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                init_screen(event.w, event.h)
                self.map_layer.set_size((event.w, event.h))
                
        keys = pygame.key.get_pressed()
        
        #if a key is pressed
        if (sum(keys)>0): 
            #array of booleans representing movement keys pressed [W,S,A,D]
            movement_wanted = [keys[a] for a in movementKeys]
            
            self.player.face(movement_wanted)
            #if a movement key is pressed...
            if(sum(movement_wanted)>0): 
                #if the player has not moved in "player.movementDelay"
                    
                #array of strings indicating pressed keys ['up','down','left','right']
                directions = [directionDict[i] for i, x in enumerate(movement_wanted) if x]
                
                #check each requested direction, if the user can move that way, update position
                for move in directions:
                    self.player.changeVelocity(move)
                    
                            
    def update(self,dt):
        self.group.update(dt)
        
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls)>-1:
                sprite.move_back(dt)
    
    
                
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
        

 

     

def updatePlayerImage():
    global PLAYER
    PLAYER = pygame.image.load(player.getImage()).convert_alpha()
        
 
    
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
    
               