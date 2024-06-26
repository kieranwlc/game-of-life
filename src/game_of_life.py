import pickle
import pygame
from pygame import Rect, time

import pygame_gui

from grid.grid import Grid, EVENT_GAME_TICK
from settings import settings
from colorMenu import draw_color_boxes, get_selected_color, hide_color_boxes

from tkinter import Tk, filedialog

# Markup display into Rects
display_width = settings.settings_read("display_width")
display_height = settings.settings_read("display_height")

chosen_option = "Vanilla Game"
col = (0,0,0)

pygame.init()
pygame.display.set_caption("Game of Life")

screen = pygame.display.set_mode((display_width, display_height))
gui_manager = pygame_gui.UIManager((display_width, display_height))

global grid
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
        time.set_timer(EVENT_GAME_TICK, millis=get_tick_delay_ms(), loops=0)
        playing = True
    else:
        play_button.text = 'Play'
        play_button.rebuild()
        time.set_timer(EVENT_GAME_TICK, millis=0)
        playing = False 

menuShow = False
option_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((display_height, 55), (100, 50)),
                                           text='Options',
                                           manager=gui_manager)

def create_text_surface(text, font_size, color):
    font = pygame.font.Font(None, font_size)
    return font.render(text, True, color)

def draw_options(screen, x, y):
    option_y = y
    for option in Grid.OPTIONS:
        pygame.draw.rect(screen, (100, 100, 100), (x, option_y, 170, 50))
        text_surface = create_text_surface(option, 24, (255,255,255))
        text_rect = text_surface.get_rect(center=(x + 170 / 2, option_y + 50 / 2))
        screen.blit(text_surface, text_rect)
        option_y += 60

def toggle_options(screen):
    global menuShow
    if menuShow:
        menuShow = False
        pygame.draw.rect(screen, (0,0,0), (display_height + 105, 55, 170, 60 * len(Grid.OPTIONS)))
        if chosen_option == "Immigration Game":
            draw_color_boxes(screen, display_height + 10, 230)
    else:
        if chosen_option == "Immigration Game":
            hide_color_boxes(screen, display_height + 10, 230)
        draw_options(screen, display_height + 105, 55)
        menuShow = True

save_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((display_height, 110), (100, 50)),
                                           text='Save',
                                           manager=gui_manager)

load_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((display_height, 165), (100, 50)),
                                           text='Load',
                                           manager=gui_manager)

next_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((display_height + 200, display_height - 50), (100, 50)),
                                           text='Next',
                                           manager=gui_manager)

def force_next_tick():
    event = pygame.Event(EVENT_GAME_TICK)
    pygame.event.post(event)

clear_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((display_height + 105, 0), (100, 50)),
                                           text='Clear',
                                           manager=gui_manager)

def clear_grid():
    global grid
    grid = Grid((50, 50), Rect(0, 0, display_height, display_height), chosen_option)

speed_slider = pygame_gui.elements.UIHorizontalSlider(pygame.Rect((display_height, display_height - 50), (200, 50)),
                                                      value_range=(1, 6),
                                                      start_value=1,
                                                      click_increment=1)

def update_speed():
    if playing:
        time.set_timer(EVENT_GAME_TICK, millis=get_tick_delay_ms(), loops=0)

def get_tick_delay_ms():
    speed_discreet = round(6 - speed_slider.current_value)
    return 40 * pow(2, speed_discreet)

def load_grid_dialog():
    global grid

    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.destroy()
    if (file_path):
        with open(file_path, "rb") as infile:
            infile.seek(0)
            grid = pickle.load(infile)

def save_grid_dialog():
    global grid

    root = Tk()
    root.withdraw()
    user_input = filedialog.asksaveasfilename()
    root.destroy()
    if (user_input):
        with open(user_input, "wb") as outfile:
            pickle.dump(grid, outfile)

clock = pygame.time.Clock()
running = True

while running:
    time_delta = clock.tick(60)/1000.0

    for event in pygame.event.get():
        gui_manager.process_events(event)
        grid.process_event(event)

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                save_grid_dialog()
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == play_button:
                toggle_play()
            if event.ui_element == option_button:
                toggle_options(screen)
            if event.ui_element == save_button:
                save_grid_dialog()
            if event.ui_element == load_button:
                load_grid_dialog()
            if event.ui_element == clear_button:
                clear_grid()
            if event.ui_element == next_button:
                force_next_tick()

        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == speed_slider:
                update_speed();

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = event.pos
                if menuShow:
                    for i, option in enumerate(Grid.OPTIONS):
                        option_rect = pygame.Rect(display_height + 105, 55 + i * 60, 170, 50)
                        if option_rect.collidepoint(mouse_x, mouse_y):
                            chosen_option = option
                            grid = Grid((50, 50), Rect(0, 0, display_height, display_height), chosen_option)
                            toggle_options(screen)
                            if chosen_option == "Immigration Game":
                                draw_color_boxes(screen, display_height + 10, 230)
                if chosen_option == "Immigration Game":
                    col = get_selected_color(event.pos, display_height + 10, 230, col)
                    grid._update_cell_color(col)

    grid.draw(screen)
    gui_manager.update(time_delta)
    gui_manager.draw_ui(screen)
    pygame.display.update()

