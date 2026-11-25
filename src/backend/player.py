# Local modules
from .level import Level
from .player_dir import PlayerDir
from .tilemap import TileMap
from ..constants import TILE_PX


class Player():
    """Represent the player with a position, direction and speed.

    Attributes:
        pos_x: Horizontal position of the player in px relative to maze.
        pos_y: Vertical position of the player in px relative to maze.
        direction: Current movement direction, or None if the player has
            no direction set.
        speed: Movement speed of the player.
    """
    def __init__(self, start_pos: tuple[float, float],
                 speed: int = 5) -> None:
        """Initialize the player at a starting position.

        Args:
            start_pos: Initial ``(x, y)`` position of the player in px.
            speed: Movement speed of the player. Defaults to 1.
        """
        self.pos_x = start_pos[0]
        self.pos_y = start_pos[1]
        self.direction: PlayerDir = PlayerDir.NONE
        self.speed = speed

    def update(self, dt: float, level: Level) -> None:
        """Move the player for a time step, stopping at walls.

        Travel ``speed * dt`` px along the current direction in steps that
        never cross a tile center. At each center, check for a wall ahead
        before continuing, so the player cannot skip over a wall at high
        speed. Do nothing if the player has no direction.

        Args:
            dt: Time elapsed since the previous update (assumed to be in
                seconds).
            level: Level used to look up walls.
        """
        remaining = self.speed * dt * TILE_PX

        while remaining > 0 and self.direction != PlayerDir.NONE:
            if self._stop_at_wall(level):
                break

            distance, center = self._distance_to_next_center()
            step = min(remaining, distance)
            self.move(step)
            remaining -= step

            if step == distance:
                self.center_pos_to_cell(center)

    def move(self, distance: float) -> None:
        """Move the player in its current direction.

        Args:
            distance: Distance to move, in px. The player does not move
                if it has no direction.
        """
        match self.direction:
            case PlayerDir.UP:
                self.pos_y -= distance
            case PlayerDir.DOWN:
                self.pos_y += distance
            case PlayerDir.LEFT:
                self.pos_x -= distance
            case PlayerDir.RIGHT:
                self.pos_x += distance

    def has_reached(self, point: tuple[float, float]) -> bool:
        """Check whether the player has reached or passed a point.

        The check is made along the player's direction of travel only.

        Args:
            point: The ``(x, y)`` position to test, in px.

        Returns:
            True if the player is at or beyond ``point`` along its
            direction, False otherwise or if it has no direction.
        """
        x, y = point

        match self.direction:
            case PlayerDir.UP:
                return self.pos_y <= y
            case PlayerDir.DOWN:
                return self.pos_y >= y
            case PlayerDir.LEFT:
                return self.pos_x <= x
            case PlayerDir.RIGHT:
                return self.pos_x >= x
            case _:
                return False

    def center_pos_to_cell(self, center_pos: tuple[float, float]) -> None:
        """Snap the player to the center of a cell.

        Args:
            center_pos: The ``(x, y)`` center of the cell, in px.
        """
        self.pos_x = center_pos[0]
        self.pos_y = center_pos[1]

    def _stop_at_wall(self, level: Level) -> bool:
        """Stop the player at a tile center when a wall blocks its path.

        If the tile under the player has a wall in the player's current
        direction and the player has reached the center of that tile, snap
        the player to the tile center and set its direction to
        ``PlayerDir.NONE``. Otherwise, leave the player unchanged.

        Args:
            level: Level used to look up walls.

        Returns:
            True if the player was stopped, False otherwise.
        """
        col, row = TileMap.pixel_to_tile(self.pos_x, self.pos_y)

        if not level.has_wall(col, row, self.direction):
            return False

        center = TileMap.tile_center(col, row)

        if self.has_reached(center):
            self.center_pos_to_cell(center)
            self.direction = PlayerDir.NONE
            return True
        return False

    def _distance_to_next_center(
            self) -> tuple[float, tuple[float, float]]:
        """Find the next tile center ahead of the player.

        If the player has not yet reached the center of its current tile
        along its direction, that center is the next one. If it is exactly
        on the center or past it, the next one is the center of the
        adjacent tile in the direction of travel. The distance is
        therefore greater than zero and at most ``TILE_PX``.

        Returns:
            A tuple of the distance to the next center along the direction
            of travel, and the ``(x, y)`` position of that center. If the
            player has no direction, return ``(0.0, (x, y))`` with the
            player's own position.
        """
        x, y = self.pos_x, self.pos_y
        col, row = TileMap.pixel_to_tile(x, y)
        cx, cy = TileMap.tile_center(col, row)

        match self.direction:
            case PlayerDir.UP:
                ty = cy if y > cy else cy - TILE_PX
                return y - ty, (cx, ty)
            case PlayerDir.DOWN:
                ty = cy if y < cy else cy + TILE_PX
                return ty - y, (cx, ty)
            case PlayerDir.LEFT:
                tx = cx if x > cx else cx - TILE_PX
                return x - tx, (tx, cy)
            case PlayerDir.RIGHT:
                tx = cx if x < cx else cx + TILE_PX
                return tx - x, (tx, cy)
            case _:
                return 0.0, (x, y)
