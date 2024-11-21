"""
Unit tests for Random Dot Motion task.
"""

import numpy as np
from gym_rdm.task import Task


def test_task(infinite: bool = False):
    """Test the Task class"""

    n_frames = None if infinite else 60
    task = Task()
    task.run(n_frames=n_frames)


def test_task_without_window():
    """Test the Task task without showing the window"""

    task = Task(show_window=False)
    task.run_frame()
    task.run(n_frames=59)

    pixels = task.get_pixels_array()
    assert pixels.shape == (200, 200)


# Standalone execution with no duration specified
if __name__ == "__main__":
    test_task(infinite=True)
