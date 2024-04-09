from pygame import Rect
from pygame.surface import Surface
from pygame.event import Event

from gameobjects.cell import Cell

class Grid:
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

    def __init__(self, dimensions: tuple[int, int], rect: Rect):
        self._cells: list[list[Cell]] = []
        self._dimensions: tuple[int, int] = dimensions
        self._rect: Rect = rect
        self._init_cells(0, 0)

    def _init_cells(self, x: int, y: int):
        for y in range(self._dimensions[1]):
            self._cells.append([])
            for x in range(self._dimensions[0]):
                cell_rect = self._get_cell_rect(x, y)
                self._cells[y].append(Cell(cell_rect))
        
        for y in range(self._dimensions[1]):
            for x in range(self._dimensions[0]):
                neighbours: list[Cell] = []
                if (x - 1 >= 0):
                    neighbours.append(self._cells[y][x - 1])
                if (y - 1 >= 0):
                    neighbours.append(self._cells[y - 1][x])
                if (x + 1 < (self._dimensions[0] - 1)):
                    neighbours.append(self._cells[y][x + 1])
                if (y + 1 < self._dimensions[1] - 1):
                    neighbours.append(self._cells[y + 1][x])

                self._cells[y][x].set_neighbours(neighbours)

    def update(self):
        for row in self._cells:
            for cell in row:
                cell.calc_next_status()
        for row in self._cells:
            for cell in row:
                cell.update_status()

    def draw(self, surface: Surface):
        for y in range(self._dimensions[1]):
            for x in range(self._dimensions[0]):
                self._cells[y][x].rect = self._get_cell_rect(x, y)
                self._cells[y][x].draw(surface)

    def handle_click(self, event: Event):
        for row in self._cells:
            for cell in row:
                if cell.rect.collidepoint(event.pos):
                    cell.handle_click(event)

    def _get_cell_rect(self, x, y) -> Rect:
        cell_w = self._rect.w / self._dimensions[0] 
        cell_h = self._rect.h / self._dimensions[1] 
        return Rect(x * cell_w, y * cell_h, cell_w, cell_h)
