import numpy as np

from pygame import Rect
from pygame.surface import Surface
from pygame.event import Event

from core.clickable_rect import ClickableRect
from grid.cell import Cell
from grid.cells.vanilla_cell import VanillaCell

class Grid(ClickableRect):
    def __init__(self, 
                 shape: tuple[int, int], 
                 rect: Rect):
        self._shape = shape
        self._rect = rect
        self._cells = np.empty(self._shape, dtype=Cell)
        self._init_cells()

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

    def update(self):
        '''
        Does one update of every cell's status in parallel
        '''
        for cell in self._cells.flatten():
            cell.calc_next_status()
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
                self._cells[y][x] = VanillaCell(rect, self._cells, (x, y))

    def _on_click(self, event: Event):
        for cell in self._cells.flatten():
            if cell.rect.collidepoint(event.pos):
                cell.handle_click(event)

    def _get_cell_rect(self, x, y) -> Rect:
        cell_w = self._rect.w / self._shape[0] 
        cell_h = self._rect.h / self._shape[1] 
        return Rect(x * cell_w, y * cell_h, cell_w, cell_h)

