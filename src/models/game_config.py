# Built-in modules
from math import inf

# Installed modules
from pydantic import BaseModel, Field, PositiveInt, field_validator


class GameConfig(BaseModel):
    """Validated game settings loaded from the configuration file.

    Every field has a default, so a partial configuration is accepted.
    Values outside the documented bounds raise a validation error.

    Attributes:
        highscore_filename: Name of the file used to store the high score.
            Must end with ``.txt``.
        lives: Number of lives the player starts with (1 to 10).
        total_pacgum: Total number of pac-gums (1 to 100).
        pacgum_points: Points awarded per pac-gum (1 to 100).
        super_pacgum_points: Points awarded per super pac-gum (1 to 500).
        ghost_points: Points awarded per ghost (1 to 2000).
        level_time_limit: Time limit of a level (1 to 1000).
        retro_shader: Whether the retro shader is enabled. Accepted in the
            configuration as ``"on"`` or ``"off"``.
    """

    highscore_filename: str = Field(default="highscore.txt")
    lives: PositiveInt = Field(default=3, gt=0, le=10)
    total_pacgum: PositiveInt = Field(default=42, gt=0, le=100)
    pacgum_points: PositiveInt = Field(default=10, le=100)
    super_pacgum_points: PositiveInt = Field(default=50, le=500)
    ghost_points: PositiveInt = Field(default=200, le=2000)
    level_time_limit: PositiveInt = Field(default=90, gt=0, le=1000)
    retro_shader: bool = Field(default=True) # 'on == true' and 'off == false' 

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
        raise ValueError(f"Incorrect mode for 'retro_shader'.\n"
                         "  - Accepted: 'on'/'off'")

    @field_validator("highscore_filename", mode="after")
    @classmethod
    def parse_highscore_file(cls, value: str) -> bool:
        """Validate that the high score file has a ``.txt`` extension.

        Args:
            value: File name already validated as a string.

        Returns:
            The unchanged file name.

        Raises:
            ValueError: If the file name does not end with ``.txt``.
        """
        if value.endswith(".txt"):
            return value
        raise ValueError(f"Highscore file must be '.txt' file.\n"
                         f" - File name provided: {value}")