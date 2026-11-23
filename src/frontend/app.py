# Built-in modules
from pathlib import Path

# Installed modules
import pygame

# Local modules
from .screens import (MainMenu, ScreenAction, Screen,
                      Instructions, Game, HighscoresTable, Pause,
                      GameOver, Win, EndMenu)
from .paths import FontsPaths, SpritesPaths, TilemapPath, SfxPaths, HudPaths
from .assets import AssetsLoader
from .terminal import TerminalPrinter
from ..constants import ARCADE_WIDTH, ARCADE_HEIGHT
from ..exceptions import LoadAssetsError, PacManError
from ..validation import GameConfig
from ..backend import Highscores


class App:
    """Pygame window that plays the game and handles user input.

    Attributes:
        game_config: Configuration of game extracted from config.json
        clock: Pygame clock.
        screen: Pygame window to hold the drawings.
        arcade_screen: Subwindow to hold arcade related drawings.
        arcade_size: Arcade window scaled by the user screen.
        assets: Loader holding every font, sprite and sound.
        highscores: Persistent highscore table, loaded at startup.
        main_menu: Main menu window to return to.
        current_screen: Current menu or window to be displayed.
        game: Running game, or None when no game is in progress.
        running: False once the main loop must stop.
    """
    FPS = 60
    BACKGROUND = (12, 14, 16)

    # Screens
    ENDMENUS: dict[ScreenAction, type[EndMenu]] = {
        ScreenAction.GAME_OVER: GameOver,
        ScreenAction.WIN: Win,
    }

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------
    def __init__(self, game_config: GameConfig) -> None:
        """Open the window, load the assets and highscore"""
        self.validate_assets()
        self.game_config = game_config

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = self._create_window()
        self.arcade_screen = pygame.Surface((ARCADE_WIDTH, ARCADE_HEIGHT))
        self.arcade_size = self._compute_arcade_size()

        self.assets = AssetsLoader()
        self.assets.load()
        self.highscores = self._load_highscores()

        self.main_menu: Screen = MainMenu(self.assets)
        self.current_screen: Screen = self.main_menu
        self.game: Game | None = None
        self.running = True
        self.on_dev_mode = False

    @staticmethod
    def validate_assets() -> None:
        """Raise LoadAssetsError listing every missing asset."""
        missing: list[str] = []
        for paths in (FontsPaths, SpritesPaths, TilemapPath, SfxPaths,
                      HudPaths):
            missing += paths.validate()
        if missing:
            raise LoadAssetsError(
                "Missing assets needed to run pac-man:\n - "
                + "\n - ".join(missing))

    @staticmethod
    def _create_window() -> pygame.Surface:
        """Open the resizable window, set its title and hide the cursor."""
        pygame.display.set_caption("Pac-Man")
        pygame.mouse.set_visible(False)
        return pygame.display.set_mode((0, 0), pygame.RESIZABLE)

    def _compute_arcade_size(self) -> tuple[int, int]:
        """Return the arcade size scaled to fit the window."""
        win_w, win_h = self.screen.get_size()
        factor = min(win_w / ARCADE_WIDTH, win_h / ARCADE_HEIGHT)
        return int(ARCADE_WIDTH * factor), int(ARCADE_HEIGHT * factor)

    def _load_highscores(self) -> Highscores:
        """Load the highscore table; on failure print the error and go on."""
        highscores = Highscores(Path(self.game_config.highscores_path))
        try:
            highscores.load()
        except PacManError as e:
            TerminalPrinter.print_error(f"{e}\n")
        return highscores

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self) -> None:
        """Run the main loop until the window is closed."""
        while self.running:
            dt = self.clock.tick(self.FPS) / 1000
            action = self._handle_events()
            if action == ScreenAction.NONE:
                action = self._update(dt)
            self._switch(action)
            self._draw()
        pygame.quit()

    def _handle_events(self) -> ScreenAction:
        """Forward events to the screen, return the first action it
        asked for."""
        action = ScreenAction.NONE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.arcade_size = self._compute_arcade_size()
            result = self.current_screen.handle_event(event)
            if action == ScreenAction.NONE:
                action = result
        return action

    def _update(self, dt: float) -> ScreenAction:
        """Advance the current screen by dt seconds."""
        return self.current_screen.update(dt)

    def _draw(self) -> None:
        """Draw the current screen scaled and centered in the window."""
        self.screen.fill((0, 0, 0))
        self.arcade_screen.fill(self.BACKGROUND)
        self.current_screen.draw(self.arcade_screen)
        scaled = pygame.transform.scale(self.arcade_screen, self.arcade_size)
        self.screen.blit(
            scaled, scaled.get_rect(center=self.screen.get_rect().center))
        pygame.display.flip()

    # ------------------------------------------------------------------
    # Screen switching
    # ------------------------------------------------------------------
    def _switch(self, action: ScreenAction | None) -> None:
        """Change the current screen according to the action."""
        match action:
            case ScreenAction.QUIT:
                self.highscores.save()
                self.running = False
            case ScreenAction.BACK | ScreenAction.MAIN_MENU:
                self._show_main_menu()
            case ScreenAction.START_GAME:
                self._start_game()
            case ScreenAction.HIGHSCORES:
                self._show_highscores()
            case ScreenAction.INSTRUCTIONS:
                self._show_instructions()
            case ScreenAction.PAUSE:
                self._show_pause()
            case ScreenAction.GAME_OVER | ScreenAction.WIN:
                self._show_end_menu(action)
            case ScreenAction.NAME_SUBMITTED:
                self._insert_high_score()
            case ScreenAction.DEV_MODE:
                self.on_dev_mode = True
                self._enter_dev_mode()
            case ScreenAction.RESUME:
                self._resume()

    def _show_main_menu(self) -> None:
        """Drop the current game and go back to the main menu."""
        self.game = None
        self.current_screen = self.main_menu

    def _start_game(self) -> None:
        """Create a new game and make it the current screen."""
        self.game = Game(self.assets, self.game_config,
                         self.highscores.get_high_score())
        self.current_screen = self.game

    def _show_highscores(self) -> None:
        """Show the highscore table."""
        self.current_screen = HighscoresTable(self.assets,
                                              self.highscores)

    def _show_instructions(self) -> None:
        """Show the instructions screen."""
        self.current_screen = Instructions(self.assets)

    def _show_pause(self) -> None:
        """Open the pause menu over the running game."""
        if self.game is None:
            return
        self.current_screen = Pause(ARCADE_WIDTH, ARCADE_HEIGHT, self.assets,
                                    self.game)

    def _show_end_menu(self, action: ScreenAction) -> None:
        """Open the game over or win menu over the finished game."""
        if self.game is None:
            return
        menu = self.ENDMENUS[action]
        is_highscore = self.highscores.is_highscore(self.game.score)
        self.current_screen = menu(ARCADE_WIDTH, ARCADE_HEIGHT, self.assets,
                                   self.game, is_highscore)

    def _insert_high_score(self) -> None:
        """Inserts current score to highscore if its valid"""
        if self.game is None or not isinstance(self.current_screen,
                                               EndMenu):
            return
        name = self.current_screen.name

        self.highscores.insert(name, self.current_screen.game.score)

    def _resume(self) -> None:
        """Close the pause menu and go back to the game."""
        if self.game is not None:
            self.current_screen = self.game

    def _enter_dev_mode(self) -> None:
        ...
