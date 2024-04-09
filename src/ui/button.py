import os
from typing import Callable
from pygame import Color, Rect, Surface, draw
import pygame
from pygame.event import Event
from core.clickable_rect import ClickableRect

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Button(ClickableRect):
    def __init__(self, rect: Rect, 
                 label: str = "", 
                 on_click: Callable[[object], None] | None = None):
        self._rect = rect
        self._label = label
        self._on_click = on_click

    @property
    def rect(self) -> Rect:
        return self._rect

    @rect.setter
    def rect(self, value: Rect):
        self._rect = value

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, value: str):
        self._label = value

    @property
    def on_click(self) -> Callable[[], None] | None:
        return self._on_click

    @on_click.setter
    def on_click(self, value: Callable[[], None] | None):
        self._on_click = value

    @property
    def clickable(self) -> Rect:
        return self._rect

    def draw(self, surface: Surface):
        border_color = Color('#404040')
        border_width = 2

        color = Color('#737373')
        innerRect = Rect(self._rect.x + border_width,
                         self._rect.y + border_width,
                         self._rect.w - border_width,
                         self._rect.h - border_width)

        label_color = Color('#FFFFFF')
        font = pygame.font.Font(ROOT_DIR + '/../assets/fonts/Roboto/Roboto-Medium.ttf', 18)
        label_text = font.render(self._label, False, label_color)
        label_rect = label_text.get_rect()
        label_rect.center = self._rect.center

        draw.rect(surface, border_color, self._rect)
        draw.rect(surface, color, innerRect)
        surface.blit(label_text, label_rect)

    def on_click(self, event: Event):
        if (self._on_click):
            self._on_click(self)

    def _on_click(self, event: Event):
        self.on_click()
