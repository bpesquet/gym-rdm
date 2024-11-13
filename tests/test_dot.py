"""
Unit tests for dots.
"""

from math import sqrt, cos, sin, radians
import pytest
from gym_rdm.envs.dot import Coords


def test_coords():
    """Test the Coords class"""

    coords = Coords(x=1, y=1)
    radius, angle = coords.to_polar()
    assert radius == sqrt(2)
    assert angle == 45

    coords = Coords.from_polar(radius=1, angle=45)
    assert coords.x == pytest.approx(cos(radians(45)))
    assert coords.y == pytest.approx(sin(radians(45)))

    coords = Coords.from_polar(radius=1, angle=225)
    assert coords.x == pytest.approx(cos(radians(225)))
    assert coords.x == pytest.approx(sin(radians(225)))

    coords = Coords.from_polar(radius=1, angle=90)
    assert coords.x == pytest.approx(0)
    assert coords.y == pytest.approx(1)
