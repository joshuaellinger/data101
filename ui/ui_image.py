# UI_Image displays an image.
#

import pygame
from typing import Tuple

from .ui_color import *

from .ui_element import UI_Element, UI_EventHandler, NoOp_EventHandler
from .ui_helpers import TextAlignment, create_surface, render_text, render_border, Background

class UI_Image(UI_Element):
    "A image display"
    def __init__(self, id: str, rect: pygame.Rect, *, 
                 border = 0, padding = 0,
                 image: Background = IMAGE_BACKGROUND,
                 border_color = IMAGE_BORDER
                 ):
        
        super().__init__(id, rect, background=image, border=border, border_color=border_color)

    @property
    def image(self) -> Background:
        return self.background
    @image.setter
    def image(self, val: Background):
        self.background = val

    def update(self, screen: pygame.Surface):
        if not self._changed: return
    
        image = create_surface(self._rect.width, self._rect.height, self._background)
        render_border(image, self._border, self.border_color)

        screen.blit(image, self._rect.topleft)
        self._changed = False

