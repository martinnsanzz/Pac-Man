# Built-in modules
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "assets"
FONTS = ASSETS / "fonts"


class PathsBase():
    """Base class for groups of asset path constants.

    Subclasses declare `pathlib.Path` class attributes. Call `validate()` on
    a subclass to check that those files exist on disk.
    """
    @classmethod
    def validate(cls) -> list[str]:
        """Return a description of each missing path declared on the class.

        Inspect only the `Path` attributes defined directly on `cls`;
        attributes inherited from a parent class are not checked.

        Returns:
            A list of `"NAME: relative/path"` strings, one per path that does
            not exist, with the path relative to `ROOT` in POSIX form. The
            list is empty when every path exists.
        """
        return [f"{name}: {value.relative_to(ROOT).as_posix()}"
                for name, value in vars(cls).items()
                if isinstance(value, Path) and not value.exists()]


class FontsPaths(PathsBase):
    """Paths to the font files used by the game.

    Attributes:
        CRACKMAN: Path to the Crackman `.TTF` font.
        ARCADECLASSIC: Path to the ARCADECLASSIC `.TTF` font.
        ARCADEBUTTON: Path to the ARCADECLASSIC `.TTF` font.
        DIGITAL808: Path to the Digital808 `.TTF` font.
        BARCADE: Path to the barcadenobar `.ttf` font.
    """
    CRACKMAN = [(FONTS / "CRACKMAN" / "Crackman.TTF"), 100]
    ARCADECLASSIC = [(FONTS / "ARCADECLASSIC" / "ARCADECLASSIC.TTF"), 30]
    ARCADEBUTTON = [(FONTS / "ARCADECLASSIC" / "ARCADECLASSIC.TTF"), 38]
    DIGITAL808 = [(FONTS / "digital808" / "Digital808.TTF"), 18]
    BARCADE = [(FONTS / "barcade" / "barcadenobar.ttf"), 18]


class TilemapPath(PathsBase):
    """Path to the tilemap image.

    Attributes:
        TILEMAP: Path to the tilemap `.png` file.
    """
    TILEMAP = (ASSETS / "tilemap" / "tilemap").with_suffix(".png")


class SpritesPaths(PathsBase):
    """Paths to sprite files.

    Attributes:
        PAC_MAN: Path to the Pac-Man animation `.gif` file.
    """
    PAC_MAN = (ASSETS / "player" / "PacMan-Anim").with_suffix(".gif")
