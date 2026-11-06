# Built-in modules
from typing import Any

# Installed modules
from pydantic import ValidationError

# Local modules
from ..models import GameConfig
from ..exceptions import PacManError


def parse_game_config(config: dict[str, Any]) -> GameConfig:
    """Validate a raw configuration dictionary as a ``GameConfig``.

    Unknown keys are ignored. Only the first validation error is reported.

    Args:
        config: Raw configuration data, as returned by ``load_json``.

    Returns:
        The validated game configuration.

    Raises:
        PacManError: If any value fails validation. The message names the
            first invalid field and the reason.
    """
    try:
        return GameConfig.model_validate(config, extra="ignore")
    except ValidationError as e:
        var = e.errors()[0]["loc"][0]
        msg = e.errors()[0]["msg"].removeprefix("Value error, ")

        raise PacManError(f"Invalid value on '{var}':\n"
                          f"    {msg}") from e
