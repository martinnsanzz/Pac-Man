# Built-in modules
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .cheat_codes import CheatCodes

# Local modules
from .enums import LogKind


@dataclass
class LogEntry:
    """A single line shown in the dev log.

    Attributes:
        text: The message to display.
        kind: Category of the message.
    """
    text: str
    kind: LogKind


class DevLog:
    """Message history and input line of the dev log panel.

    Stores the messages shown on screen and the text currently being typed.
    It does not interpret the text, the caller decides what a submitted line
    means (cheat code, message, ...).

    Attributes:
        entries: Logged messages, oldest first, at most MAX_ENTRIES.
        text: Characters typed so far in the input line.
    """

    MAX_ENTRIES = 100   # oldest entries are dropped beyond this

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------
    def __init__(self) -> None:
        """Create an empty log with an empty input line."""
        self.entries: list[LogEntry] = []
        self.text: str = ""

    # ------------------------------------------------------------------
    # Log entries
    # ------------------------------------------------------------------
    def add(self, text: str, kind: LogKind) -> None:
        """Append a message to the log.

        When the log grows past MAX_ENTRIES the oldest entry is dropped.

        Args:
            text: The message to display.
            kind: Category of the message.
        """
        self.entries.append(LogEntry(text, kind))
        if len(self.entries) > self.MAX_ENTRIES:
            self.entries.pop(0)

    # ------------------------------------------------------------------
    # Input line
    # ------------------------------------------------------------------
    def add_char(self, char: str) -> None:
        """Append a typed character to the input line.

        Non-printable characters are ignored.

        Args:
            char: A single typed character.
        """
        if char and char.isprintable():
            self.text += char

    def backspace(self) -> None:
        """Remove the last typed character, if there is one."""
        self.text = self.text[:-1]

    def submit(self) -> str:
        """Return the typed text and clear the input line.

        Leading and trailing spaces are stripped.

        Returns:
            The submitted text or an empty string if nothing was typed.
        """
        text = self.text.strip()
        self.text = ""
        return text

    # ------------------------------------------------------------------
    # Command handling
    # ------------------------------------------------------------------
    def process(self, cheats: "CheatCodes") -> None:
        """Submit the input line and log the result.

        Text starting with ``/`` is checked as a cheat code and logged as
        ``CHEAT`` feedback, or as a ``WARNING`` if the code is unknown.
        Any other text is logged as a ``MESSAGE``. Empty input does
        nothing.

        Args:
            cheats: Cheat codes used to check and apply ``/`` commands.
        """
        text = self.submit()
        if text == "":
            return
        elif not text.startswith("/"):
            self.add(text, LogKind.MESSAGE)
        else:
            cheat = cheats.submit(text)
            if cheat is None:
                self.add(f"Unknown code: {text}", LogKind.WARNING)
            else:
                self.add(cheats.feedback(cheat), LogKind.CHEAT)
