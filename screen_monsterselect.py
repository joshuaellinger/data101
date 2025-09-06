# Simple pygame programs

import pygame
from pygame.locals import *
import time

BLUE = (0, 0, 255)

from ui_label import Label, is_point_in_rect
monsters=[]

def select_monster(pos):
    for rows in monsters:
        for m in rows:
            if is_point_in_rect(pos,m.loc):
                return m
    return None

def draw_text(is_started):
    #print("example #2: draw text")
 
    # example from https://pygame.readthedocs.io/en/latest/4_text/text.html

    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GRAY = (200, 200, 200)
    #if not is_started:
    pygame.init()
    screen = pygame.display.set_mode((1024, 650))

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
    for row in range(4):
            monster_row=[]
            for col in range(4):
                x=Label(f"m{row}{col}",(500+col*125,87.5+row*125,100,100))
                monster_row.append(x)
            monsters.append(monster_row)
    running = True
    background = GRAY
    monster_one=None
    monster_two=None
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == MOUSEBUTTONDOWN: 
                m=select_monster(event.pos)
                if m!=None:
                    if monster_one==None:
                        print("selected "+m.msg)
                        monster_one=m
                    else:
                        print("monster_two is "+m.msg)
                        monster_two=m
                        running = False

            #elif event.type==KEYDOWN:
                #text_box.add('abcdefg')

        screen.fill(background)
        for row in range(4):
            for col in range(4):
                monsters[row][col].blit(screen)
        
        pygame.display.update()

    pygame.quit()    





def screen_monsterselect(is_started):
    draw_text(is_started)
    
if __name__ =="__main__":
    screen_monsterselect()