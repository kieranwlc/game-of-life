import pygame
from pygame import Rect, time

import pygame_gui
from pygame_gui.elements import UIButton

from grid.grid import Grid, EVENT_GAME_TICK
from settings import settings

# Markup display into Rects
display_width = settings.settings_read("display_width")
display_height = settings.settings_read("display_height")

chosen_option = "Vanilla Game"

pygame.init()
pygame.display.set_caption("Game of Life")

screen = pygame.display.set_mode((display_width, display_height))
gui_manager = pygame_gui.UIManager((display_width, display_height))

grid: Grid = Grid((50, 50), Rect(0, 0, display_height, display_height), chosen_option)
    
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

options = ["Vanilla Game", "Rock Paper Scissors", "Immigration Game"]
menuShow = False
option_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((display_height, 55), (100, 50)),
                                           text='Options',
                                           manager=gui_manager)

def create_text_surface(text, font_size, color):
    font = pygame.font.Font(None, font_size)
    return font.render(text, True, color)

def draw_options(screen, x, y):
    option_y = y
    for option in options:
        pygame.draw.rect(screen, (100, 100, 100), (x, option_y, 170, 50))
        text_surface = create_text_surface(option, 24, (255,255,255))
        text_rect = text_surface.get_rect(center=(x + 170 / 2, option_y + 50 / 2))
        screen.blit(text_surface, text_rect)
        option_y += 60

def toggle_options(screen):
    global menuShow
    if menuShow:
        menuShow = False
        pygame.draw.rect(screen, (0,0,0), (display_height + 105, 55, 170, 60 * 3))
    else:
        draw_options(screen, display_height + 105, 55)
        menuShow = True

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
            if event.ui_element == option_button:
                toggle_options(screen)
        if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = event.pos
                    if menuShow:
                        for i, option in enumerate(options):
                            option_rect = pygame.Rect(display_height + 105, 55 + i * 60, 170, 50)
                            if option_rect.collidepoint(mouse_x, mouse_y):
                                chosen_option = option
                                grid = Grid((50, 50), Rect(0, 0, display_height, display_height), chosen_option)
                                toggle_options(screen)

    grid.draw(screen)
    gui_manager.update(time_delta)
    gui_manager.draw_ui(screen)
    pygame.display.update()

