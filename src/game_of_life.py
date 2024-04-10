import pygame
from pygame import Rect, time
from pygame.surface import Surface

from grid.grid import Grid
from ui.button import Button

# Markup display into Rects
DISPLAY_WIDTH = 1600
DISPLAY_HEIGHT = 900

GRID_X = 0
GRID_Y = 0
GRID_W = 0.9 * DISPLAY_HEIGHT
GRID_H = 0.9 * DISPLAY_HEIGHT

PLAY_X = 0
PLAY_Y = GRID_H
PLAY_W = 100
PLAY_H = 0.1 * DISPLAY_HEIGHT

grid: Grid = Grid((50, 50), Rect(GRID_X, GRID_Y, GRID_W, GRID_H))

def toggle_play(sender: object):
    global playing
    if not playing:
        time.set_timer(EVENT_GAME_TICK, millis=100, loops=0)
        playing = True
        play_button.label = "Pause"
    else:
        time.set_timer(EVENT_GAME_TICK, millis=0)
        playing = False
        play_button.label = "Play"

play_button: Button = Button(Rect(PLAY_X, PLAY_Y, PLAY_W, PLAY_H), "Play", toggle_play)

def render(screen: Surface):
    grid.draw(screen)
    play_button.draw(screen)
    pygame.display.flip()

EVENT_UPDATE_DISPLAY = pygame.USEREVENT
EVENT_GAME_TICK = pygame.USEREVENT + 1

def main():
    pygame.init()
    pygame.display.set_caption("Game of Life")
    screen = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))

    time.set_timer(EVENT_UPDATE_DISPLAY, millis=33)

    global playing
    playing = False
     
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                grid.handle_click(event)
                play_button.handle_click(event)
            if event.type == (EVENT_UPDATE_DISPLAY):
                render(screen)
            if event.type == (EVENT_GAME_TICK):
                grid.update()
     
if __name__=="__main__":
    main()
