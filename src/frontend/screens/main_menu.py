class MainMenu:
    """Main menu screen shown at game start.

    Attributes:
        options: Labels of the menu entries, in display order.
        selected: Index of the currently highlighted option.
    """
    def __init__(self) -> None:
        self.options: tuple[str] = ["Start",
                                    "Highscores",
                                    "Instructions",
                                    "Exit"]
        self.selected: int = 0
