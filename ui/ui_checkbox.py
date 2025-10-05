# UI_Checkbox is a simple checkbox implemented as a wrapper around UI_Text 
#   with an extra icon in front and code to track check status
# 

import pygame
from typing import Tuple

from .ui_color import *

from .ui_text import UI_Text
from .ui_element import UI_Element, UI_EventHandler, NoOp_EventHandler
from .ui_helpers import TextAlignment, create_surface, render_text, render_border, Background


class UI_Checkbox(UI_Text):
    "A simple checkbox"
    def __init__(self, id: str, rect: pygame.Rect, text: str, *, 
                 border = 0, padding = 10, checked=False,
                 color: pygame.Color = BUTTON_TEXT,  
                 border_color: pygame.Color = BUTTON_BORDER,
                 background: Background = BUTTON_BACKGROUND,  
                 set_color: pygame.Color = CHECKMARK_SET_COLOR,
                 clear_color: pygame.Color = CHECKMARK_CLEAR_COLOR,
                 ):
        
        super().__init__(id, rect, text=text, 
                         alignment=TextAlignment.Left, padding=padding,
                         border=border, border_color=border_color,
                         color=color, background=background)

        self._enabled = True
        self._checked = checked

        self.set_color = set_color
        self.clear_color = clear_color

        # wait 10 ticks before invoking onclick handler
        self._counter = 0
        def debounce_handler(event: pygame.event.Event):
            if self._counter == 0 and self._enabled:
                self._counter = 10
                self._changed = True
        self._onclick = debounce_handler
        self._onchange_external: UI_EventHandler = NoOp_EventHandler

        def hover_handler(event: pygame.event.Event):
            self._changed = True
        self._onenter = hover_handler
        self._onexit = hover_handler

    @property
    def enabled(self) -> bool:
        return self._enabled
    @enabled.setter
    def enabled(self, val: bool):
        if self._enabled == val: return 
        self._enabled = val
        self._changed = True

    @property
    def checked(self) -> bool:
        return self._checked
    @checked.setter
    def checked(self, val: bool):
        if self._checked == val: return 
        self._checked = val
        self._changed = True
        self._onchange_external(self)
                
    @property
    def onchange(self) -> UI_EventHandler:
        return self._onchange_external
    @onchange.setter
    def onchange(self, val: UI_EventHandler):
        self._onchange_external = val

    def tick(self):
        # count down the cycles before calling onchange handler
        # if triggered from UI
        if self._counter > 0:
            self._counter -= 1
            if self._counter == 0:
                self._checked = not self._checked
                self._onchange_external(self)
                self._changed = True

    def update(self, screen: pygame.Surface):
        if not self._changed: return

        # draw differently if disabled or pending click event
        if not self._enabled or self._counter > 0:
            c, bg, b = BUTTON_TEXT_DISABLED, BUTTON_BACKGROUND_DISABLED, BUTTON_BORDER_DISABLED
        else:
            c, bg, b = self._color, self._background, BUTTON_HOVER if self._hover else self._border_color

        image = create_surface(self._rect.width, self._rect.height, bg)

        # draw checkbox
        x = max(min(self._rect.width, self._rect.height), 10) - 2 * self.padding
        rect = pygame.Rect(self.padding, self.padding, x, x)
        subimage = image.subsurface(rect)
        m = self.set_color if self._checked else self.clear_color
        if self.checked: subimage.fill(m)
        pygame.draw.rect(subimage, b, subimage.get_rect(), width=2)
    

        # draw text with offset
        rect = pygame.Rect(x + self.padding, 0, self._rect.width - x - self.padding, self._rect.height)
        subimage = image.subsurface(rect)
        self._text_width, self._text_height = render_text(subimage, self._text, c, alignment=self._alignment, padding=self._padding)
        
        render_border(image, self._border, b)

        screen.blit(image, self._rect.topleft)
        self._changed = False

