import numpy as np

from pygame import Rect
from pygame.surface import Surface
from pygame.event import Event, custom_type
import csv

from grid.cell import Cell
from grid.cells.vanilla_cell import VanillaCell
from grid.cells.rps_cell import RPSCell
from grid.cells.immigration_cell import ImmigrationCell
from grid.cells.shell_cell import ShellCell
from grid.cells.brians_brain_cell import BriansBrainCell
from grid.cells.iter_prisoner_cell import IPDCell

EVENT_GAME_TICK = custom_type()

class Grid():
    def __init__(self, 
                 shape: tuple[int, int], 
                 rect: Rect,
                 celltype: str):
        self._shape = shape
        self._rect = rect
        self._cells = np.empty(self._shape, dtype=Cell)
        self._celltype = celltype
        self._init_cells()

    OPTIONS = ["Vanilla Game", 
               "Rock Paper Scissors", 
               "Immigration Game", 
               "Shell Pattern", 
               "Brians Brain",
               "Prisoner's Dilemma"]

    @property
    def shape(self) -> tuple[int, int]:
        return self._shape

    @shape.setter
    def shape(self, shape: tuple[int, int]):
        self._shape = shape
        
        # Initialize the array with the new shape, copying over any previous state
        prev = self._cells.copy()
        self._cells = np.empty(self._shape, dtype=Cell)
        self._init_cells()
        np.copyto(self._cells, prev)

    @property
    def rect(self) -> Rect:
        return self._rect

    @rect.setter
    def rect(self, value: Rect):
        self._rect = value

    @property
    def cells(self) -> np.ndarray:
        return self._cells

    @property
    def clickable(self) -> Rect:
        return self._rect

    def process_event(self, event: Event):
        '''
        Handle pygame events
        '''
        for cell in self._cells.flatten():
            cell.process_event(event)
        if event.type == EVENT_GAME_TICK:
            self.update()

    def update(self):
        '''
        Does one update of every cell's status in parallel
        '''
        for cell in self._cells.flatten():
            cell.calc_next()
        for cell in self._cells.flatten():
            cell.update()

    def draw(self, surface: Surface):
        '''
        Draws the grid, and it's contents onto the surface.
        '''
        for y in range(len(self._cells)):
            for x in range(len(self._cells[0])):
                self._cells[y][x].rect = self._get_cell_rect(x, y)
                self._cells[y][x].draw(surface)

    def _init_cells(self):
        for y in range(len(self._cells)):
            for x in range(len(self._cells[0])):
                rect = self._get_cell_rect(x, y)
                if self._celltype == "Vanilla Game":
                    self._cells[y][x] = VanillaCell(rect, self._cells, (x, y))
                elif self._celltype == "Rock Paper Scissors":
                    self._cells[y][x] = RPSCell(rect, self._cells, (x, y))
                elif self._celltype == "Shell Pattern":
                    self._cells[y][x] = ShellCell(rect, self._cells, (x, y))
                elif self._celltype == "Brians Brain":
                    self._cells[y][x] = BriansBrainCell(rect, self._cells, (x, y))
                elif self._celltype == "Immigration Game":
                    self._cells[y][x] = ImmigrationCell(rect, self._cells, (x, y))
                elif self._celltype == "Prisoner's Dilemma":
                    self._cells[y][x] = IPDCell(rect, self._cells, (x, y))

    def _handle_click(self, event: Event):
        if self.clickable.collidepoint(event.pos):
            for cell in self._cells.flatten():
                if cell.rect.collidepoint(event.pos):
                    cell.handle_click(event)

    def _get_cell_rect(self, x, y) -> Rect:
        cell_w = self._rect.w / self._shape[0] 
        cell_h = self._rect.h / self._shape[1] 
        return Rect(x * cell_w, y * cell_h, cell_w, cell_h)
    
    def _update_cell_color(self, col):
        for cell in self._cells.flatten():
            cell.newcol(col)

