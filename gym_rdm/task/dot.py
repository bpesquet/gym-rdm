"""
Moving dot.
"""

from typing import Tuple
import random
import pygame
from pygame.math import Vector2
from gym_rdm import params


class Dot(pygame.sprite.Sprite):
    """A moving dot"""

    def __init__(
        self,
        radius: float,
        center: Tuple[float],
        aperture_radius: float,
        motion_angle: float,
        coherence: float = params.COHERENCE,
        speed: float = params.DOT_SPEED,
    ):
        super().__init__()

        self.center = center
        self.max_radius = aperture_radius - params.DOT_SIZE / 2

        # Motion angle may be set randomly depending on coherence
        self.motion_angle = (
            motion_angle if random.random() < coherence else random.randint(0, 359)
        )

        # Create an image of the dot, and fill it with its color
        self.image = pygame.Surface(size=[params.DOT_SIZE, params.DOT_SIZE])
        self.image.fill(color=params.DOT_COLOR)

        # Speed vector
        self.speed: Vector2 = Vector2.from_polar((speed, self.motion_angle))

        # Initial dot angle is set randomly
        angle = random.randint(0, 359)

        # Initial dot position in local coordinates (relative to the center of the dot circular area)
        position = Vector2.from_polar((radius, angle))

        # Fetch the rectangle object that has the dimensions of the dot, centered at its absolute coordinates
        self.rect = self.image.get_rect(
            center=self._get_abs_position(position=position)
        )

    def update(self):
        """(Overriden) Move the dot around"""

        # Move dot according to speed vector
        self.rect.move_ip(self.speed.x, -self.speed.y)

        # Check if dot is now outside of circular area, and reset its position in that case
        new_position = Vector2(self.rect.center)
        distance_to_center = new_position.distance_to(Vector2(self.center))
        if distance_to_center > self.max_radius:
            self._reset()

    def _reset(self):
        """Reset dot position"""

        # Move dot to the other side of the circular area
        # (angle is randomly altered for more stochasticity)
        new_radius = self.max_radius
        new_angle = self.motion_angle - 180 + random.randint(-90, 90)

        # Compute local coordinates
        new_position = Vector2.from_polar((new_radius, new_angle))

        # Update position of the dot
        self.rect = self.image.get_rect(
            center=self._get_abs_position(position=new_position)
        )

    def _get_abs_position(self, position: Vector2):
        """Convert local coordinates to absolute"""

        # Pygame origin is the top left of the screen
        return (position.x + self.center[0], self.center[1] - position.y)

    def __str__(self):
        return f"Position: {self.rect}"
