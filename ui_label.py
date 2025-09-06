import pygame
from pygame.locals import *
import time

DARK_GRAY = (150, 150, 150)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

class Label:
    def __init__(self,msg:str,loc):


        #pass in how tall the screen is
        #add lines of text til screen is full, scroll only when screen is full
       
        self.msg=msg
        self.loc=loc
        self.font = pygame.font.SysFont(None, 48)
        #
        self.image=pygame.Surface((loc[2],loc[3]))
        self.image.fill(DARK_GRAY)
        txt_image = self.font.render(msg,True, BLUE)
        self.image.blit(txt_image,(10,10))

    def blit(self,screen):
        screen.blit(self.image,self.loc)
