from abc import ABC, abstractmethod
from pygame import Rect
from pygame.event import Event

class ClickableRect(ABC):
    @property
    @abstractmethod
    def clickable(self) -> Rect:
        return self._clickable_rect

    def handle_click(self, event: Event):
        if self.clickable.collidepoint(event.pos):
            self._on_click(event)

    @abstractmethod
    def _on_click(self, event: Event):
        pass

