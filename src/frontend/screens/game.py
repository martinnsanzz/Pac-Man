# Built-in modules

# Installed modules
import pygame

# Local modules
from .screen import Screen
from .actions import ScreenAction
from ..assets import AssetsLoader
from ...models import GameConfig, Maze
from ..maze_renderer import MazeRenderer
from ..hud import HUD


class Game(Screen):
    """Game screen that will run all the core pac-man logic."""

    def __init__(self, screen_w: int, screen_h: int,
                 assets: AssetsLoader, config: GameConfig) -> None:
        super().__init__(screen_w, screen_h, assets)
        self.config = config
        self.maze = Maze()
        self.maze_renderer = MazeRenderer(self.maze.grid, assets,
                                          screen_w, screen_h)
        self.hud = HUD(assets)

        self.lives = config.lives
        self.score = 0
        self.highscore = 0  # Needs replacement with highscore backend
        self.time_left = config.level_time_limit

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
        self.maze_renderer.render_maze(surface)
        self.hud.display_hud(surface, self.lives, self.score,
                             self.highscore, self.time_left)
