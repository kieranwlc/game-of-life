from enum import Enum

from pygame import Color, Rect, draw
from pygame.event import Event
from pygame.surface import Surface
import random
from operator import itemgetter

from grid.cell import Cell, _coords_within_range

class IPDCell(Cell):
    def __init__(self, *args, **kwargs):
        super(IPDCell, self).__init__(*args, **kwargs)
        random_state = random.randint(0, 3)
        self._state: self.State = self.State(random_state)
        self._next_state: self.State = self.State(random_state) 
        self.choice = random_state
        if random_state == 2 or random_state == 3:
            self.choice = random.randint(0, 1)
        self.next_choice = self.choice
      

    '''
    Possible cell states
    '''
    class State(Enum):
        COOP = 0
        DEFECT = 1
        TIT4TAT = 2
        ANTITIT4TAT = 3

    @property
    def state(self) -> State:
        return self._state
    
    def calc_score(self, cell, neighbours):
        score = 0
        for neighbour in neighbours:
            if cell.choice == 0 and neighbour.choice == 0:
                score += 4
            elif cell.choice == 0 and neighbour.choice == 1:
                score += 0
            elif cell.choice == 1 and neighbour.choice == 0:
                score += 5
            elif cell.choice == 1 and neighbour.choice == 1:
                score += 1
        return score


    def calc_neighbours(self, cell):
        neighbours: list[IPDCell] = []
        for ny in range(cell._position[1] - 1, cell._position[1] + 2):
            for nx in range(cell._position[0] - 1, cell._position[0] + 2):
                if not (ny == cell._position[1] and nx == cell._position[0] or (ny != cell._position[1] and nx != cell._position[0])):
                    if _coords_within_range(cell._cells, (nx, ny)):
                        neighbours.append(cell._cells[ny][nx])
        return neighbours


    def calc_next(self):
        '''
        Triggers the cell to calculate what it's state will be on the next update
        '''

        neighbours = self.calc_neighbours(self)
        scores = []
        scores.append((self._state, self.calc_score(self, neighbours)))
        for neighbour in neighbours:
            scores.append((neighbour.state, self.calc_score(neighbour, self.calc_neighbours(neighbour))))
        random.shuffle(scores)
        self._next_state = max(scores, key = itemgetter(1))[0]
        coop_neighbours = 0
        for cell in neighbours:
            if cell.choice == 0:
                coop_neighbours += 1

        defect_neighbours = 0
        for cell in neighbours:
            if cell.choice == 1:
                defect_neighbours += 1

        if self._state == self.State.COOP:
            self.next_choice = 0
        elif self._state == self.State.DEFECT:
            self.next_choice = 1
        elif self._state == self.State.TIT4TAT:
            if coop_neighbours < defect_neighbours:
                self.next_choice = 1
            elif coop_neighbours == defect_neighbours:
                self.next_choice = random.randint(0, 1)
            else:
                self.next_choice = 0
        elif self._state == self.State.ANTITIT4TAT:
            if coop_neighbours < defect_neighbours:
                self.next_choice = 0
            else:
                self.next_choice = 1


    def update(self):
        '''
        Updates the cells state to next_state (calculated by calc_next_state())
        '''
        self._state = self._next_state
        self.choice = self.next_choice

    def draw(self, surface: Surface):
        border_color = Color('#404040')
        border_width = 2

        match self._state:
            case self.State.COOP:
                color = Color('#3DE329')
            case self.State.DEFECT:
                color = Color('#E32929')
            case self.State.TIT4TAT:
                color = Color('#2938E3')
            case self.State.ANTITIT4TAT:
                color = Color('#E2E329')

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

