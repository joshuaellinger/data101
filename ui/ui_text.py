# UI_Text supports drawing text into a rectangle, with an optional border
# 
# It supports text alignment (default left) and padding around the text (default 10)
# It does not resize based on the size of the text.  It does not change appearance
# based on hover and ignores click events by default.
#
# It has a read-only property that tells you the size of the text after it is first rendered
# 
import pygame
from pygame.locals import *

from typing import Callable, Tuple
from abc import ABC, abstractmethod
from enum import Enum 

from .ui_color import *

from .ui_element import UI_Element
from .ui_helpers import TextAlignment, create_surface, render_text, render_border, Background

class UI_Text(UI_Element):
    def __init__(self, id: str, rect: pygame.Rect, *, 
                 text="", alignment = TextAlignment.Left,
                 border = 0, padding = 10,
                 border_color: pygame.Color = BLUE,
                 color: pygame.Color = BLUE,  
                 background: Background = DARK_GRAY
                 ):
        super().__init__(id, rect, 
                         border=border, border_color=border_color,
                         color=color, background=background)

        self._text = text
        self._alignment = alignment
        self._padding = padding
        self._changed = True

    @property
    def text(self) -> str:
        return self._text
    @text.setter
    def text(self, value: str):
        if value == self._text: return
        self._text = value
        self._changed = True    

    @property
    def padding(self) -> int:
        return self._padding
    @padding.setter
    def padding(self, value: int):
        if value == self._padding: return
        self._padding = value
        self._changed = True    

    @property
    def alignment(self) -> TextAlignment:
        return self._alignment
    @alignment.setter
    def alignment(self, value: TextAlignment):
        if value == self._alignment: return
        self._alignment = value
        self._changed = True    

    def update(self, screen: pygame.Surface):
        if not self._changed: return

        surface = create_surface(self.rect.width, self.rect.height, self.background)
        render_text(surface, self.text, self.color,
             alignment=self._alignment, padding=self.padding)
        render_border(surface, self.border, self.border_color)

        screen.blit(surface, self.rect.topleft)
        self._changed = False
    
