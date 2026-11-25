# Built-in modules
from enum import Enum


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
    """Typed cheat code and the set of active cheats.

    Toggle cheats stay active until typed again or cleared with NOCHEATS.
    One-shot cheats are never stored, they are returned by ``submit()``
    for the game to apply once.

    Attributes:
        active: Toggle cheats that are currently on.
    """
    ONE_SHOTS: frozenset[Cheat] = frozenset([Cheat.SKIPZONE,
                                             Cheat.MORELIFE,
                                             Cheat.NOCHEATS,
                                             Cheat.SUPERPAC])

    def __init__(self) -> None:
        self.active: set[Cheat] = set()

    def submit(self, text: str) -> Cheat | None:
        """Check the typed text against the codes.

        A valid toggle cheat is switched on or off. NOCHEATS turns every
        toggle off.

        Args:
            text: The typed code to be submitted.

        Returns:
            The matched cheat or None if the text is not a valid code.
        """
        if not text.startswith("/"):
            return None
        text = text.removeprefix("/")

        try:
            cheat = Cheat(text.upper())
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

    def feedback(self, cheat: Cheat) -> str:
        """Return the log message describing what a submitted cheat did.

        Args:
            cheat: The cheat that was submitted.

        Returns:
            "<CODE> used" for one-shots, otherwise "<CODE> ON"
            or "<CODE> OFF" depending on its status.
        """
        if cheat in CheatCodes.ONE_SHOTS:
            return f"<{cheat.name}> used"
        elif self.is_active(cheat):
            return f"<{cheat.name}> ON"
        else:
            return f"<{cheat.name}> OFF"
