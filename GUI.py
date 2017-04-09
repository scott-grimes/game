import pygame

class float_message():
    def __init__(self,text,location):
        #flots the message Text over the character's head
        self.location = location
        
        pass
    
class chat_window():
    def __init__(self):
        self.window_state = 'chat'
        self.rect = (100,100,300,300)
        self.color = (0,0,0)
    def toggle_chat(self):
        pass
    
    def toggle_log(self):
        pass
    
    def update_size(self,width,height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = height*.8
        
     
def text_objects(text, font,color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,screen,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))
    color = (0,0,0)
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText,color)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)