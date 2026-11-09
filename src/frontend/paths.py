# Built-in modules
from pathlib import Path

# Path to the root of the project
ROOT = Path(__file__).resolve().parents[2]

# Assets folder within the project
ASSETS = ROOT / "assets"

# Fonts folder
FONTS = ASSETS / "fonts"

class FontsPaths():
    CRACKMAN = (FONTS / "Crackman").with_suffix(".TTF")
    ARCADECLASSIC = (FONTS / "ARCADECLASSIC").with_suffix(".TTF")
    ARCADE = (FONTS / "ARCADE").with_suffix(".TTF")


class SpritesPaths():
    PAC_MAN = (ASSETS / "player" / "PacMan-Anim").with_suffix(".gif")
    TILEMAP = (ASSETS / "tilemap" / "tilemap").with_suffix(".png")
