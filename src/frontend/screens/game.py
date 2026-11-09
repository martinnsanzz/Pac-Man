# Built-in modules

# Installed modules
import pygame
from mazegen import MazeGenerator

# Local modules
from .screen import Screen
from .actions import ScreenAction
from .pause import Pause
from ..assets import AssetsLoader


class Game(Screen):
    """Game screen that will run all the core pac-man logic."""

    def __init__(self, screen_w: int, screen_h: int,
                 assets: AssetsLoader) -> None:
        super().__init__(screen_w, screen_h, assets)

    def handle_event(self, event: pygame.event.Event) -> ScreenAction:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return ScreenAction.PAUSE
            elif event.key == pygame.K_t:
                return ScreenAction.TEXT_BOX
            elif event.key == pygame.K_q: # TEMP TO BE DELETED
                return ScreenAction.QUIT
        return ScreenAction.NONE

    def draw(self, surface: pygame.Surface) -> None:
        ...

    # def generate_maze(self) -> list[list[int]]:
    #     maze = MazeGenerator(10, 10, (0, 0), (9, 9), False)
    #     maze.generate()
    #     return maze.maze