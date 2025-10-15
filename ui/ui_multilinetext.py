# UI_MultLineText supports drawing multiple lines of text
# 
# It contains a list of lines to display and binds up/down arrows to scroll
# Supports font_size as a property
#

import pygame
from pygame.locals import *

from typing import Callable, Tuple, List
from abc import ABC, abstractmethod
from enum import Enum 

from .ui_color import *

from .ui_element import UI_Element
from .ui_helpers import create_surface, render_text, render_border, Background

class UI_MultiLineText(UI_Element):
    "Mult-Line Text Display with scrolling support"
    def __init__(self, id: str, rect: pygame.Rect, *, 
                 lines:List[str] = [], 
                 font_name="arial", font_size=25,
                 border = 0, padding = 2,
                 border_color: pygame.Color = BLUE,
                 color: pygame.Color = BLACK,  
                 background: Background = DARK_GRAY
                 ):
        super().__init__(id, rect, 
                         border=border, border_color=border_color,
                         color=color, background=background)

        self._lines = lines
        self._font_name = font_name
        self._font_size = font_size
        self._row_height = int(font_size * 1.2)
        self._padding = padding

        self._start_row = 0

        self._scroll_key = pygame.K_SPACE
        self._scroll_delay = 0

        self._image: pygame.Surface = None 
        self._changed = True

    def get_lines(self) -> List[str]:
        return self._lines

    def add_line(self, value: str):
        self._lines.append(value)
        self._changed = True

    def clear(self):
        self._lines.clear()
        self._start_row = 0
        self._changed = True    

    def deactivate(self):
        self._image: pygame.Surface = None 

    def show_last_row(self) -> bool:
        n = len(self._lines) - self.screen_rows
        self.start_row = n+1

    # --- properties ---

    @property
    def start_row(self) -> int:
        return self._start_row
    @start_row.setter
    def start_row(self, value: int):

        if value >= len(self._lines) - 1:
            value = len(self._lines) - 1
        if value < 0: value = 0
        
        if value == self._start_row: return

        self._start_row = value
        self._changed = True

    @property
    def font_size(self) -> int:
        return self._font_size
    @font_size.setter
    def font_size(self, value: int):
        if value == self._font_size: return
        if value < 5 or value > 50: raise Exception(f"Invalid Font-Size ({value})")
        self._font_size = value
        self._row_height = int(font_size * 0.8)
        
        self._changed = True    
        self._image: pygame.Surface = None 

    @property
    def screen_rows(self) -> int:
        offset = self._padding + self._border

        max_width = self._rect.width - 2 * offset
        max_height = self._rect.height - 2 * offset

        return (max_height // self._row_height) + 1


    @property
    def end_row(self) -> int:
        n = self._start_row + self.screen_rows
        if n > len(self._lines): n = len(self._lines) 
        return n

    @property
    def padding(self) -> int:
        return self._padding
    @padding.setter
    def padding(self, value: int):
        if value == self._padding: return
        self._padding = value
        self._changed = True    
        self._image: pygame.Surface = None 


    def render_lines(self, image: pygame.Surface):
        font = pygame.font.SysFont(self._font_name, self._font_size)

        offset = self._padding + self._border
        max_width = self._rect.width - 2 * offset
        max_height = self._rect.height - 2 * offset
        screen_rows = (max_height // self._row_height) + 1

        # -- debug ---
        def show_row_outlines():
            dest_area = (offset, offset, max_width, max_height)
            pygame.draw.rect(image, (0,200,0), dest_area, width=1)

            h = offset
            for row in range(screen_rows):
                if row == screen_rows - 1:
                    dest_area = (offset, h, max_width, max_height + offset - h )
                else:
                    dest_area = (offset, h, max_width, self._row_height)
                pygame.draw.rect(image, (200,0,0), dest_area, width=1)
                h += self._row_height
        #show_row_outlines()
        # ------------

        end_row = self._start_row + screen_rows
        if end_row > len(self._lines): end_row = len(self._lines) 

        src_area = (0, 0, max_width, self._row_height)

        h = offset
        for row in range(self._start_row, end_row):
            txt_image = font.render(self._lines[row], True, self.color)
            if row == screen_rows - 1:
                src_area = (0, 0, max_width, max_height + offset - h)                
            image.blit(txt_image, (offset, h), area=src_area)
            h += self._row_height

    def process(self, event: pygame.event.Event) -> bool:
        "process events"

        # handle up/down arrows
        if event.type == KEYDOWN:
            key = event.dict["key"]
            if key == pygame.K_UP:
                self.start_row -= 1
                self._scroll_key = key
                self._scroll_delay = 10
                return False
            elif key == pygame.K_DOWN: 
                self.start_row += 1
                self._scroll_key = key
                self._scroll_delay = 10
                return False
        elif event.type == KEYUP:
            self._scroll_key = pygame.K_SPACE
            return False

        return super().process(event)

    def tick(self):
        if self._scroll_key == pygame.K_UP:
            self._scroll_delay -= 1
            if self._scroll_delay <= 0:
                self.start_row -= 1
                self._scroll_delay = 3
        elif self._scroll_key == pygame.K_DOWN: 
            self._scroll_delay -= 1
            if self._scroll_delay <= 0:
                self.start_row += 1
                self._scroll_delay = 3

    def update(self, screen: pygame.Surface):

        if not self._changed: return

        offset = self._border + self._padding

        if self._image == None or self._image.get_rect() != self._rect:
            self._image = create_surface(self._rect.width, self._rect.height, self._background)
            render_border(self._image, self._border, self._border_color)
        
        self.render_lines(self._image)

        screen.blit(self._image, self._rect.topleft)
        self._changed = False
    
