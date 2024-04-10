import pygame
from pygame import Rect, time

import pygame_gui
from pygame_gui.elements import UIButton

from grid.grid import Grid, EVENT_GAME_TICK
from settings import settings

# Markup display into Rects
display_width = settings.settings_read("display_width")
display_height = settings.settings_read("display_height")

pygame.init()
pygame.display.set_caption("Game of Life")

screen = pygame.display.set_mode((display_width, display_height))
gui_manager = pygame_gui.UIManager((display_width, display_height))

grid: Grid = Grid((50, 50), Rect(0, 0, display_height, display_height))
    
playing = False
play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((display_height, 0), (100, 50)),
                                           text='Play',
                                           manager=gui_manager)
def toggle_play():
    global playing
    if not playing:
        play_button.text = 'Pause'
        play_button.rebuild()
        time.set_timer(EVENT_GAME_TICK, millis=100, loops=0)
        playing = True
    else:
        play_button.text = 'Play'
        play_button.rebuild()
        time.set_timer(EVENT_GAME_TICK, millis=0)
        playing = False 

clock = pygame.time.Clock()
running = True

while running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        gui_manager.process_events(event)
        grid.process_event(event)

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == play_button:
                toggle_play()

    grid.draw(screen)
    gui_manager.update(time_delta)
    gui_manager.draw_ui(screen)
    pygame.display.update()

