"""
Unit tests for Random Dot Motion task.
"""

from gym_rdm.task import Task
from gym_rdm import params


def test_task(infinite: bool = False) -> None:
    """Test the Task class"""

    n_frames = None if infinite else 60
    task = Task()
    task.run(n_frames=n_frames)


def test_task_without_window() -> None:
    """Test the Task task without showing the window"""

    task = Task(show_window=False)
    task.run_frame()
    task.render_frame()
    frame = task.get_frame()
    assert frame.shape == (params.DISPLAY_SIZE, params.DISPLAY_SIZE, 3)


# Standalone execution with no duration specified
if __name__ == "__main__":
    test_task(infinite=True)
