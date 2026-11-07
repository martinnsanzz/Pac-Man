# Installed modules
import pygame

# Local modules
from .screens import MainMenu, Action, Screen


# Arcade screen
WIDTH = 672
HEIGHT = 864
FPS = 60


class App:
    """Pygame window that plays the game and handles user input.

    Attributes:
        clock: pygame clock.
        screen: Pygame window to hold the drawings.
        arcade_screen: Subwindow to hold arcade related drawings.
        current_screen: Current menu or window to be displayed.
        arcade_size: Arcade window scaled by the user screen.
    """
    def __init__(self) -> None:
        """Open the window and load the main menu."""
        # ---------- pygame controls ----------
        pygame.init()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        win_w, win_h = self.screen.get_size()

        # ---------- arcade screen ----------
        self.arcade_screen = pygame.Surface((WIDTH, HEIGHT))
        ratio_w = win_w / WIDTH
        ratio_h = win_h / HEIGHT
        arcade_factor = min(ratio_w, ratio_h)
        self.arcade_size = (int(WIDTH * arcade_factor),
                            int(HEIGHT * arcade_factor))

        self.current_screen: Screen = MainMenu()

    def run(self) -> None:
        """Run the main loop until the window is closed.

        Each frame handles key presses and redraws the window.
        """
        running = True
        while running:
            # ---------- control block ----------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                action = self.current_screen.handle_event(event)
                if action is Action.QUIT:
                    running = False
            # ---------- time block ----------

            # ---------- drawing block ----------
            self.screen.fill((0, 0, 0))
            self.arcade_screen.fill((12, 14, 16))
            self.current_screen.draw(self.arcade_screen)
            playable_surface = pygame.transform.scale(self.arcade_screen,
                                                      self.arcade_size)
            self.screen.blit(
                    playable_surface,
                    playable_surface.get_rect(
                        center=self.screen.get_rect().center))
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
