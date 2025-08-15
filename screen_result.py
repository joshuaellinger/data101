# Simple pygame programs

import pygame
from pygame.locals import *
import time
from ui_label import Label

GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

def game_loop():
    #print("example #2: draw text")
 
    # example from https://pygame.readthedocs.io/en/latest/4_text/text.html

    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    pygame.init()
    screen = pygame.display.set_mode((1048, 1048))

    sysfont = pygame.font.get_default_font()
    #print('system font :', sysfont)

    t0 = time.time()
    #print(t0)
    font = pygame.font.SysFont(None, 48)
    #print('time needed for Font creation :', time.time()-t0)

    #font1 = pygame.font.SysFont('chalkduster.ttf', 72)
    text_box = Label('====== Monster Mash! ======',(50,50,500,100))

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

def screen_result():
    game_loop()
    
if __name__=="__main__":
    screen_result()