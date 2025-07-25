# Simple pygame programs

import pygame
from pygame.locals import *
import time


def draw_a_circle():
    print("example #2: draw a circle")
    # example from https://realpython.com/pygame-a-primer/#basic-pygame-program

    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode([500, 500])

    # Run until the user asks to quit
    running = True
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white
        screen.fill((255, 255, 255))

        # Draw a solid blue circle in the center
        pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()

def draw_text():
    print("example #2: draw text")
 
    # example from https://pygame.readthedocs.io/en/latest/4_text/text.html

    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GRAY = (200, 200, 200)

    pygame.init()
    screen = pygame.display.set_mode((640, 240))

    sysfont = pygame.font.get_default_font()
    print('system font :', sysfont)

    t0 = time.time()
    font = pygame.font.SysFont(None, 48)
    print('time needed for Font creation :', time.time()-t0)

    img = font.render(sysfont, True, RED)
    rect = img.get_rect()
    pygame.draw.rect(img, BLUE, rect, 1)

    font1 = pygame.font.SysFont('chalkduster.ttf', 72)
    img1 = font1.render('chalkduster.ttf', True, BLUE)

    font2 = pygame.font.SysFont('didot.ttc', 72)
    img2 = font2.render('didot.ttc', True, GREEN)

    fonts = pygame.font.get_fonts()
    print(len(fonts))
    for i in range(7):
        print(fonts[i])

    running = True
    background = GRAY
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        screen.fill(background)
        screen.blit(img, (20, 20))
        screen.blit(img1, (20, 50))
        screen.blit(img2, (20, 120))
        pygame.display.update()

    pygame.quit()    


def main():
    draw_a_circle()
    draw_text()


main()