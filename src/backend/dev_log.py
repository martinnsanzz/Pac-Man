# Built-in modules
from enum import Enum, auto
from dataclasses import dataclass


class LogKind(Enum):
    """Category of a log entry, used by the UI to pick its color."""
    INFO = auto()
    WARNING = auto()
    CHEAT = auto()
    MESSAGE = auto()


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

    MAX_ENTRIES = 100

    def __init__(self) -> None:
        self.entries: list[LogEntry] = []
        self.text: str = ""

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

    def add_char(self, char: str) -> None:
        """Append a typed character to the input line.

        Non-printable characters are ignored.

        Args:
            char: A single typed character.
        """
        if char and char.isprintable():
            self.text += char

    def backspace(self) -> None:
        """Remove the last typed character, if exists."""
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
