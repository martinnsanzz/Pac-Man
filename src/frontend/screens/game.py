# Built-in modules

# Installed modules
import pygame
from mazegen import MazeGenerator

# Local modules
from .screen import Screen
from .actions import ScreenAction
from ..assets import AssetsLoader


class Game(Screen):
    """Game screen that will run all the core pac-man logic."""

    def __init__(self, screen_w: int, screen_h: int,
                 assets: AssetsLoader) -> None:
        super().__init__(screen_w, screen_h, assets)
        self.level = self.generate_maze()

    def handle_event(self, event: pygame.event.Event) -> ScreenAction:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return ScreenAction.PAUSE
            elif event.key == pygame.K_t:
                return ScreenAction.TEXT_BOX
            elif event.key == pygame.K_q:  # TEMP TO BE DELETED
                return ScreenAction.QUIT
        return ScreenAction.NONE

    def draw(self, surface: pygame.Surface) -> None:
        pix_y = 0
        for x, col in enumerate(self.level):
            pix_x = 0
            for y, val in enumerate(col):
                surface.blit(self.assets.tiles[val], (pix_x, pix_y))

                if x == len(self.level) // 2 and y == len(col) // 2:
                    surface.blit(self.assets.sprites["PAC_MAN"],
                                 (pix_x + 7, pix_y + 7))

                pix_x += self.assets.TILE * self.assets.SCALE

            pix_y += self.assets.TILE * self.assets.SCALE

    def generate_maze(self) -> list[list[int]]:
        generator = MazeGenerator(15, 15, (0, 0), (1, 1), False)
        generator.generate()
        maze: list[list[int]] = generator.maze
        return maze
