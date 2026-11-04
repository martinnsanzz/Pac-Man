class MainMenu:
    """Main menu screen shown at game start.

    Attributes:
        options: Labels of the menu entries, in display order.
        selected: Index of the currently highlighted option.
    """
    def __init__(self) -> None:
        self.options: tuple[str, ...] = ("Start",
                                         "Highscores",
                                         "Instructions",
                                         "Exit")
        self.selected: int = 0

    def navigate(self, step: int) -> None:
        """Move the selection by `step`.

        Args:
            step: Offset to add to the current position (negative moves up,
                positive moves down).
        """
        self.selected += step
        if self.selected < 0:
            self.selected = 0
        elif self.selected >= len(self.options):
            self.selected = len(self.options) - 1
