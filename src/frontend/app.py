# Installed modules
import pygame

# Local modules
from .screens import MainMenu, Action


# window
WIDTH = 672
HEIGHT = 864


class App:
    """Pygame window that plays the game and handles user input.

    Attributes:
        clock: pygame clock.
        screen: Pygame window to hold the drawings.
        current_screen: Current menu or window to be displayed.
    """
    def __init__(self) -> None:
        """Open the window and load the main menu."""
        # ---------- pygame controls ----------
        pygame.init()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.current_screen = MainMenu()

    def run(self) -> None:
        """Run the main loop until the window is closed.

        Each frame handles key presses and redraws the window.
        """
        running = True
        while running:
            # control block
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                action = self.current_screen.handle_event(event)
                if action is Action.QUIT:
                    running = False
            # time block

            # drawing block

        pygame.quit()
