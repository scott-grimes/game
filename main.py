import pygame, sys, datetime, pytmx, pyscroll, eztext
from Character import *
from Player import *
from NPC import *
from pygame.locals import *
from pygame.colordict import THECOLORS as COLOR
from locals import *
from GameState import GameState
import pyscroll.data
from pyscroll.group import PyscrollGroup
from rightClickPopup import *
from GUI import *

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
        self.chatIsOn = False
        self.rightClickMenuShowing = False
        self.txtbx = eztext.Input(maxlength=45, color=(255,0,0), prompt='{}: '.format(self.player.name))
        self.movement_queue = []
    
    def leftClick(self):
        currentTime = pygame.time.get_ticks()
        if(self.rightClickMenuShowing):
            if(currentTime>self.rightClickMenu.timeToWait+self.rightClickMenu.openTime):
                self.rightClickMenuShowing = False
                self.richtClickMenu = None
        
    def rightClick(self):
        currentTime = pygame.time.get_ticks()
        if(self.rightClickMenuShowing):
            if(currentTime>self.rightClickMenu.timeToWait+self.rightClickMenu.openTime):
                self.rightClickMenuShowing = False
                self.richtClickMenu = None
        else:
            self.rightClickMenuShowing = True
            self.rightClickMenu = rightClickPopup(pygame.mouse.get_pos(),currentTime)
            
    
    def draw(self, surface):
        # center the screen on the player
        self.group.center(self.player.rect.center)

        # draw everything
        self.group.draw(surface)  
             
    def handle_input(self):
        events = pygame.event.get()
        movement_queue = [] #list of movement keys pressed 
        for event in events:
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                init_screen(event.w, event.h)
                self.map_layer.set_size((event.w, event.h))
        #change pressed to mouse_down / up que
            if(event.type == MOUSEBUTTONUP):
                if(event.button == 1):
                    self.leftClick()
                if(event.button == 3):
                    self.rightClick()
                    pygame.KEYDOWN
            if(event.type == pygame.KEYDOWN):
                if(self.txtbx.chatActivated):
                #CHAT WINDOW TAKES KEYS
                    if(event.key==13): #enter is pressed
                        self.text_input = self.txtbx.read() #accept users input
                        print(self.text_input)
                    elif(event.key== 27): #escape was pressed while chatting
                        self.txtbx.reset() #throw out chat window
                    else:
                        self.txtbx.update(event)
                else: 
                #chat is disabled, keys go into game
                    if(event.key==13): #enter is pressed while not chatting, open chat window
                        self.txtbx.enable()
                    if(event.key in movementKeys.keys() and
                       movementKeys[event.key] not in self.player.movement_queue):
                        self.player.movement_queue.append(movementKeys[event.key])
            elif(event.type == pygame.KEYUP):
                if(event.key in movementKeys.keys() and
                   movementKeys[event.key] in self.player.movement_queue):
                    self.player.movement_queue.remove(movementKeys[event.key])
                
        if(len(self.player.movement_queue)>0):
            self.player.moveCharacter(self.collisions)

             
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
                    if(char.target is None and 
                       distance<char.aggroDistance
                       and char.aggro == 1
                       ):
                        
                        if self.player.dead is False:
                            char.target = self.player
                        
                    #move NPC if nessesary   
                    if(char.target is not None):
                        #find distance to aggro target
                        distance = char.distance(char.target)
                        if(distance>1):
                            char.movement_queue = char.directionTowards(char.target)
                            char.moveCharacter(self.collisions)
                            char.movement_queue = []
                            
        pass
    
    def runAttacks(self,dt):
        for char in self.group:
            char.attack()
    
    
    def update(self,dt):
        self.group.update(dt)
        self.moveNPCs(dt)
        self.runAttacks(dt)
          
    
    def run(self):
        clock = pygame.time.Clock()
        self.running = True

        from collections import deque
        times = deque(maxlen=30)

        try:
            while self.running:
                dt = clock.tick(120)
                times.append(clock.get_fps())
                #print(sum(times) / len(times))
                self.handle_input()
                self.update(dt)
                self.draw(screen)
                
                if(self.txtbx.chatActivated):
                    self.txtbx.draw(screen)
                    
                if(self.rightClickMenuShowing):
                    self.rightClickMenu.draw(screen)
                    
                pygame.display.flip()

        except KeyboardInterrupt:
            self.running = False
        

    
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
            button("Login",195,105,160,40,COLOR['white'],COLOR['grey'],screen,runGame)
            button("New User",195,190,160,40,COLOR['white'],COLOR['grey'],screen,runGame)
            pygame.display.update()
            event = pygame.event.wait()
            if event.type==QUIT:
                pygame.quit()
                sys.exit()




if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    pygame.key.set_repeat(100,50)
    pygame.display.set_caption('MVMMORPG')
    screen = init_screen(800, 600)

    try:
        startScreen()
    except:
        pygame.quit()
        raise
    
               