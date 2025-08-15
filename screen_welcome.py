# Simple pygame programs

import pygame
from pygame.locals import *
import time

from ui_label import Label

SCREEN_SIZE=(1024,650)

BLUE = (0, 0, 255)

class TextBox:
    def __init__(self,messages):

        #pass in how tall the screen is
        #add lines of text til screen is full, scroll only when screen is full
       
        self.messages=messages
        self.font = pygame.font.SysFont(None, 48)
        self.images = []
        for m in messages: 
            self.images.append(self.font.render(m,True, BLUE))

    def blit(self,screen):
        n = 0
        for x in self.images:
            screen.blit(x,(20,50+50*n))
            n=n+1
    def add(self,message):
        self.messages.pop(0)
        self.messages.append(message)
        self.images.pop(0)
        self.images.append(self.font.render(message,True, BLUE))


def draw_text():
    #print("example #2: draw text")
 
    # example from https://pygame.readthedocs.io/en/latest/4_text/text.html

    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GRAY = (200, 200, 200)

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)

    sysfont = pygame.font.get_default_font()
    #print('system font :', sysfont)

    t0 = time.time()
    #print(t0)
    font = pygame.font.SysFont(None, 48)
    #print('time needed for Font creation :', time.time()-t0)

    #font1 = pygame.font.SysFont('chalkduster.ttf', 72)

    

    #font2 = pygame.font.SysFont('didot.ttc', 72)
    #img2 = font2.render('didot.ttc', True, GREEN)

    rect1=Label("welcome!",(310,80,404,350))

    running = True
    background = GRAY
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        screen.fill(background)

        rect1.blit(screen)
        
        pygame.display.update()

    pygame.quit()    

def screen_welcome():
    draw_text()
    
if __name__ == "__main__":
    screen_welcome()