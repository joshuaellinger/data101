# UI_Button is a simple button implemented as a wrapper around UI_Text with a few extra features.
#
#    1. It defaults to having border
#    2. It has its own default colors (above)
#    3. It has a special click handler to transitions aren't instant.
#    4. It can be disabled.
#
#  When clicked, the button is temporarily disabled for 10 tlicks
#  before the handler is envoked.

import pygame
from typing import Tuple

from .ui_color import *

from .ui_text import UI_Text
from .ui_element import UI_Element, UI_EventHandler, NoOp_EventHandler
from .ui_helpers import TextAlignment, create_surface, render_text, render_border, Background


class UI_Button(UI_Text):
    "A simple button"
    def __init__(self, id: str, rect: pygame.Rect, text: str, *, 
                 alignment = TextAlignment.Center,
                 border = 2, padding = 10,
                 color: pygame.Color = BUTTON_TEXT,  
                 border_color: pygame.Color = BUTTON_BORDER,
                 background: Background = BUTTON_BACKGROUND,  
                 ):
        
        super().__init__(id, rect, text=text, 
                         alignment=alignment, padding=padding,
                         border=border, border_color=border_color,
                         color=color, background=background)

        self._enabled = True

        # wait 10 ticks before invoking onclick handler
        self._counter = 0
        def debounce_handler(x: UI_Element):
            if self._counter == 0 and self._enabled:
                self._counter = 10
                self._changed = True
        self._onclick = debounce_handler
        self._onclick_external: UI_EventHandler = NoOp_EventHandler

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

        # draw differently if disabled or pending click event
        if not self._enabled or self._counter > 0:
            c, bg, b = BUTTON_TEXT_DISABLED, BUTTON_BACKGROUND_DISABLED, BUTTON_BORDER_DISABLED
        else:
            c, bg, b = self._color, self._background, BUTTON_HOVER if self._hover else self._border_color

        image = create_surface(self._rect.width, self._rect.height, bg)
        self._text_width, self._text_height = render_text(image, self._text, c, alignment=self._alignment, padding=self._padding)
        render_border(image, self._border, b)

        screen.blit(image, self._rect.topleft)
        self._changed = False

