# Effects are graphic effects (like fade) that apply to elements or views over time
#  
#  All effects:
#   1. have a done flag and an ondone event
#   2. have a changed flag
#   3. have a counter that increments every tick
#   4. operate on the surface of their target element/view
#
#  Effects are managed by the screen logic.  They are applied after normal
#  updates and removed the screen when done.
#
import pygame
from pygame.locals import *

from typing import Callable, Tuple
from abc import ABC, abstractmethod
from enum import Enum 


UI_EffectCallback = Callable[["UI_Effect"], None]
def NoOp_EffectCallback(effect: "UI_Effect"):
    pass

class UI_Effect(ABC):
    "an effect applied to pixels of an element/view"
    def __init__(self, id: str, rect: pygame.Rect):
        self._id = id
        self._rect = rect

        self._done = False
        self._changed = False

        self._ondone: UI_EventHandler = NoOp_EffectCallback

    # make the identifer and target read only 
    @property
    def id(self) -> str:
        "the identifier for the effect"
        return self._id
    @property
    def rect(self) -> pygame.rect:
        "the draw rectangle for the effect"
        return self._rect
    @rect.setter
    def rect(self, value: pygame.rect) -> None:
        self._rect = value

    # properties that trigger changes/events
    @property
    def changed(self) -> bool:
        "set when effect needs to update screen"
        return self._changed
    @changed.setter
    def changed(self, value: bool) -> None:
        self._changed = value

    @property
    def done(self) -> bool:
        "set when effect completes"
        return self._done
    @done.setter
    def done(self, value: bool) -> None:
        "mark the effect as done"
        if not self._done and value: 
            self._ondone(self)
        self._done = value

    # callbacks
    @property
    def ondone(self) -> UI_EffectCallback:
        "effect handler called effect is finished running"
        return self._ondone
    @ondone.setter
    def ondone(self, value: UI_EffectCallback) -> None:
        self._ondone = value

    # processing routines
    def tick(self) -> None:
        "called per tick (typically 1/30 of a second)"
        pass

    # only method that an effect has to implement
    @abstractmethod
    def update(self, screen: pygame.Surface) -> None:
        "update display"
        pass
