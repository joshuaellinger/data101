import pygame
from pygame.surfarray import pixels3d, array3d, blit_array

import numpy as np
from scipy.signal import convolve2d 

from .ui_effect import UI_Effect

# Create Sobel operators for edge detection
SOBEL_FILTER_X = np.array([[-1, 0, 1], 
                    [-2, 0, 2], 
                    [-1, 0, 1]])

SOBEL_FILTER_Y = np.array([[-1, -2, -1], 
                    [0, 0, 0], 
                    [1, 2, 1]])
BLUR_FILTER = np.array([[.1, .1, .1], 
                [.1, .8, .1], 
                [.1, .1, .1]]) 



class UI_Effect_Burn(UI_Effect):
    "burn to a background gray value"
    def __init__(self, rect: pygame.Rect, background=200, duration=80):
        super().__init__("Burn", rect)
        self._background = background
        self._duration = duration
   
        self._burn_points: np.ndarry = None
        self._point_cnt = 2
        self._point_step = 2

        self._burn_state: np.ndarray = None
        self._burn_image: np.ndarray = None

        self._counter = 0
        self._delay = 5.0

        self._weights = self.get_weights()

    def reset(self) -> None:
        self._counter = 0
        self._delay = 5.0

        self._burn_points: np.ndarry = None
        self._point_cnt = 2
        self._point_step = 2

        self._burn_state: np.ndarray = None
        self._burn_image: pygame.Surface = None

        self._weights = self.get_weights()
        super().reset()

    def get_weights(self) -> np.ndarray:
        w = np.ones((5,5),dtype=np.float32) 
        w[1:4,1:4] = -(w.sum() - w[1:3, 1:3].sum())
        w[2,2] = -2*(w.sum())
        w *= 1.0/w.sum()
        return w

    def init_burn(self, source: pygame.Surface):
        self._burn_image = array3d(source)

        # setup state (starts at 0, goes to 1)
        w, h, d = self._burn_image.shape
        self._burn_state = np.zeros((w, h))

        # setup burn points
        n = self._point_cnt
        x = (np.random.random(n)*w).astype(np.int32).clip(0, w-1) 
        y = (np.random.random(n)*h).astype(np.int32).clip(0, h-1) 
        self._burn_points = np.zeros((n,2), dtype=np.int32)
        self._burn_points[:,0] = x
        self._burn_points[:,1] = y

    def adjust_burn_points(self):        
        
        n = self._point_cnt
        step = self._point_step
        if step == 0:
            return

        points = self._burn_points

        # set burn points in state to 1 
        x, y = points[:,0], points[:,1]
        self._burn_state[x,y] = 1.0

        w,h = self._burn_state.shape

        if step > 0: 
            # ----- ramping up mode -----
            # adjust existing points by +/- N(2)
            x = (x + 3.0*np.random.randn(n)).astype(np.int32).clip(0, w-1) 
            y = (y + 3.0*np.random.randn(n)).astype(np.int32).clip(0, h-1) 
            points[:,0] = x
            points[:,1] = y

            # add new points
            points.resize(n+step,2,refcheck=False)
            x = (np.random.random(step)*w).astype(np.int32).clip(0, w-1) 
            y = (np.random.random(step)*h).astype(np.int32).clip(0, h-1) 
            points[n:,0] = x
            points[n:,1] = y

            # after 10, start ramping down
            n += step
            self._point_cnt = n
            if n >= 10: self._point_step = -1
        else: 
            # ----- ramping down mode -----
            # stop adding burn points at bottom of ramp
            if n+step <= 2:
                step = 0
                return

            n += step
            points.resize(n,2,refcheck=False)

            # adjust existing points by +/- N(4)
            x, y = points[:,0], points[:,1]
            x = (x + 4.0*np.random.randn(n)).astype(np.int32).clip(0, w-1) 
            y = (y + 4.0*np.random.randn(n)).astype(np.int32).clip(0, h-1) 
            points[:,0] = x
            points[:,1] = y

        self._burn_points = points

    def expand_burn(self):

        self.adjust_burn_points()

        # randomize weights
        x = 0.5+np.random.randn(25).reshape((5,5))
        w = self._weights * x
        w *= 5.0/w.sum()

        # convolve
        s0 = self._burn_state
        s1 = convolve2d(self._burn_state, w, mode="same").clip(0.0,1.0)
        self._burn_state = s1

        # get edges
        edges = self.compute_edges(s1)

        # update image
        s1_neg = (1.0 - np.where(s1<0.8, s1, 1.0)) 
        r = self._burn_image[:,:,0] * s1_neg + edges * 255.0
        self._burn_image[:,:,0] = r.clip(0.0, 255.0).astype(np.uint8)

        g = self._burn_image[:,:,1] * s1_neg
        self._burn_image[:,:,1] = g.clip(0.0, 255.0).astype(np.uint8)

        b = self._burn_image[:,:,2] * s1_neg
        self._burn_image[:,:,2] = b.clip(0.0, 255.0).astype(np.uint8)

        # stop when the image is all the same color
        if s1.mean() >= 0.999:
            self.done = True

    def compute_edges(self, source: np.ndarray) -> np.ndarray:
        # Apply convolution
        edges_x = convolve2d(source, SOBEL_FILTER_X, mode='same', boundary='symm')
        edges_y = convolve2d(source, SOBEL_FILTER_Y, mode='same', boundary='symm')

        # Combine the results
        edges = np.sqrt(edges_x**2 + edges_y**2)
        edges = edges / edges.max()  # Normalize

        # Blur
        edges = convolve2d(edges, BLUR_FILTER, mode='same')

        return edges



    def tick(self) -> None:
        if self.done:
            self.changed = False
            return

        # only change every N ticks (1/15 second)
        if self._delay >= 0.0:
            self._delay -= np.random.random(1) * 4.0
            return
        self._delay = 5.0 * (1.0 - self._counter/self._duration)
    
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
            self.init_burn(image)
        else:
            self.expand_burn()

        blit_array(image, self._burn_image)
                
        self.changed = False
