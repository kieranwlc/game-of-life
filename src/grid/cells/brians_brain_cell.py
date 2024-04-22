from enum import Enum

from pygame import Color, Rect, draw
from pygame.event import Event
from pygame.surface import Surface

from grid.cell import Cell, _coords_within_range

class BriansBrainCell(Cell):
    def __init__(self, *args, **kwargs):
        super(BriansBrainCell, self).__init__(*args, **kwargs)
        self._state: self.State = self.State.DEAD
        self._next_state: self.State = self.State.DEAD

    '''
    Possible cell states
    '''
    class State(Enum):
        DEAD = 0
        DYING = 1
        ALIVE = 2

    @property
    def state(self) -> State:
        return self._state

    def calc_next(self):
        '''
        Triggers the cell to calculate what it's state will be on the next update
        '''
        self._next_state = self._state

        neighbours: list[BriansBrainCell] = []
        for ny in range(self._position[1] - 1, self._position[1] + 2):
            for nx in range(self._position[0] - 1, self._position[0] + 2):
                if not (ny == self._position[1] and nx == self._position[0]):
                    if _coords_within_range(self._cells, (nx, ny)):
                        neighbours.append(self._cells[ny][nx])

        alive_neighbours = 0
        for cell in neighbours:
            if cell.state == self.State.ALIVE:
                alive_neighbours += 1

        if (self._state == self.State.ALIVE):
            self._next_state = self.State.DYING
        elif (self._state == self.State.DYING):
            self._next_state = self.State.DEAD
        elif(self._state == self.State.DEAD):
            if alive_neighbours == 2:
                self._next_state = self.State.ALIVE

    def update(self):
        '''
        Updates the cells state to next_state (calculated by calc_next_state())
        '''
        self._state = self._next_state

    def draw(self, surface: Surface):
        border_color = Color('#404040')
        border_width = 2

        match self._state:
            case self.State.ALIVE:
                color = Color('#484596')
            case self.State.DYING:
                color = Color('#8e3dba')
            case _:
                color = Color('#737373')

        innerRect = Rect(self._rect.x + border_width,
                         self._rect.y + border_width,
                         self._rect.w - border_width,
                         self._rect.h - border_width)

        draw.rect(surface, border_color, self._rect)
        draw.rect(surface, color, innerRect)

    def _on_click(self, event: Event):
        if (self._state == self.State.ALIVE):
            self._state = self.State.DEAD
        elif (self._state == self.State.DEAD):
            self._state = self.State.ALIVE

