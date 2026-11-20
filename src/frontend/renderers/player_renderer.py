# Installed modules
import pygame

# Local modules
from ..assets import AssetsLoader
from ...backend import Player, TileMap
from ...constants import MAZE_HEIGHT_PX, MAZE_WIDTH_PX, CHARACTER_SIZE_PX


class PlayerRenderer():
    def __init__(self, assets: AssetsLoader) -> None:
        self.assets = assets
        self.player_sprite = assets.sprites["PAC_MAN"]

    def display_player(self, surface: pygame.Surface,
                       player: Player) -> None:
        origin_x, origin_y = self._maze_origin(surface)
        cx, cy = TileMap.tile_center(player.pos_x, player.pos_y)
        half = CHARACTER_SIZE_PX // 2

        surface.blit(self.player_sprite,
                     (origin_x + cx - half, origin_y + cy - half))

    def _maze_origin(self, surface: pygame.Surface) -> tuple[int, int]:
        """Top-left of the maze when centered on the surface."""
        return ((surface.get_width() - MAZE_WIDTH_PX) // 2,
                (surface.get_height() - MAZE_HEIGHT_PX) // 2)
