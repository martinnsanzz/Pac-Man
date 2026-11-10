class PacManError(Exception):
    """Base class for every expected error in the project."""


class LoadAssetsError(PacManError):
    """Error class to raise when something fails loading assets"""
