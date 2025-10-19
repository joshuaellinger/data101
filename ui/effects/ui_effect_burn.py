import pygame
from pygame.surfarray import pixels3d, array3d, blit_array
from enum import Enum
import numpy as np

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


class BURN_MODE(Enum):
    RANDOM = 1,
    FROM_BOTTOM = 2,
    FROM_EDGES = 3 

class BurnPoints:

    def __init__(self, mode: BURN_MODE, width: int, height: int):
        self.mode = mode
        self.width = width
        self.height = height

        self.num_reps = 0
        self.enabled = True

        self.cnt = int(np.log(width*height)) + 2

        self.x = np.random.random(self.cnt)*self.width
        self.dx = 2*np.random.randn(self.cnt)
        
        if self.mode == BURN_MODE.RANDOM: 
            self.y = np.random.random(self.cnt)*self.height
            self.dy = 2*np.random.randn(self.cnt)
        elif self.mode == BURN_MODE.FROM_BOTTOM: 
            self.y = (self.height - 1) - np.random.random(self.cnt)*3
            self.dy = np.clip(2.0*np.random.randn(self.cnt) + 2.5, 0.0, 10.0)
        
    def apply(self, dest: np.ndarray):
        x = self.x.astype(np.int32).clip(0, self.width-1) 
        y = self.y.astype(np.int32).clip(0, self.height-1) 
        dest[x,y] = 1.0

        # after 10 reps, there is a 5% change to disable
        self.num_reps += 1
        if self.num_reps > 10:
            p = np.random.random(1)
            if p < 0.05:
                self.enabled = False

    def adjust(self):

        # adjust existing points velocity            
        
        if self.mode == BURN_MODE.RANDOM: 
            self.dx = self.dx * (1 + 0.1*np.random.randn(self.cnt) + 0.1) + np.random.randn(self.cnt)
            self.dy = self.dy * (1 + 0.1*np.random.randn(self.cnt) + 0.1) + np.random.randn(self.cnt)
        elif self.mode == BURN_MODE.FROM_BOTTOM: 
            self.dx = self.dx * (1 + 0.025*np.random.randn(self.cnt)) + 2.*np.random.randn(self.cnt)
            self.dy = self.dy * (1 + 0.1*np.random.randn(self.cnt) ) - 2*np.random.randn(self.cnt) - 0.5
            self.dy = np.clip(self.dy, -10.0, 1.0)

        # update position
        self.x += self.dx
        self.y += self.dy

        # randomly reset 10% of the points
        prob = np.random.random(self.cnt)
        x = np.random.random(self.cnt)*self.width

        if self.mode == BURN_MODE.RANDOM: 
            y = np.random.random(self.cnt)*self.height
        elif self.mode == BURN_MODE.FROM_BOTTOM: 
            scale = min(self.num_reps, self.height-1)
            y = self.height - np.random.random(self.cnt)*scale
        self.x = np.where(prob > 0.10, self.x, x)
        self.y = np.where(prob > 0.10, self.y, y)
        
        if self.mode == BURN_MODE.FROM_BOTTOM and 3*self.num_reps > self.height:
            self.mode = BURN_MODE.RANDOM

        #dx, dy = 2*np.random.randn(self.cnt), 2*np.random.randn(self.cnt)
        #self.dx = np.where(prob > 0.10, self.dx, dx)
        #self.dy = np.where(prob > 0.10, self.dy, dy)





class UI_Effect_Burn(UI_Effect):
    "burn to a background gray value"
    def __init__(self, rect: pygame.Rect, background=200, duration=200, mode=BURN_MODE.RANDOM):
        super().__init__("Burn", rect)
        self._background = background
        self._duration = duration
        self._mode = mode 

        self._burn_points: BurnPoints = None

        self._burn_state: np.ndarray = None
        self._burn_image: np.ndarray = None

        self._counter = 0
        self._delay = 5.0

        self._weights = self.get_weights()

    def reset(self) -> None:
        self._counter = 0
        self._delay = 5.0

        self._burn_points: BurnPoints = None

        self._burn_state: np.ndarray = None
        self._burn_image: np.ndarry = None

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
        self._burn_points = BurnPoints(self._mode, w, h)


    def expand_burn(self):
        from scipy.signal import convolve2d 

        if self._burn_points.enabled:
            self._burn_points.adjust()
            self._burn_points.apply(self._burn_state)

        # randomize weights
        x = 0.5+np.random.randn(25).reshape((5,5))
        w = self._weights * x
        w *= 5.0/w.sum()

        # convolve
        s0 = self._burn_state
        m = s0.mean()
        if m >= 1.0:
            s1 = s0
            self.done = True
        elif m >= 0.990:
            s0[:,:] = 1.0            
            s1 = s0
        else:
            s1 = convolve2d(s0, w, mode="same").clip(0.0,1.0)
            if m > 0.95:
                s1[:,:1] = 1
                s1[:,-2:] = 1
                s1[:1,:] = 1
                s1[-2:,:] = 1
            self._burn_state = s1



        # update image
        s1_neg = (1.0 - np.where(s1<0.8, s1, 1.0)) 
        r = self._burn_image[:,:,0] * s1_neg
        
        # add edges
        if m < 0.990:
            edges = self.compute_edges(s1)
            r += edges * 255.0

        self._burn_image[:,:,0] = r.clip(0.0, 255.0).astype(np.uint8)

        g = self._burn_image[:,:,1] * s1_neg
        self._burn_image[:,:,1] = g.clip(0.0, 255.0).astype(np.uint8)

        b = self._burn_image[:,:,2] * s1_neg
        self._burn_image[:,:,2] = b.clip(0.0, 255.0).astype(np.uint8)



    def compute_edges(self, source: np.ndarray) -> np.ndarray:
        from scipy.signal import convolve2d 
        
        # Apply convolution
        edges_x = convolve2d(source, SOBEL_FILTER_X, mode='same', boundary='symm')
        edges_y = convolve2d(source, SOBEL_FILTER_Y, mode='same', boundary='symm')

        # Combine the results
        edges = np.sqrt(edges_x**2 + edges_y**2)
        e_max = edges.max() 
        if e_max > 0.0: edges = edges / e_max   # Normalize

        # Blur
        edges = convolve2d(edges, BLUR_FILTER, mode='same')

        return edges



    def tick(self) -> None:
        if self.done:
            self.changed = False
            return

        # only change every N ticks (1/15 second)
        #if self._delay >= 0.0:
        #    self._delay -= np.random.random(1) * 4.0
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
        if self.done or not self.changed: return

        image = surface.subsurface(self._rect)

        if self._counter == 1:
            self.init_burn(image)
        else:
            self.expand_burn()

        blit_array(image, self._burn_image)
              
        self.changed = False
