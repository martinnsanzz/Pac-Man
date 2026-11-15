# Built-in modules
from enum import Enum

MAX_LENGTH = 8


class Cheat(Enum):
    """Cheats that can be activated by typing their code.

    Each member's value is the code the player must type.
    """
    IMMORTAL = "IMMORTAL"
    SKIPZONE = "SKIPZONE"
    MORELIFE = "MORELIFE"
    ZOOMZOOM = "ZOOMZOOM"
    FREEZEUP = "FREEZEUP"
    SUPERPAC = "SUPERPAC"
    NOCHEATS = "NOCHEATS"


class CheatCodes:
    """Typed cheat code input and the set of active cheats.

    Toggle cheats stay active until typed again or cleared with NOCHEATS.
    One-shot cheats are never stored, they are returned by ``submit()``
    for the game to apply once.

    Attributes:
        text: Characters types so far, at most MAX_LENGHT long.
        active: Toggle cheats that are currently on.
    """
    ONE_SHOTS: frozenset[Cheat] = frozenset([Cheat.SKIPZONE,
                                             Cheat.MORELIFE,
                                             Cheat.NOCHEATS,
                                             Cheat.SUPERPAC])

    def __init__(self) -> None:
        self.text: str = ""
        self.active: set[Cheat] = set()

    def add_char(self, char: str) -> None:
        """Append a typed character to the current text.

        Characters past MAX_LENGTH are ignored.

        Args:
            char: A single typed character.
        """
        if len(self.text) >= MAX_LENGTH:
            return
        elif (char.isalpha() and char.isascii()) or char == "/":
            self.text += char.upper()

    def backspace(self) -> None:
        """Remove the last typed character, if any."""
        self.text = self.text[:-1]

    def submit(self) -> Cheat | None:
        """Check the typed text against the codes, then clear it.

        A valid toggle cheat is switched on or off. NOCHEATS turns every
        toggle off.

        Returns:
            The matched cheat or None if the text is not a valid code.
        """
        text = self.text
        self.text = ""
        try:
            cheat = Cheat(text)
        except ValueError:
            return None

        if cheat is Cheat.NOCHEATS:
            self.active.clear()
        elif cheat not in self.ONE_SHOTS:
            if cheat not in self.active:
                self.active.add(cheat)
            else:
                self.active.discard(cheat)
        return cheat

    def is_active(self, cheat: Cheat) -> bool:
        """Check whether a toggle cheat is currently on.

        Args:
            cheat: The cheat to check.

        Returns:
            True if the cheat is active, False otherwise.
        """
        return cheat in self.active
