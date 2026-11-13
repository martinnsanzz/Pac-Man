# Built-in modules
from pathlib import Path

# Installed modules
import pygame

# Local modules
from .screens import (MainMenu, ScreenAction, Screen,
                      Instructions, Game, HighscoresTable, Pause)
from .paths import FontsPaths, SpritesPaths, TilemapPath
from .assets import AssetsLoader
from .terminal import TerminalPrinter
from ..exceptions import LoadAssetsError, PacManError
from ..models import GameConfig
from ..backend import Highscores


class App:
    """Pygame window that plays the game and handles user input.

    Attributes:
        game_config: Configuration of game extracted from config.json
        clock: pygame clock.
        screen: Pygame window to hold the drawings.
        main_menu: Main menu window to return to.
        arcade_screen: Subwindow to hold arcade related drawings.
        current_screen: Current menu or window to be displayed.
        arcade_size: Arcade window scaled by the user screen.
        highscores: Persistent highscore table, loaded at startup.
    """
    # Arcade screen
    WIDTH = 672
    HEIGHT = 864
    FPS = 60
    BACKGROUND = (12, 14, 16)

    def __init__(self, game_config: GameConfig) -> None:
        """Open the window, load the assets and highscore"""
        self.validate_assets()
        self.game_config = game_config

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = self._create_window()
        self.arcade_screen = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.arcade_size = self._compute_arcade_size()

        self.assets = AssetsLoader()
        self.assets.load()
        self.highscores = self._load_highscores()

        self.main_menu: Screen = MainMenu(self.WIDTH,
                                          self.HEIGHT,
                                          self.assets)
        self.current_screen: Screen = self.main_menu
        self.running = True

        self.game: Game | None = None

    @staticmethod
    def _create_window() -> pygame.Surface:
        """Open the resizable window and set its title."""
        pygame.display.set_caption("Pac-Man")
        return pygame.display.set_mode((0, 0), pygame.RESIZABLE)

    @staticmethod
    def validate_assets() -> None:
        """Raise LoadAssetsError listing every missing asset."""
        missing: list[str] = []
        for paths in (FontsPaths, SpritesPaths, TilemapPath):
            missing += paths.validate()
        if missing:
            raise LoadAssetsError(
                "Missing assets needed to run pac-man:\n - "
                + "\n - ".join(missing))

    def _load_highscores(self) -> Highscores:
        """Load the highscore table; on failure print the error and go on."""
        highscores = Highscores(Path(self.game_config.highscores_path))
        try:
            highscores.load()
        except PacManError as e:
            TerminalPrinter.print_error(f"{e}\n")
        return highscores

    def run(self) -> None:
        """Run the main loop until the window is closed."""
        while self.running:
            dt = self.clock.tick(self.FPS) / 1000
            self._handle_events()
            self._update(dt)
            self._draw()
        pygame.quit()

    def _compute_arcade_size(self) -> tuple[int, int]:
        """Return the arcade size scaled to fit the window."""
        win_w, win_h = self.screen.get_size()
        factor = min(win_w / self.WIDTH, win_h / self.HEIGHT)
        return int(self.WIDTH * factor), int(self.HEIGHT * factor)

    def _switch(self, action: ScreenAction) -> None:
        """Change the current screen according to the action."""
        match action:
            case ScreenAction.QUIT:
                self.running = False
            case ScreenAction.BACK:
                self.current_screen = self.main_menu
            case ScreenAction.MAIN_MENU:
                self.current_screen = self.main_menu
            case ScreenAction.START_GAME:
                self.game = Game(self.WIDTH, self.HEIGHT,
                                 self.assets, self.game_config,
                                 self.highscores.get_high_score())
                self.current_screen = self.game
            case ScreenAction.HIGHSCORES:
                self.current_screen = HighscoresTable(self.WIDTH, self.HEIGHT,
                                                      self.assets,
                                                      self.highscores)
            case ScreenAction.INSTRUCTIONS:
                self.current_screen = Instructions(self.WIDTH, self.HEIGHT,
                                                   self.assets)
            case ScreenAction.PAUSE:
                if self.game:
                    self.current_screen = Pause(self.WIDTH, self.HEIGHT,
                                                self.assets, self.game)
            case ScreenAction.RESUME:
                if self.game:
                    self.current_screen = self.game
            case _:
                pass

    def _handle_events(self) -> None:
        """Read the pygame events and forward them to the screen."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.arcade_size = self._compute_arcade_size()
            self._switch(self.current_screen.handle_event(event))

    def _draw(self) -> None:
        """Draw the current screen scaled and centered in the window."""
        self.screen.fill((0, 0, 0))
        self.arcade_screen.fill(self.BACKGROUND)
        self.current_screen.draw(self.arcade_screen)
        scaled = pygame.transform.scale(self.arcade_screen, self.arcade_size)
        self.screen.blit(
            scaled, scaled.get_rect(center=self.screen.get_rect().center))
        pygame.display.flip()

    def _update(self, dt: float) -> None:
        """Advance the current screen by dt seconds."""
        self.current_screen.update(dt)
