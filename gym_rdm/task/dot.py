"""
Moving dot.
"""

from typing import Tuple
import random
import pygame
from pygame import Rect
from pygame.math import Vector2
from gym_rdm.config import Config


class Dot(pygame.sprite.Sprite):
    """A moving dot"""

    def __init__(
        self,
        initial_radius: float,
        center_position: Tuple[float, float],
        config: Config = Config(),
    ):
        super().__init__()

        self.center_position = center_position
        self.max_radius = config.dot_area_radius - config.dot_size / 2

        # Motion angle may be set randomly depending on coherence
        self.motion_angle = (
            config.motion_angle
            if random.random() < config.motion_coherence
            else random.randint(0, 359)
        )

        # Create an image of the dot, and fill it with its color
        self.image = pygame.Surface(size=[config.dot_size, config.dot_size])
        self.image.fill(color=config.dot_color)

        # Speed vector
        speed: Vector2 | None = Vector2.from_polar(
            (config.dot_velocity, self.motion_angle)
        )
        self.speed: Vector2 = speed if speed is not None else Vector2()

        # Initial dot angle is set randomly
        position_angle = random.randint(0, 359)

        # Initial dot position in local coordinates (relative to the center of the dot circular area)
        initial_position: Vector2 | None = Vector2.from_polar(
            (initial_radius, position_angle)
        )
        assert initial_position is not None

        # Fetch the rectangle object that has the dimensions of the dot, centered at its absolute coordinates
        self.rect: Rect = self.image.get_rect(
            center=self._get_abs_position(position=initial_position)
        )

    def update(self) -> None:
        """(Overriden) Move the dot around"""

        # Move dot according to speed vector
        self.rect.move_ip(self.speed.x, -self.speed.y)

        # Check if dot is now outside of circular area, and reset its position in that case
        new_position = Vector2(self.rect.center)
        distance_to_center = new_position.distance_to(Vector2(self.center_position))
        if distance_to_center > self.max_radius:
            self._reset()

    def _reset(self) -> None:
        """Reset dot position"""

        # Move dot to the other side of the circular area
        # (angle is randomly altered for more stochasticity)
        new_radius = self.max_radius
        new_angle = self.motion_angle - 180 + random.randint(-90, 90)

        # Compute local coordinates
        new_position = Vector2.from_polar((new_radius, new_angle))

        if new_position is not None:
            # Update position of the dot
            self.rect = self.image.get_rect(
                center=self._get_abs_position(position=new_position)
            )

    def _get_abs_position(self, position: Vector2) -> Tuple[float, float]:
        """Convert local coordinates to absolute"""

        # Pygame origin is the top left of the screen
        return (
            position.x + self.center_position[0],
            self.center_position[1] - position.y,
        )

    def __str__(self) -> str:
        return f"Position: {self.rect}. Speed: {self.speed}. Motion angle: {self.motion_angle}"
