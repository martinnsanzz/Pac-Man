# Built-in modules
from pathlib import Path

# Installed modules
from pydantic import BaseModel, Field, PositiveInt, field_validator


class GameConfig(BaseModel):
    """Validated game settings loaded from the configuration file.

    Every field has a default, so a partial configuration is accepted.
    Values outside the documented bounds raise a validation error.

    Attributes:
        highscore_path: Name of the file used to store the high score.
            Must end with ``.json``.
        lives: Number of lives the player starts with (1 to 10).
        total_pacgum: Total number of pac-gums (1 to 100).
        pacgum_points: Points awarded per pac-gum (1 to 100).
        super_pacgum_points: Points awarded per super pac-gum (1 to 500).
        ghost_points: Points awarded per ghost (1 to 2000).
        level_time_limit: Time limit of a level (1 to 1000).
        retro_shader: Whether the retro shader is enabled. Accepted in the
            configuration as ``"on"`` or ``"off"``.
    """

    highscores_path: str = Field(default="data/highscores.json")
    lives: PositiveInt = Field(default=3, gt=0, le=10)
    total_pacgum: PositiveInt = Field(default=42, gt=0, le=100)
    pacgum_points: PositiveInt = Field(default=10, le=100)
    super_pacgum_points: PositiveInt = Field(default=50, le=500)
    ghost_points: PositiveInt = Field(default=200, le=2000)
    level_time_limit: PositiveInt = Field(default=90, gt=0, le=1000)
    retro_shader: bool = Field(default=True)

    @field_validator("retro_shader", mode="before")
    @classmethod
    def parse_shader(cls, value: str) -> bool:
        """Convert the ``"on"``/``"off"`` setting to a boolean.

        Runs before Pydantic's own validation, on the raw input value.

        Args:
            value: Raw configuration value, expected to be ``"on"`` or
                ``"off"``.

        Returns:
            True for ``"on"``, False for ``"off"``.

        Raises:
            ValueError: If the value is neither ``"on"`` nor ``"off"``.
        """
        if value == "on":
            return True
        elif value == "off":
            return False
        raise ValueError("Incorrect mode for 'retro_shader'.\n"
                         "  - Accepted: 'on'/'off'")

    @field_validator("highscores_path", mode="after")
    @classmethod
    def validate_highscores_path(cls, value: str) -> str:
        """Validate the high score file path.

        The path must be relative, stay inside ``data/``, end in ``.json``,
        and its file name must have a non-empty stem with no spaces.

        Args:
            value: Path already validated as a string.

        Returns:
            The unchanged path.

        Raises:
            ValueError: If any of the rules above is broken.
        """
        if not value.endswith(".json"):
            raise ValueError("Highscore file must end in '.json'.\n"
                             f" - Path provided: {value}")

        path = Path(value)
        if path.name == ".json":
            raise ValueError("Highscore file name is empty.\n"
                             f" - Path provided: {value}")
        if " " in path.name:
            raise ValueError("Found invalid space in highscore file name.\n"
                             f" - Path provided: {value}")
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("Highscore path must be relative and cannot "
                             f"contain '..'.\n - Path provided: {value}")
        if path.parts[0] != "data":
            raise ValueError("Highscore file must be inside 'data/'.\n"
                             f" - Path provided: {value}")
        return value
