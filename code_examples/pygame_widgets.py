# https://pygamewidgets.readthedocs.io/en/latest/

import pygame
import pygame_widgets

pygame.init()
win = pygame.display.set_mode((600, 600))
button = pygame_widgets.textbox.TextBox(win, 100, 100, 300, 150)

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    win.fill((255, 255, 255))

    # Now
    pygame_widgets.update(events)

    # Instead of
    button.listen(events)
    button.draw()

    pygame.display.update()