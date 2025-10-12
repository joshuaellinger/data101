import pygame
from pygame.surfarray import pixels3d, array3d, blit_array
from enum import Enum
import numpy as np

from .ui_effect import UI_Effect


class MELT_MODE(Enum):
    CRUMBLE = 1

class MeltPoints:

    def __init__(self, mode: MELT_MODE, width: int, height: int):
        self.mode = mode
        self.width = width
        self.height = height

        self.num_reps = 0
        self.phase = 0.0
        
        self.enabled = True
        self.done = False

        self.cut = np.full(width, 1.0*height)
        self.shift = np.zeros(width)
        self.weights = np.array([0.1, 0.5, 1.0, 0.5, 0.1])

    def apply(self, dest: np.ndarray, background: int):
        h = self.height
        for x, (s, cut) in enumerate(zip(self.shift, self.cut)):

            if s <= 0: continue
            s = int(s)

            vals = dest[x,:,:].copy()
            vals[s:h] = vals[0:h-s]            
            vals[0:s,:] = 0

            cut= max(int(cut), 0)
            dest[x,cut:,:] = vals[cut:]

        if dest.mean() == 0.0:
            self.done = True


    def adjust(self):

        scale = np.sqrt(self.num_reps+1)

        dy = 1.0*scale + 5.0*scale*np.random.randn(self.width)
        dy = np.convolve(dy, self.weights, mode="same")
        self.shift = np.clip(dy, 0.0, 30.0)
        
        self.phase += 0.50 * np.pi * (np.random.randn())
        scale = np.random.randn(self.width)*10 + 15
        dy = scale*(1+np.cos(np.pi * np.linspace(start=self.phase, stop=self.phase + np.pi, num=self.width)))
        dy = np.convolve(dy, self.weights, mode="same")
        self.cut -= dy

        self.num_reps += 1
        if self.num_reps > 75:
            self.done = True



class UI_Effect_Melt(UI_Effect):
    "melts an image"
    def __init__(self, rect: pygame.Rect, background=200, duration=200, mode=MELT_MODE.CRUMBLE):
        super().__init__("Melt", rect)
        self._background = background
        self._duration = duration
        self._mode = mode 

        self._melt_points: MeltPoints = None

        self._melt_image: np.ndarray = None

        self._counter = 0
        self._delay = 5.0

    def reset(self) -> None:
        self._counter = 0
        self._delay = 5.0

        self._melt_points: MeltPoints = None

        self._melt_rgb: np.ndarray = None

        super().reset()

    def init_melt(self, source: pygame.Surface):
        self._melt_rgb = array3d(source)
        w, h, _ = self._melt_rgb.shape

        # setup melt points
        self._melt_points = MeltPoints(self._mode, w, h)


    def expand_melt(self):

        if self._melt_points.enabled:
            self._melt_points.adjust()
            self._melt_points.apply(self._melt_rgb, self._background)

        # stop when all the melt points are done
        if self._melt_points.done:
            self.done = True


    def tick(self) -> None:
        if self.done:
            self.changed = False
            return

        # only change every N ticks (1/15 second)
        #if self._delay >= 0.0:
        #    self._delay -= np.random.random(1) * 2.0
        #    return
        #self._delay = 5.0 * (1.0 - self._counter/self._duration)
    
        # raise done event when counter expires 
        if self._counter >= self._duration:
            self.done = True
            return

        self.changed = True
        self._counter += 1

        super().tick()

    def update(self, surface: pygame.Surface):
        if not self.changed: return

        image = surface.subsurface(self._rect)

        if self._counter == 1:
            self.init_melt(image)
        else:
            self.expand_melt()

        blit_array(image, self._melt_rgb)
                
        self.changed = False
