# Built-in modules
from pathlib import Path
import json

# Installed modules
from pydantic import ValidationError

# Local modules
from ..validation import HighscoreEntry
from ..exceptions import HighScoreError

MAX_ENTRIES = 10
DEFAULT_ERROR = "Creating a new highscore file"


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
        """Load the table from the highscores file.

        On success the table holds the file's entries, sorted and trimmed.
        On any failure the table is left empty and HighScoreError is
        raised.

        Raises:
            HighScoreError: If the file is missing or unreadable, is not
                valid JSON, has the wrong structure, or contains entries
                that fail validation.
        """
        try:
            raw = json.loads(self.path.read_text())
            entries = [HighscoreEntry.model_validate(item) for item in raw]
        except OSError:
            raise HighScoreError(f"No '{self.path}' found. {DEFAULT_ERROR}")
        except ValidationError as e:
            msgs = [
                f"{'.'.join(map(str, err['loc'])) or 'config'}: "
                f"{err['msg'].removeprefix('Value error, ')}"
                for err in e.errors()
            ]
            details = "\n".join(f"- {msg}" for msg in msgs)
            raise HighScoreError(f"Could not load '{self.path}':\n"
                                 f"{details}.\n{DEFAULT_ERROR}") from e
        except (ValueError, TypeError) as e:
            raise HighScoreError(f"Incorrect 'json' format on '{self.path}':\n"
                                 f" -{e}.\n{DEFAULT_ERROR}") from e
        finally:
            self.table = []
        self.table = entries
        self._sort_and_trim()

    def save(self) -> None:
        """Write the current table to the file as JSON, one entry per line.

        Raises:
            HighScoreError: If the file can't be written.
        """
        lines = [json.dumps(entry.model_dump()) for entry in self.table]
        body = ",\n".join(f"    {line}" for line in lines)
        text = f"[\n{body}\n]\n" if lines else "[]\n"

        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(text)
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
            False if the score is 0 or less or the score doesn't beat the
            lowest entry.
        """
        if score <= 0:
            return False
        elif len(self.table) < MAX_ENTRIES:
            return True
        return score > self.table[-1].score

    def _sort_and_trim(self) -> None:
        """Keep the table sorted high to low and at most MAX_ENTRIES long."""
        self.table.sort(key=lambda entry: entry.score, reverse=True)
        del self.table[MAX_ENTRIES:]
