# Built-in modules

# Installed modules
import pygame

# Local modules
from .screen import Screen, ScreenAction
from ..assets import AssetsLoader, Fruit
from ..maze_renderer import MazeRenderer
from ..hud import HUD
from ...models import GameConfig
from ...backend import MazeGen


class Game(Screen):
    """Game screen that will run all the core pac-man logic."""
    SQUARE_SIZE = 40
    SQUARE_SPEED = 200            # pixels per second
    SQUARE_COLOR = (255, 255, 0)

    def __init__(self, screen_w: int, screen_h: int,
                 assets: AssetsLoader, config: GameConfig,
                 highscore: int) -> None:
        super().__init__(screen_w, screen_h, assets)
        self.config = config
        self.assets = assets
        self.maze = MazeGen()
        self.maze_renderer = MazeRenderer(self.maze.grid, assets,
                                          screen_w, screen_h)
        self.hud = HUD(assets)

        self.lives = config.lives
        self.score = 0
        self.highscore = highscore
        self.time_left = config.level_time_limit
        self.fruits_collected: list[Fruit] = []

        self.square_x = 0.0
        self.square_y = screen_h // 2
        self.square_dir = 1       # 1 = right, -1 = left
        self.max_x = screen_w - self.SQUARE_SIZE
        self.pacman_right = assets.sprites["PAC_MAN"]
        self.pacman_left = pygame.transform.flip(self.pacman_right,
                                                 True, False)

    def handle_event(self, event: pygame.event.Event) -> ScreenAction:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return ScreenAction.PAUSE
            elif event.key == pygame.K_t:
                return ScreenAction.TEXT_BOX
            elif event.key == pygame.K_q:  # TEMP TO BE DELETED
                return ScreenAction.QUIT
        return ScreenAction.NONE

    def update(self, dt: float) -> None:
        """Move the square and bounce it off both edges."""
        self.square_x += self.square_dir * self.SQUARE_SPEED * dt

        if self.square_x >= self.max_x:
            self.square_x = self.max_x
            self.square_dir = -1
            pygame.transform.flip(self.assets.sprites["PAC_MAN"], True, False)
        elif self.square_x <= 0:
            self.square_x = 0
            self.square_dir = 1
            pygame.transform.flip(self.assets.sprites["PAC_MAN"], False, False)

    def draw(self, surface: pygame.Surface) -> None:
        self.maze_renderer.render_maze(surface)
        sprite = self.pacman_right if self.square_dir == 1 \
            else self.pacman_left
        surface.blit(sprite, (int(self.square_x), self.square_y))
        self.hud.display_hud(surface, self.lives, self.fruits_collected,
                             self.score, self.highscore, self.time_left)
