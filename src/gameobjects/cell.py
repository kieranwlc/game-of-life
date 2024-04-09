from __future__ import annotations
from enum import Enum

from pygame import Color, Surface, draw
from pygame.event import Event
from pygame.rect import Rect

class Cell:
    class Status(Enum):
        DEAD = 0
        ALIVE = 1
        UNKNOWN = 2

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value: Status):
        self._status = value

    @property
    def next_status(self):
        return self._alive

    @property
    def neighbours(self):
        return self._neighbours

    @property
    def rect(self) -> Rect:
        return self._rect

    @rect.setter
    def rect(self, value: Rect):
        self._rect = value

    def __init__(self, rect: Rect):
        self._neighbours: list[Cell] = []
        self._status: self.Status = self.Status.DEAD
        self._next_status: self.Status = self.Status.UNKNOWN
        self._rect: Rect = rect

    def calc_next_status(self):
        aliveNeighbours: int = 0
        for adjacentCell in self._neighbours:
            if adjacentCell.alive:
                aliveNeighbours += 1

        if (self._alive):
            if (aliveNeighbours < 2) or (aliveNeighbours > 3):
                self._next_status = self.Status.DEAD
        else:
            if aliveNeighbours > 3:
                self._next_status = self.Status.ALIVE

    def update_status(self):
        self._status = self._next_status
        self._next_status = self.Status.UNKNOWN

    def set_neighbours(self, val: list[Cell]):
        self._neighbours = val.copy()

    def draw(self, surface: Surface):
        border_color = Color('#404040')
        border_width = 2

        color = Color('#737373')
        if (self._status == self.Status.ALIVE):
            color = Color('#484596')
        innerRect = Rect(self._rect.x + border_width,
                         self._rect.y + border_width,
                         self._rect.w - border_width,
                         self._rect.h - border_width)

        draw.rect(surface, border_color, self._rect)
        draw.rect(surface, color, innerRect)

    def handle_click(self, event: Event):
        if (self._status == self.Status.ALIVE):
            self._status = self.Status.DEAD
        elif (self._status == self.Status.DEAD):
            self._status = self.Status.ALIVE
