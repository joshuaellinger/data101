# Simple pygame programs

import pygame
from pygame.locals import *
import time

from ui_label import Label,is_point_in_rectangle

SCREEN_SIZE=(1024,650)

BLUE = (0, 0, 255)


def draw_text(is_started):
    #print("example #2: draw text")
 
    # example from https://pygame.readthedocs.io/en/latest/4_text/text.html

    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GRAY = (200, 200, 200)

    #if is_started == False:
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
    rect4=Label("     auto",(310,550,187,70))
    label_result=Label("    result",(527,550,187,70))
    #rect5=Label("Monster Mash!!!",(30,150,404,150))
    #print(label_result.loc)
    running = True
    background = GRAY
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                if is_point_in_rectangle(event.pos,label_result.loc):
                    running = False
                #print(event.pos)

        screen.fill(background)

        rect1.blit(screen)
        rect2.blit(screen)
        rect3.blit(screen)
        rect4.blit(screen)
        label_result.blit(screen)
        #rect5.blit(screen)

        
        pygame.display.update()

    pygame.quit()    

def screen_fight(is_started):
    draw_text(is_started)
    
if __name__ == "__main__":
    screen_fight(False)