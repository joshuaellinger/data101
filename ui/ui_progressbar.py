# UI_Progress bar draws a a progress bar (either horizontal or vertical)
#
# It has a current value and a maximum which control how full it is. 
#
import pygame
from pygame.locals import *

from typing import Callable, Tuple
from abc import ABC, abstractmethod
from enum import Enum 

from .ui_color import *

from .ui_element import UI_Element
from .ui_helpers import create_surface, render_border, Background

class Orientation(Enum):
    Horizontal = 1,
    Vertical = 2


class UI_ProgressBar(UI_Element):
    def __init__(self, id: str, rect: pygame.Rect, *,
                 current = 0, maximum = 100, orientation = Orientation.Horizontal,
                 color: pygame.Color = BLUE,  
                 border: int = 0,
                 border_color: pygame.Color = BLUE,
                 background: Background = DARK_GRAY,  
                 ):
        super().__init__(id, rect, border=border, border_color=border_color,
                         background=background)

        self._current = current
        self._maximum = maximum
        self._orientation = orientation

        self._color = color
        self._changed = True

    @property
    def current(self) -> int:
        "current position, must be between 0 and maximum"
        return self._current
    @current.setter
    def current(self, value: int):
        if value > self._maximum: value = self._maximum
        if value < 0: value = 0
        if value == self._current: return
        self._current = value
        self._changed = True

    @property
    def percentage(self) -> float:
        "percentage full (0 to 1)"
        return self._current/self._maximum

    @property
    def maximum(self) -> int:
        "maximum position, must be positive"
        return self._maximum
    @current.setter
    def maximum(self, value: int):
        if value == self._maximum: return
        if value <= 0:
            raise Exception("maximum must be positive") 
        self._maximum = value
        if self._current > self._maximum:
            self._current = self._maximum
        self._changed = True    

    @property
    def orientation(self) -> Orientation:
        return self._orientation
    @orientation.setter
    def oriention(self, value: Orientation):
        if value == self._orientation: return
        self._orientation = value
        self._changed = True    

    @property
    def color(self) -> int:
        return self._color
    @color.setter
    def color(self, value: pygame.Color):
        if value == self._color: return
        self._color = value
        self._changed = True    

    # ----

    def render(self) -> pygame.Surface:

        img = create_surface(self.rect.width, self.rect.height, self.background)

        if self.orientation == Orientation.Horizontal:
            w = (self._current / self._maximum) * self.rect.width
            rect = pygame.Rect(0, 0, w, self.rect.height)
        elif self.orientation == Orientation.Vertical:
            h = (1.0-self._current / self._maximum) * self.rect.height
            rect = pygame.Rect(0, h, self.rect.width, self.rect.height-h)
        else:
            raise Exception(f"Invalid Orientation: {self.orientation}")
        img.fill(self.color, rect)

        render_border(img, self.border, self.border_color)
        return img

    def update(self, screen: pygame.Surface):
        if not self._changed: return

        image = self.render()
        screen.blit(image, self.rect.topleft)

        self._changed = False

