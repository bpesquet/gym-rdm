"""
Moving dot.
"""

from typing import Tuple
import random
from math import cos, sin, radians, sqrt, atan2, degrees
import pygame
from gym_rdm.envs import params


class Coords:
    """Cartesian coordinates of an object"""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @classmethod
    def from_polar(cls, radius: float, angle: float):
        """Init from polar coordinates, with angle expressed in degrees"""

        angle_radians = radians(angle)
        x = radius * cos(angle_radians)
        y = radius * sin(angle_radians)
        return cls(x, y)

    def to_polar(self):
        """Convert to polar coordinates, with angle expressed in degrees"""

        radius = sqrt(self.x**2 + self.y**2)
        angle = degrees(atan2(self.y, self.x))
        return (radius, angle)


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
        self.max_radius = aperture_radius  # - params.DOT_SIZE

        # Motion angle may be set randomly depending on coherence
        self.motion_angle = (
            motion_angle if random.random() < coherence else random.randint(0, 359)
        )

        # Create an image of the dot, and fill it with its color
        self.image = pygame.Surface(size=[params.DOT_SIZE, params.DOT_SIZE])
        self.image.fill(color=params.DOT_COLOR)

        # Speed vector
        self.speed = Coords.from_polar(radius=speed, angle=self.motion_angle)

        # Initial dot angle is set randomly
        angle = 10  # random.randint(0, 359)

        # Initial dot position in local coordinates (relative to the center of the dot circular area)
        position = Coords.from_polar(radius=radius, angle=angle)

        # Fetch the rectangle object that has the dimensions of the dot, centered at its absolute coordinates
        self.rect = self.image.get_rect(
            center=self._get_abs_position(position=position)
        )

    def update(self):
        """(Overriden) Move the dot around"""

        # Move dot according to speed vector
        self.rect.move_ip(self.speed.x, -self.speed.y)

        # Check if dot is now outside of circular area, and reset its position in that case
        (new_x, new_y) = self.rect.center
        (x_center, y_center) = self.center
        distance_to_center = sqrt((new_x - x_center) ** 2 + (new_y - y_center) ** 2)
        if distance_to_center >= self.max_radius:
            self._reset()

    def _reset(self):
        """Reset dot position"""

        # Move dot to the opposite border of the circular area
        # (angle is randomly altered for more stochasticity)
        new_radius = self.max_radius
        new_angle = self.motion_angle - 180 + random.randint(-90, 90)

        # Compute local coordinates
        new_position = Coords.from_polar(radius=new_radius, angle=new_angle)

        # Update position of the dot
        self.rect.update(
            self._get_abs_position(position=new_position),
            (params.DOT_SIZE, params.DOT_SIZE),
        )

    def _get_abs_position(self, position: Coords):
        """Convert local coordinates to absolute"""

        # Pygame origin is the top left of the screen
        return (position.x + self.center[0], self.center[1] - position.y)

    def __str__(self):
        return f"Position: {self.rect}"
