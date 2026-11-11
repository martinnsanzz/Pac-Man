# Built-in modules

# Installed modules
import pygame
from mazegen import MazeGenerator

# Local modules
from .screen import Screen
from .actions import ScreenAction
from ..assets import AssetsLoader
from ...models import GameConfig


class Game(Screen):
    """Game screen that will run all the core pac-man logic."""

    def __init__(self, screen_w: int, screen_h: int,
                 assets: AssetsLoader, config: GameConfig) -> None:
        super().__init__(screen_w, screen_h, assets)
        self.level = self.generate_level_maze()
        self.lives = config.lives
        self.total_pacgum = config.total_pacgum
        self.pacgum_points = config.pacgum_points
        self.super_pacgum_points = config.super_pacgum_points
        self.ghost_points = config.ghost_points
        self.level_time_limit = config.level_time_limit

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
        self.display_level_maze(surface)

    def display_hud(self, surface: pygame.Surface) -> None:
        ...

    def display_level_maze(self, surface: pygame.Surface) -> None:
        tile = self.assets.TILE_PX
        start_x = (surface.get_width() - len(self.level[0]) * tile) // 2
        start_y = (surface.get_height() - len(self.level) * tile) // 2

        for row_i, row in enumerate(self.level):
            for col_i, val in enumerate(row):
                surface.blit(self.assets.tiles[val],
                            (start_x + col_i * tile, start_y + row_i * tile))

    def generate_level_maze(self) -> list[list[int]]:
        generator = MazeGenerator(19, 20, (0, 0), (1, 1), False)
        generator.generate()
        maze: list[list[int]] = generator.maze
        return maze
