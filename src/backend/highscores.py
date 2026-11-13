# Built-in modules
from pathlib import Path
import json

# Installed modules
from pydantic import ValidationError

# Local modules
from ..models import HighscoreEntry
from ..exceptions import HighScoreError

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
            HighScoreError: If it is not possible to load highscore file.
        """
        try:
            raw = json.loads(self.path.read_text())
            entries = [HighscoreEntry.model_validate(item) for item in raw]
        except FileNotFoundError:
            self.table = []
        except (OSError, ValueError, TypeError) as e:
            self.table = []
            raise HighScoreError(f"Could not load '{self.path}': {e}.") from e
        else:
            self.table = entries
            self._sort_and_trim()

    def save(self) -> None:
        """Write the current table to the file as JSON.

        Raises:
            HighScoreError: If the file can't be written.
        """
        data = [entry.model_dump() for entry in self.table]
        try:
            self.path.write_text(json.dumps(data, indent=4))
        except OSError as e:
            raise HighScoreError(
                f"Could not save highscores to '{self.path}': {e}."
            ) from e

    def insert(self, name: str, score: int) -> bool:
        """Add a score to the table if it makes the top MAX_ENTRIES.

        Args:
            name: Player name, validated by HighscoreEntry.
            score: Points scored, a non-negative integer.

        Returns:
            True if the entry was added, False otherwise.
        """
        try:
            entry = HighscoreEntry(name=name, score=score)
        except ValidationError:
            return False
        if not self.is_highscore(score):
            return False
        self.table.append(entry)
        self._sort_and_trim()
        return True

    def get_high_score(self) -> int:
        """Return the highest score in the table.

        Returns:
            The highest ``score`` among all entries, or 0 if the table is
            empty.
        """
        return max((entry.score for entry in self.table), default=0)

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

    def _sort_and_trim(self) -> None:
        """Keep the table sorted high to low and at most MAX_ENTRIES long."""
        self.table.sort(key=lambda entry: entry.score, reverse=True)
        del self.table[MAX_ENTRIES:]
