"""
Configuration values.
"""

# Allow any number of instance attributes for the Config class
# pylint: disable=too-many-instance-attributes

from typing import Tuple
from dataclasses import dataclass


@dataclass
class Config:
    """Configuratiov class"""

    # ----- Motion -----
    # Percentage of signal dots
    motion_coherence: float = 0.5

    # Motion angle for signal dots (in degrees)
    motion_angle: float = 180

    # ----- Dots -----
    # Number of dots
    n_dots: int = 500

    # Dot size in pixels
    dot_size: int = 3

    # Dot speed in pixels per frame
    dot_velocity: int = 3

    # ------ Display -----
    # Dot color
    dot_color: Tuple[int, int, int] = (255, 255, 255)

    # Background color
    background_color: Tuple[int, int, int] = (0, 0, 0)

    # Radius of the circular area containing the dots
    dot_area_radius: int = 256

    # Title of the display window
    window_title: str = "Random Dot Motion"

    @property
    def display_size(self) -> int:
        """Compute the size of the rectangular display surface"""
        return self.dot_area_radius * 2
