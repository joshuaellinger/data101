# UI_Host and UI_View - A structure for running games with multiple screens 
#
# The host manages the pygame instance.
#
# A game developer registers one or more views with it to handle displaying
# different views without having to open new screens.  Each view has a list
# of display elements (UI_Elements) and effects (UI_Effect).
#
# A view has four primary methods that can be overwritten by the developer:
#     1. activate - called when the screen is selected.
#     2. deactivate - called when switching to a new screen
#     3. process - called for each event
#     4. tick - perform any time-based actions.
#     5. update - called to redraw the screen
#
# The host has three main methods
#     1. register a view
#     2. selected a new view
#     3. run the main game loop 
#
# Typically, the developer will register elements in activate and clear them
# in deactivate and implement any time based processing in tick.  The default
# behavior for both process and update is to call it on each element but that
# can be customized.
#
# Effects are added once then removed when completed.
#
# See sample_screens.py for an example
#

import pygame
from pygame.locals import *
import time

from typing import List
from abc import ABC, abstractmethod 

from .ui_element import UI_Element
from .effects.ui_effect import UI_Effect
#import ui_timer

pygame.init()

class UI_View(ABC):
    "Base class for define a view in a game"
    def __init__(self, id: str, caption: str):
        self.id = id
        self.caption = caption
        self._elements: List[UI_Element] = []
        self._effects: List[UI_Effect] = []

    def clear(self):
        self._elements.clear()
        self._effects.clear()

    def redraw(self):
        for e in self._elements:
            e.changed = True
        self._effects.clear()

    # elements
    def add_element(self, element: UI_Element):
        "add an element to a view"
        if element in self._elements:
            raise Exception(f"Element {element.id} is already in View {self.id}")
        self._elements.append(element)
    
    def index_element(self, element: UI_Element) -> int:
        "index of an element"
        return self._elements.index(element)
        
    def remove_element(self, element: UI_Element):
        "remove an element from a view"
        self._elements.remove(element)

    # effects
    def add_effect(self, effect: UI_Effect):
        "add an effect to a view"
        if effect in self._effects:
            raise Exception(f"Effect {effect.id} is already in View {self.id}")
        self._effects.append(effect)
    
    def index_element(self, effect: UI_Effect) -> int:
        "index of an effect"
        return self._effects.index(effect)
        
    def remove_effect(self, effect: UI_Effect):
        "remove an effect from a view"
        self._effects.remove(effect)

    # actions

    @abstractmethod
    def activate(self, host: "UI_Host"):
        "prepare before entering a view"
        pass

    @abstractmethod
    def deactivate(self, host: "UI_Host"):
        "cleanup after exiting a view"
        pass

    def process(self, event: pygame.event.Event) -> None:
        "process events"
        # only process event one if there are overlapping elements
        for elem in reversed(self._elements):
            if elem.process(event): break

    def tick(self):
        "handle per-tick changes"

        # remove completed effects
        completed = []
        for effect in self._effects:
            if effect.done: completed.add(effect)
        for effect in completed:
            self._effects.remove_effect(effect)

        # run tick actions
        for elem in self._elements:
            elem.tick()
        for effect in self._effects:
            effect.tick()

    def update(self, screen: pygame.Surface):
        "update the view"
        
        for elem in self._elements:
            elem.update(screen)
        for effect in self._effects:
            effect.update(screen)


class UI_Host:
    "Manages the pygame engine, a shared screen, and a list of views"

    def __init__(self, *, width=1024, height=650, fps=30):    
        self.screen_size = (width, height)
        self.fps = fps # frames per second

        self.views: List[UI_View] = []
        
        self.current_view: UI_View = None
        self.next_view: UI_View = None 

        self.screen: pygame.Surface = None
        self.clock: pygame.time.Clock = None

    def register_view(self, view: UI_View):
        "register a view with the host"
        if view in self.views:
            raise Exception(f"View {view.id} is already registered")
        self.views.append(view)

    def unregister_view(self, view: UI_View):
        "unregister a view from the host"
        self.views.remove(view)

    def select_new_view(self, id: str):
        "select a new view once after update"
        if self.current_view.id == id:
            raise Exception("Cannot reselect current view")

        for v in self.views:
            if v.id == id:
                self.next_view = v
                return
        raise Exception("Invalid View ID (" + id + "), registered views are:" + ", ". join([v.id for v in self.views]))

    def run_game(self):

        # open the screen
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        
        #sysfont = pygame.font.get_default_font()
        #font = pygame.font.SysFont(None, 48)

        # activate the first view
        self.current_view = self.views[0]
        self.current_view.activate(self)
        pygame.display.set_caption(self.current_view.caption)

        #ui_timer.TIMER.record(f"RUN {self.fps}")

        # MAIN GAME LOOP
        running = True
        while running:

            # 1. send any events to the view            
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    break
                self.current_view.process(event)

            if not running:
                break

            # 3. tell the view to run periodic actions
            self.current_view.tick()            

            # 4. update the screen
            self.current_view.update(self.screen)            
            
            # make it visible to the player
            pygame.display.flip()

            # if needed, deactivate the old view and activate the new view.
            if self.next_view != None:
                self.current_view.deactivate(self)
                self.current_view = self.next_view
                self.next_view = None
                self.current_view.activate(self)
                pygame.display.set_caption(self.current_view.caption)

            # limit update rate to FPS (frames-per-second)
            self.clock.tick(self.fps) 
        
        #ui_timer.TIMER.record("QUIT")

        pygame.quit()    

    def exit_game(self):
        "send the QUIT event to the game queue"
        pygame.event.post(QUIT)

