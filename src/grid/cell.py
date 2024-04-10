from __future__ import annotations
from abc import ABC, abstractmethod

from numpy import ndarray

import pygame
from pygame import Surface
from pygame.event import Event
from pygame.rect import Rect

class Cell(ABC):
    def __init__(self, 
                 rect: Rect,
                 cells: ndarray,
                 position: tuple[int, int]):
        self._rect = rect
        self._cells = cells
        self._position = position

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
    def calc_next(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, surface: Surface):
        pass

    def process_event(self, event: Event):
        '''
        Handle pygame events
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._rect.collidepoint(event.pos):
                self._on_click(event)

    @abstractmethod
    def _on_click(self, event: Event):
        pass

def _coords_within_range(arr: ndarray, coords: tuple[int, int]):
    '''
    Function to check if a point lies within the range of an array
    '''
    if (coords[0] < 0):
        return False
    if (coords[1] < 0):
        return False
    if (coords[0] >= (arr.shape[0])):
        return False
    if (coords[1] >= (arr.shape[1])):
        return False

    return True
