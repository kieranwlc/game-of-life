from numpy import ndarray
from grid.cell import Cell

class VanillaCell(Cell):
    def calc_next_status(self):
        '''
        Triggers the cell to calculate what it's status will be on the next update
        '''
        self._next_status = self._status

        neighbours: list[Cell] = []
        for ny in range(self._position[1] - 1, self._position[1] + 2):
            for nx in range(self._position[0] - 1, self._position[0] + 2):
                if not (ny == self._position[1] and nx == self._position[0]):
                    if _coords_within_range(self._cells, (nx, ny)):
                        neighbours.append(self._cells[ny][nx])

        alive_neighbours = 0
        for cell in neighbours:
            if cell.status == self.Status.ALIVE:
                alive_neighbours += 1

        if (self._status == self.Status.ALIVE):
            if (alive_neighbours < 2) or (alive_neighbours > 3):
                self._next_status = self.Status.DEAD
        elif (self._status == self.Status.DEAD):
            if alive_neighbours == 3:
                self._next_status = self.Status.ALIVE

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
