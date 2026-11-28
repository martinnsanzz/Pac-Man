# Installed modules
import pygame

# Local modules
from ..assets import AssetsLoader
from ...backend import Player, PlayerDir, PlayerState
from ...constants import MAZE_HEIGHT_PX, MAZE_WIDTH_PX


class PlayerRenderer():
    ANIMATION_FPS = 10

    def __init__(self, assets: AssetsLoader) -> None:
        self.assets = assets
        self.last_index = 0
        self.frames = {
            PlayerState.MOVING: assets.sprites["PAC_MAN_MOVING"],
            PlayerState.IDLE: assets.sprites["PAC_MAN_MOVING"],
            PlayerState.DEAD: assets.sprites["PAC_MAN_DEAD"],
        }

    def display_player(self, surface: pygame.Surface,
                       player: Player) -> None:
        origin_x, origin_y = self._maze_origin(surface)
        center = (origin_x + player.pos_x, origin_y + player.pos_y)

        sprite = self._current_frame(player)
        surface.blit(sprite, sprite.get_rect(center=center))

    def _current_frame(self, player: Player) -> pygame.Surface:
        """Return the frame to draw for a state.

        Moving and dead frames follow the clock at ``ANIMATION_FPS``. While
        idle, the last frame shown is kept so the player freezes in place.
        """
        frames = self.frames[player.state]
        if player.state == PlayerState.IDLE:
            last_frame = frames[self.last_index % len(frames)]
            sprite = self._flip_sprite(last_frame, player.view_direction)
            return sprite

        ticks = pygame.time.get_ticks()
        self.last_index = ticks * self.ANIMATION_FPS // 1000 % len(frames)
        return self._flip_sprite(frames[self.last_index], player.direction)

    def _flip_sprite(self, sprite: pygame.Surface,
                     dir: PlayerDir) -> pygame.Surface:
        match dir:
            case PlayerDir.UP:
                return pygame.transform.rotate(sprite, 90)
            case PlayerDir.DOWN:
                return pygame.transform.rotate(sprite, -90)
            case PlayerDir.LEFT:
                return pygame.transform.flip(sprite, True, False)
            case PlayerDir.RIGHT:
                return pygame.transform.flip(sprite, False, False)
            case _:
                return sprite

    def _maze_origin(self, surface: pygame.Surface) -> tuple[int, int]:
        """Top-left of the maze when centered on the surface."""
        return ((surface.get_width() - MAZE_WIDTH_PX) // 2,
                (surface.get_height() - MAZE_HEIGHT_PX) // 2)
