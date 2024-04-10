from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum

from numpy import ndarray

from pygame import Color, Surface, draw
from pygame.event import Event
from pygame.rect import Rect

from core.clickable_rect import ClickableRect

class Cell(ClickableRect, ABC):
    def __init__(self, 
                 rect: Rect,
                 cells: ndarray,
                 position: tuple[int, int]):
        self._status: self.Status = self.Status.DEAD
        self._next_status: self.Status = self.Status.DEAD
        self._rect = rect
        self._cells = cells
        self._position = position

    '''
    Possible cell states
    '''
    class Status(Enum):
        DEAD = 0
        ALIVE = 1

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value: Status):
        self._status = value

    @property
    def next_status(self):
        return self._next_status

    @property
    def rect(self) -> Rect:
        return self._rect

    @rect.setter
    def rect(self, value: Rect):
        self._rect = value

    @property
    def clickable(self) -> Rect:
        return self._rect

    @abstractmethod
    def calc_next_status(self):
        pass

    def update(self):
        '''
        Updates the cells status to next_status (calculated by calc_next_status())
        '''
        self._status = self._next_status

    def draw(self, surface: Surface):
        border_color = Color('#404040')
        border_width = 2

        match self._status:
            case self.Status.ALIVE:
                color = Color('#484596')
            case _:
                color = Color('#737373')

        innerRect = Rect(self._rect.x + border_width,
                         self._rect.y + border_width,
                         self._rect.w - border_width,
                         self._rect.h - border_width)

        draw.rect(surface, border_color, self._rect)
        draw.rect(surface, color, innerRect)

    def _on_click(self, event: Event):
        if (self._status == self.Status.ALIVE):
            self._status = self.Status.DEAD
        elif (self._status == self.Status.DEAD):
            self._status = self.Status.ALIVE

