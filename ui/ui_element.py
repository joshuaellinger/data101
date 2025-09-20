# UI_Element is a base class for display elements on a pygame screen 
# 
# It supports 
#    1. support hovering
#    2. support clicking
#    3. have an identifier, a way to identify multiple elements of a given type.
#    4. a rectangle where it should be drawn
#    5. a foreground color, background color, border width, and border_color
#    6. a changed flag that indicates that the item needs to be redrawn. 
#
#  If any of the properties (like color) are modified, changed is set to true
#  as a side-effect. Derived classes are expected to update changed and clear
#  it after drawing the element.
# 
#  The update/process/tick method mirror the method on the view (see UI_View)
#
#  The default event handler (process) handles mouse enter/exit events 
#  and click events.  The default draw routine draws light red placeholder
#  with the name of the component.  

import pygame
from pygame.locals import *

from typing import Callable, Tuple
from abc import ABC, abstractmethod
from enum import Enum 

from .ui_color import *
from .ui_helpers import TextAlignment, create_surface, render_text, render_border, Background

# event handlers are functions that receive an event for processing
# NoOp is shorthand for "No Operation"
UI_EventHandler = Callable[[pygame.event.Event], None]
def NoOp_EventHandler(event: pygame.event.Event):
    pass


class UI_Element(ABC):
    "a simple UI element that supports click and hover and borders"     
    def __init__(self, id: str, rect: pygame.Rect, *,
                 border: int, border_color: pygame.Color = BLACK,
                 color: pygame.Color = BLACK, 
                 background: Background = DARK_GRAY):
        
        self._id = id
        self._rect = pygame.Rect(rect)
        self._hover = False
        self._changed = True

        self._border = border
        self._border_color = border_color
        self._color = color
        self._background = background

        # set up the 'do nothing' event handlers
        self._onclick: UI_EventHandler = NoOp_EventHandler
        self._onenter: UI_EventHandler = NoOp_EventHandler
        self._onexit: UI_EventHandler = NoOp_EventHandler

    # make the identifer read only 
    @property
    def id(self) -> str:
        return self._id

    # --- properties that trigger redraw ----

    @property
    def rect(self) -> pygame.Rect:
        "the location/size of the element, can be a tuple or a pygame.Rect"
        return self._rect
    @rect.setter
    def rect(self, value: pygame.Rect):
        if type(value) == tuple: value = pygame.Rect(value)
        if value == self._rect: return
        self._rect = value
        self._changed = True    

    @property
    def border(self) -> int:
        "border width in pixels"
        return self._border
    @border.setter
    def border(self, value: int):
        if value == self._border: return
        self._border = value
        self._changed = True    

    @property
    def border_color(self) -> pygame.Color:
        return self._border_color
    @border_color.setter
    def border_color(self, value: pygame.Color):
        if value == self._border_color: return
        self._border_color = value
        self._changed = True    

    @property
    def color(self) -> int:
        "foreground color to text"
        return self._color
    @color.setter
    def color(self, value: pygame.Color):
        if value == self._color: return
        self._color = value
        self._changed = True    

    @property
    def background(self) -> Background:
        "background color/image"
        return self._background
    @background.setter
    def background(self, value: Background):
        if value == self._background: return
        self._background = value
        self._changed = True

    @property
    def changed(self) -> bool:
        "True if changed since last draw"
        return self._changed

    # --- event handlers ---

    @property
    def onclick(self) -> UI_EventHandler:
        "event handler called when user clicks on element"
        return self._onclick
    @onclick.setter
    def onclick(self, val: UI_EventHandler):
        self._onclick = val

    @property
    def onenter(self) -> UI_EventHandler:
        "event handler called when mouse moves over element"
        return self._onenter
    @onenter.setter
    def onenter(self, val: UI_EventHandler):
        self._onenter = val

    @property
    def onexit(self) -> UI_EventHandler:
        "event handler called when mouse moves out of element"
        return self._onexit
    @onclick.setter
    def onexit(self, val: UI_EventHandler):
        self._onexit = val

    # ---- utility methods -------

    def is_in(self, x: float, y: float):
        "test is (x,y) are in element"
        dx, dy = x - self._rect.left, y - self._rect.top
        return (0 <= dx <= self._rect.width) and (0 <= dy <= self._rect.height)

    # ---- methods for implementations to override -------

    def process(self, event: pygame.event.Event) -> None:
        "process events"

        # handle mouse click and mouse movement
        if event.type == MOUSEBUTTONDOWN:
            if self.is_in(*event.pos):
                self._onclick(self)
        elif event.type == MOUSEMOTION:
            if self.is_in(*event.pos):
                if not self._hover:
                    self._onenter(self)
                    self._hover = True
            else:
                if self._hover:
                    self._onexit(self)
                    self._hover = False
        
    def tick(self) -> None:
        "called per tick (typically 1/30 of a second)"
        pass

    def update(self, screen: pygame.Surface) -> None:
        "update display"

        if not self._changed: return

        img = create_surface(self._rect.width, self._rect.height, self.background)
        render_text(img, f"[{self.id}]", self.color, alignment=TextAlignment.Center, size=20)
        render_border(img, self.border, self.border_color)

        screen.blit(img, self._rect.topleft)
        self._changed = False
        
