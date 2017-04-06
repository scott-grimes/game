import pygame
class rightClickPopup:
    def __init__(self,coord,currentTime):
        popupSurf = pygame.Surface((50, 50))
        self.top = coord[1]
        self.left = coord[0]
        options = ['Attack',
                   'Talk']
        for i in range(len(options)):
            smallText = pygame.font.SysFont("comicsansms",20)
            textSurf = smallText.render(options[i], 1, (0,0,0))
            textRect = textSurf.get_rect()
            textRect.top = self.top
            textRect.left = self.left
            self.top += pygame.font.Font.get_linesize(smallText)
            popupSurf.blit(textSurf, textRect)
        self.menu = popupSurf
        self.coord = coord
        self.openTime = currentTime #last time enter was pressed
        self.timeToWait = 300 #wait at least 1000ms before you can hit enter again
    def draw(self,screen):
        screen.blit(self.menu, self.coord)