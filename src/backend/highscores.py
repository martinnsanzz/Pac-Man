# Built-in modules
from pathlib import Path
import json

# Installed modules
from pydantic import ValidationError

# Local modules
from ..models import HighscoreEntry
from ..exceptions import PacManError

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

        A missing file leaves the table empty. An unreadable or invalid
        file also empties the table, then raises.

        Raises:
            PacManError: If it is not possible to load highscore file.
        """
        try:
            with open(self.path, "r") as file:
                data = json.load(file)
                entries: list[HighscoreEntry] = []
                for entry in data:
                    # ** unpacks the dict
                    entries.append(HighscoreEntry(**entry))
                self.table = entries
            self.table.sort(key=lambda entry: entry.score, reverse=True)
            self.table = self.table[:MAX_ENTRIES]
        except FileNotFoundError:
            self.table = []
        except (OSError, ValueError, TypeError) as e:
            self.table = []
            raise PacManError(f"Could not load '{self.path}': {e}.")

    def save(self) -> None:
        """Write the current table to the file as JSON.

        Raises:
            PacManError: If the file can't be written.
        """
        data: list[dict[str, str | int]] = []
        for entry in self.table:
            data.append(entry.model_dump())

        try:
            with open(self.path, "w") as file:
                json.dump(data, file, indent=4)
        except OSError as e:
            raise PacManError(f"Could not save highscores to '{self.path}':"
                              f" {e}.")

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
