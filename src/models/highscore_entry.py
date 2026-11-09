# Installed modules
from pydantic import BaseModel, Field

VALID_NAME_RE = r"^[A-Za-z0-9][A-Za-z0-9 ]*$"


class HighscoreEntry(BaseModel):
    """A single highscore record with a validated player name and score.

    Attributes:
        name: Player name, 1 to 10 characters, letters, digits and spaces only
            and it can't start with a space.
        score: Points scored in the game, a non-negative integer.
    """
    name: str = Field(max_length=10, pattern=VALID_NAME_RE)
    score: int = Field(ge=0)
