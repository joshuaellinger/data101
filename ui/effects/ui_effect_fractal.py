import pygame
from pygame.surfarray import pixels3d, array3d, blit_array

import numpy as np
from enum import Enum
from .ui_effect import UI_Effect

class FractalNamesEnum(Enum):
    MANDELBRIOT = 1,
    JULIA = 2



class UI_Effect_Fractal(UI_Effect):
    "render a fractal"
    def __init__(self, rect: pygame.Rect, background=200, iterations=20, 
        fractal=FractalNamesEnum.JULIA, version=3):

        super().__init__("Fade", rect)
        self._background = background
        self._iterations = iterations
        self._fractal = fractal
        self._version = version

        self._image:np.ndarray = None
        self._C:np.ndarray = None
        self._Z:np.ndarray = None
        self._M:np.ndarray = None

        self._counter = -1
        self._delay = 0

    def reset(self) -> None:
        self._counter = -1
        self._delay = 0
        super().reset()

    def tick(self) -> None:
        if self.done:
            self.changed = False
            return

        if self._delay < 5:
            self._delay += 1
            return

        self.changed = True
        self._delay = 0


        # raise done event after last update 
        self._counter += 1
        if self._counter >= self._iterations:
            self.done = True

        super().tick()

    def init_fractal(self, source: pygame.Surface):
        self._image = array3d(source)
        w, h, _ = self._image.shape

        if self._fractal == FractalNamesEnum.MANDELBRIOT:
            x = np.linspace(-2, 1, num=w).reshape((1, w))
            y = np.linspace(-1, 1, num=h).reshape((h, 1))
            self._C = np.tile(x, (h, 1)) + 1j * np.tile(y, (1, w))

            self._Z = np.zeros((h, w), dtype=complex)
        elif self._fractal == FractalNamesEnum.JULIA:
            if self._version == 1:
                self._C = np.full((h, w), -0.4 + 0.6j)
            elif self._version == 2:
                self._C = np.full((h, w), .4 + -0.5j)
            elif self._version == 3:
                m, s = .4 + -0.5j, 0.01
                self._C = ((m - (1+1j) * s/2) + s * (np.random.rand(h*w) + 1j * np.random.rand(h*w))).reshape(h, w) 
            else:
                raise Exception(f"Julia version {self._version} not implemented")

            s = 200  # Scale.
            x = np.linspace(-w / s, w / s, num=w).reshape((1, w))
            y = np.linspace(-h / s, h / s, num=h).reshape((h, 1))
            self._Z = np.tile(x, (h, 1)) + 1j * np.tile(y, (1, w))
        else:
            raise NotImplemented(f"{self._fractal} not implemented")

        self._M = np.full((h, w), True, dtype=bool)
        self._N = np.zeros((h, w))


    def update_fractal(self):
        if (self._fractal == FractalNamesEnum.MANDELBRIOT or
            self._fractal == FractalNamesEnum.JULIA):
            Z, M, C, N = self._Z, self._M, self._C, self._N
            Z[M] = Z[M] * Z[M] + C[M]
            M[np.abs(Z)>2] = False
            N[M] = self._counter
            print(self._counter)
        else:
            raise NotImplemented(f"{self._fractal} not implemented")

    def update_image(self):
        if False:
            # plot set only
            Z, M = self._Z.T, self._M.T
            scaled = np.abs(Z*M)
            xmin,xmax = np.min(scaled), np.max(scaled)
            xscale = 1.0/(xmax-xmin)
        else:
            # plot when pixel when to infinity
            N = self._N.T
            scaled = N
            xmin,xmax = np.min(scaled), np.max(scaled)
            xscale = 1.0/(xmax-xmin)

        # use colormap from matplotlib
        import matplotlib
        cmap = matplotlib.cm.get_cmap('plasma')

        vals = (scaled - xmin) * xscale
        rgb = cmap(vals, bytes=True)
        
        self._image[:,:,0] = rgb[:,:,0]
        self._image[:,:,1] = rgb[:,:,1]
        self._image[:,:,2] = rgb[:,:,2]


    def update(self, surface: pygame.Surface):
        if not self.changed: return

        source = surface.subsurface(self._rect)

        if self._counter == 0:
            self.init_fractal(source)
        else:
            self.update_fractal()
        self.update_image()

        blit_array(source, self._image)

        self.changed = False
