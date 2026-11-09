# Built-in modules
from pathlib import Path
import json

# Installed modules
from pydantic import ValidationError

# Local modules
from ..models.highscore_entry import HighscoreEntry

MAX_ENTRIES = 10


class Highscores:
    """Top-10 highscore table stored in a JSON file.

    Attributes:
        table: Entries sorted from highest to lowest score
            at most MAX_ENTRIES long.
        path: Location of the highscore JSON file.
    """
    def __init__(self, path: Path) -> None:
        self.table: list[HighscoreEntry] = []
        self.path: Path = path

    def load(self) -> None:
        """Load the table from the file.

        A missing or invalid file leaves the table empty instead
        of raising an error.
        """
        ...

    def save(self) -> None:
        """Write the current table to the file as JSON."""
        data: list[dict[str, str | int]] = []
        for entry in self.table:
            data.append(entry.model_dump())

        try:
            with open(self.path, "w") as file:
                json.dump(data, file, indent=4)
        except OSError:
            # TODO: Decide what should happen after a fail
            pass

    def insert(self, name: str, score: int) -> bool:
        """Add a score to the table if it makes the top MAX_ENTRIES.

        Args:
            name: Player name, validated by HighscoreEntry.
            score: Points scored, a non-negative integer.

        Returns:
            True if the entry was added, False otherwise.
        """
        if not self.is_highscore(score):
            return False
        try:
            entry = HighscoreEntry(name=name, score=score)
        except ValidationError:
            return False
        self.table.append(entry)
        self.table.sort(key=lambda entry: entry.score, reverse=True)
        self.table = self.table[:MAX_ENTRIES]
        return True

    def is_highscore(self, score: int) -> bool:
        """Check whether a score would make it into the table.

        Args:
            score: Points scored in the finished game.

        Returns:
            True if the table isn't full or the score beats the lowest entry.
        """
        if len(self.table) < MAX_ENTRIES:
            return True
        return score > self.table[-1].score
