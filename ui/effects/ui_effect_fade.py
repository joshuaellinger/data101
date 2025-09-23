import pygame
from pygame.surfarray import array3d, blit_array

import numpy as np

from .ui_effect import UI_Effect

class UI_Effect_Fade(UI_Effect):
    "fade to a background gray value"
    def __init__(self, rect: pygame.Rect, background=200, duration=20):
        super().__init__("Fade", rect)
        self._background = background
        self._duration = duration
   
        self._upstep = int(max(background/duration, 1))
        self._downstep =  int(min((255-background)/duration,1))

        self._counter = 0
        self._min = 0
        self._max = 255
   
    def tick(self) -> None:
        if self.done:
            self.changed = False
            return

        # raise done event after last update 
        if self._min == self._max:
            self.done = True
            return

        if self._min < self._background:
            self.changed = True
            self._min += self._upstep
        if self._max > self._background:
            self.changed = True
            self._max -= self._downstep
        if self._min > self._max:
            self._min = self._max = self._background

        self._counter += 1

        super().tick()

    def update(self, surface: pygame.Surface):
        if not self.changed: return

        pixels = array3d(surface)
        x1, x2 = self._rect.left, self._rect.right
        y1, y2 = self._rect.top, self._rect.bottom
        pixels[x1:x2, y1:y2, :] = pixels[x1:x2, y1:y2, :].clip(self._min, self._max)
        blit_array(surface, pixels)

        self.changed = False
