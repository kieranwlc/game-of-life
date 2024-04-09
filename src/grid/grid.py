from pygame import Rect
from pygame.surface import Surface
from pygame.event import Event

from grid.cell import Cell
from core.clickable_rect import ClickableRect

class Grid(ClickableRect):
    @property
    def cells(self) -> list[list[Cell]]:
        return self._cells

    @property
    def dimensions(self) -> tuple[int, int]:
        return self._dimensions

    @property
    def rect(self) -> Rect:
        return self._rect

    @rect.setter
    def rect(self, value: Rect):
        self._rect = value

    @property
    def clickable(self) -> Rect:
        return self._rect

    def __init__(self, dimensions: tuple[int, int], rect: Rect):
        self._cells: list[list[Cell]] = []
        self._dimensions: tuple[int, int] = dimensions
        self._rect: Rect = rect
        self._init_cells(0, 0)

    def _coords_in_bounds(self, x: int, y: int):
        if (x < 0):
            return False
        if (y < 0):
            return False
        if (x >= (self._dimensions[0])):
            return False
        if (y >= self._dimensions[1]):
            return False
        return True

    def _add_neighbours(self, x: int, y: int):
        neighbours: list[Cell] = []
        for ny in range(y - 1, y + 2):
            for nx in range(x - 1, x + 2):
                if not (ny == y and nx == x):
                    if self._coords_in_bounds(nx, ny):
                        neighbours.append(self._cells[ny][nx])

        self._cells[y][x].set_neighbours(neighbours)

    def _init_cells(self, x: int, y: int):
        for y in range(self._dimensions[1]):
            self._cells.append([])
            for x in range(self._dimensions[0]):
                cell_rect = self._get_cell_rect(x, y)
                self._cells[y].append(Cell(cell_rect))
        
        for y in range(len(self._cells)):
            for x in range(len(self._cells[0])):
                self._add_neighbours(x, y)

    def update(self):
        for row in self._cells:
            for cell in row:
                cell.calc_next_status()
        for row in self._cells:
            for cell in row:
                cell.update_status()

    def draw(self, surface: Surface):
        for y in range(len(self._cells)):
            for x in range(len(self._cells[0])):
                self._cells[y][x].rect = self._get_cell_rect(x, y)
                self._cells[y][x].draw(surface)

    def _on_click(self, event: Event):
        for row in self._cells:
            for cell in row:
                if cell.rect.collidepoint(event.pos):
                    cell.handle_click(event)

    def _get_cell_rect(self, x, y) -> Rect:
        cell_w = self._rect.w / self._dimensions[0] 
        cell_h = self._rect.h / self._dimensions[1] 
        return Rect(x * cell_w, y * cell_h, cell_w, cell_h)
