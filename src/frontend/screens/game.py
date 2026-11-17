# Built-in modules

# Installed modules
import pygame

# Local modules
from .screen import Screen, ScreenAction
from ..assets import AssetsLoader, Fruit
from ..maze_renderer import MazeRenderer
from ..hud import HUD
from ...validation import GameConfig
from ...backend import Level


class Game(Screen):
    """Game screen that will run all the core pac-man logic."""

    # Temp square (to be deleted)
    SQUARE_SIZE = 40
    SQUARE_SPEED = 200            # pixels per second
    SQUARE_COLOR = (255, 255, 0)

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------
    def __init__(self, screen_w: int, screen_h: int,
                 assets: AssetsLoader, config: GameConfig,
                 highscore: int) -> None:
        super().__init__(screen_w, screen_h, assets)
        self.config = config
        self.assets = assets
        self.hud = HUD(assets)
        self.maze_renderer = MazeRenderer(assets, screen_w, screen_h)

        # Persists across levels
        self.last_level = config.total_levels
        self.current_level = 1
        self.lives = config.lives
        self.score = 0
        self.highscore = highscore
        self.fruits_collected: list[Fruit] = [Fruit.APPLE] * 7  # temp

        # Thrown away and rebuilt every level
        self.level = Level(self.config, self.current_level)

        #  temp to be deleted
        self.square_x = 0.0
        self.square_y = screen_h // 2
        self.square_dir = 1       # 1 = right, -1 = left
        self.max_x = screen_w - self.SQUARE_SIZE
        self.pacman_right = assets.sprites["PAC_MAN"]
        self.pacman_left = pygame.transform.flip(self.pacman_right,
                                                 True, False)

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------
    def handle_event(self, event: pygame.event.Event) -> ScreenAction:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return ScreenAction.PAUSE
            #  temp to be deleted
            elif event.key == pygame.K_1:
                self.score += 100
            elif event.key == pygame.K_9:
                return self._advance_level()
            elif event.key == pygame.K_8:
                self.level.decrease_time()
        return ScreenAction.NONE

    def _advance_level(self) -> ScreenAction:
        """Go to the next level, or win if the last one was just cleared."""
        if self.current_level >= self.last_level:
            return ScreenAction.WIN
        self.current_level += 1
        self.level = Level(self.config, self.current_level)
        return ScreenAction.NONE

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------
    def update(self, dt: float) -> ScreenAction:
        """Move the square and bounce it off both edges."""
        #  temp to be deleted
        self._move_square(dt)

        return self._check_game_status()

    def _check_game_status(self) -> ScreenAction:
        if self.level.time_left <= 0:
            return ScreenAction.GAME_OVER
        return ScreenAction.NONE

    def _move_square(self, dt: float) -> None:
        """Temp: move the square and flip its sprite at the edges."""
        self.square_x += self.square_dir * self.SQUARE_SPEED * dt

        if self.square_x >= self.max_x:
            self.square_x = self.max_x
            self.square_dir = -1
            pygame.transform.flip(self.assets.sprites["PAC_MAN"], True, False)
        elif self.square_x <= 0:
            self.square_x = 0
            self.square_dir = 1
            pygame.transform.flip(self.assets.sprites["PAC_MAN"], False, False)

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------
    def draw(self, surface: pygame.Surface) -> None:
        self._draw_level(surface)
        sprite = self.pacman_right if self.square_dir == 1 \
            else self.pacman_left
        surface.blit(sprite, (int(self.square_x), self.square_y))
        self.hud.display_hud(surface, self.lives, self.fruits_collected,
                             self.score, self.highscore, self.level.time_left,
                             self.current_level, self.last_level)

    def _draw_level(self, surface: pygame.Surface) -> None:
        """Draw the maze of the current level."""
        self.maze_renderer.render_maze(surface, self.level.grid)
