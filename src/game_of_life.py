import pygame
from pygame import Rect

from grid.grid import Grid

grid_rect: Rect = Rect(0, 0, 1600, 900)
grid: Grid = Grid((20, 20), grid_rect)

def main():
    pygame.init()

    pygame.display.set_caption("Game of Life")
     
    screen = pygame.display.set_mode((1600,900))
     
    running = True
    while running:
        grid.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if grid_rect.collidepoint(event.pos):
                    grid.handle_click(event)
     
if __name__=="__main__":
    main()
