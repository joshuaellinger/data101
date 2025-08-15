# Simple pygame programs

import pygame
from pygame.locals import *
import time

from ui_label import Label

SCREEN_SIZE=(1024,650)

BLUE = (0, 0, 255)


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

    fonts = pygame.font.get_fonts()

    rect1=Label("monster 1",(30,30,250,590))
    rect2=Label("monster 2",(744,30,250,590))
    rect3=Label("fight log",(310,180,404,350))
    rect4=Label("auto or on-click",(310,180,404,350))
    running = True
    background = GRAY
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        screen.fill(background)

        rect1.blit(screen)
        rect2.blit(screen)
        rect3.blit(screen)
        
        pygame.display.update()

    pygame.quit()    

def screen_fight():
    draw_text()
    
if __name__ == "__main__":
    screen_fight()