from enum import Enum

from numpy import random
from pygame import Color, Rect, draw
from pygame.event import Event
from pygame.surface import Surface

from grid.cell import Cell, _coords_within_range

class RPSCell(Cell):
    def __init__(self, *args, **kwargs):
        super(RPSCell, self).__init__(*args, **kwargs)
        self._state: self.State = self.State.DEAD
        self._next_state: self.State = self.State.DEAD

    '''
    Possible cell states
    '''
    class State(Enum):
        DEAD = 0
        ROCK = 1
        PAPER = 2
        SCISSORS = 3

    @property
    def state(self) -> State:
        return self._state

    def calc_next(self):
        '''
        Triggers the cell to calculate what it's state will be on the next update
        '''
        self._next_state = self._state

        neighbours: list[RPSCell] = []
        for ny in range(self._position[1] - 1, self._position[1] + 2):
            for nx in range(self._position[0] - 1, self._position[0] + 2):
                if not (ny == self._position[1] and nx == self._position[0]):
                    if _coords_within_range(self._cells, (nx, ny)):
                        neighbours.append(self._cells[ny][nx])
        
        rock = 0
        paper = 0
        scissors = 0
        for cell in neighbours:
            if (cell.state == self.State.ROCK):
                rock += 1
            elif (cell.state == self.State.PAPER):
                paper += 1
            elif (cell.state == self.State.SCISSORS):
                scissors += 1

        if self._state == self.State.DEAD:
            if rock > paper and rock > scissors:
                if rock == 3:
                    self._next_state = self.State.ROCK
            elif paper > rock and paper > scissors:
                if paper == 3:
                    self._next_state = self.State.PAPER
            elif scissors > paper and scissors > rock:
                if scissors == 3:
                    self._next_state = self.State.SCISSORS

        if (self._state != self.State.DEAD):
            if self._state == self.State.ROCK:
                if rock < 1 or rock > 3:
                    self._next_state = self.State.DEAD
                if paper > scissors:
                    self._next_state = self.State.DEAD
            if self._state == self.State.PAPER:
                if paper < 1 or paper > 3:
                    self._next_state = self.State.DEAD
                if scissors > rock:
                    self._next_state = self.State.DEAD
            if self._state == self.State.SCISSORS:
                if scissors < 1 or scissors > 3:
                    self._next_state = self.State.DEAD
                if rock > paper:
                    self._next_state = self.State.DEAD

    def update(self):
        '''
        Updates the cells state to next_state (calculated by calc_next_state())
        '''
        self._state = self._next_state

    def draw(self, surface: Surface):
        border_color = Color('#404040')
        border_width = 2

        match self._state:
            case self.State.ROCK:
                color = Color('#484596')
            case self.State.PAPER:
                color = Color('#026312')
            case self.State.SCISSORS:
                color = Color('#7d0418')
            case _:
                color = Color('#737373')

        innerRect = Rect(self._rect.x + border_width,
                         self._rect.y + border_width,
                         self._rect.w - border_width,
                         self._rect.h - border_width)

        draw.rect(surface, border_color, self._rect)
        draw.rect(surface, color, innerRect)

    def _on_click(self, event: Event):
        if (self._state == self.State.DEAD):
            self._state = self.State.ROCK
        elif (self._state == self.State.ROCK):
            self._state = self.State.PAPER
        elif (self._state == self.State.PAPER):
            self._state = self.State.SCISSORS
        elif (self._state == self.State.SCISSORS):
            self._state = self.State.DEAD



