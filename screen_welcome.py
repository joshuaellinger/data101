# Simple pygame programs

import pygame
from pygame.locals import *
import time

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
    screen = pygame.display.set_mode((640, 480))

    sysfont = pygame.font.get_default_font()
    #print('system font :', sysfont)

    t0 = time.time()
    #print(t0)
    font = pygame.font.SysFont(None, 48)
    #print('time needed for Font creation :', time.time()-t0)

    #font1 = pygame.font.SysFont('chalkduster.ttf', 72)
    text_box = TextBox(['welcome!'])

    #font2 = pygame.font.SysFont('didot.ttc', 72)
    #img2 = font2.render('didot.ttc', True, GREEN)

    running = True
    background = GRAY
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type==KEYDOWN:
                text_box.add('abcdefg')

        screen.fill(background)
        text_box.blit(screen)
        pygame.display.update()

    pygame.quit()    

def main():
    draw_text()
    
main()