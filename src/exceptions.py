class PacManError(Exception):
    """Base class for every expected error in the project."""


class ConfigError(PacManError):
    """Error class to raise when something fails with the config"""


class LoadAssetsError(PacManError):
    """Error class to raise when something fails loading assets"""


class HighScoreError(PacManError):
    """Error class to raise when anything goes wrong with highscore"""


class MazegenError(PacManError):
    """Error class to raise if mazegen library fails"""
