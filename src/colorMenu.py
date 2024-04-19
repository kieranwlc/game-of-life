#Separated Color menu operations into separate File

import pygame

SIZE = 40

colors = [
    (255, 0, 0),     # Red
    (0, 255, 0),     # Green
    (0, 0, 255),     # Blue
    (255, 255, 0),   # Yellow
    (255, 0, 255),   # Magenta
    (0, 255, 255),   # Cyan
    (255, 255, 255), # White
    (0, 0, 0)        # Black
]

def draw_color_boxes(screen, x, y):
    for i, color in enumerate(colors):
        row = i // 3
        col = i % 3
        pygame.draw.rect(screen, color, (x + col * SIZE, y + row * SIZE, SIZE, SIZE))

def get_selected_color(mouse_pos, x, y, current):
    if mouse_pos[0] > x and mouse_pos[1] > y:
        col = (mouse_pos[0] - x) // SIZE
        row = (mouse_pos[1] - y) // SIZE
        index = row * 3 + col
        if index < len(colors):
            return colors[index]
    else:
        return current
    
def hide_color_boxes(screen, x, y):
    pygame.draw.rect(screen, (0,0,0), (x,y), 3 * SIZE, 3 * SIZE)