# UI_ImageButton displays an image with click handling
#

import pygame
from typing import Tuple

from .ui_color import *

from .ui_element import UI_Element, UI_EventHandler, NoOp_EventHandler
from .ui_helpers import TextAlignment, create_surface, render_text, render_border, Background


class UI_ImageButton(UI_Element):
    "A image button"
    def __init__(self, id: str, rect: pygame.Rect, *, 
                 image: Background,
                 border = 2, padding = 0,
                 border_color: pygame.Color = BUTTON_BORDER,
                 ):
        
        super().__init__(id, rect, background=image, border=border, border_color=border_color)

        self._enabled = True

        # wait 10 ticks before invoking onclick handler
        self._counter = 0
        def debounce_handler(event: pygame.event.Event):
            if self._counter == 0 and self._enabled:
                self._counter = 10
                self._changed = True
        self._onclick = debounce_handler
        self._onclick_external: UI_EventHandler = NoOp_EventHandler

    @property
    def image(self) -> Background:
        return self.background
    @image.setter
    def image(self, val: Background):
        self.background = val

    @property
    def enabled(self) -> bool:
        return self._enabled
    @enabled.setter
    def enabled(self, val: bool):
        if self._enabled == val: return 
        self._enabled = val
        self._changed = True

    @property
    def onclick(self) -> UI_EventHandler:
        return self._onclick_external
    @onclick.setter
    def onclick(self, val: UI_EventHandler):
        self._onclick_external = val

    def tick(self):
        # count down the cycles before calling onclick handler
        if self._counter > 0:
            self._counter -= 1
            if self._counter == 0:
                self._onclick_external(self)
                self._changed = True

    def update(self, screen: pygame.Surface):
        if not self._changed: return
    
        if not self._enabled or self._counter > 0:
            b = BUTTON_BORDER_DISABLED
        else:
            b = BUTTON_HOVER if self._hover else self._border_color

        image = create_surface(self._rect.width, self._rect.height, self._background)
        render_border(image, self._border, b)

        screen.blit(image, self._rect.topleft)
        self._changed = False

