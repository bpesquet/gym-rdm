"""
Random Dot Motion Gymnasium environment.
"""

from abc import ABC
from enum import Enum
from typing import Optional, Any, TypeVar, SupportsFloat
import numpy as np
import gymnasium as gym
import pygame
from gym_rdm import params
from gym_rdm.task.display import RandomDotMotionDisplay

# pylint: disable=invalid-name
ObsType = TypeVar("ObsType")
ActType = TypeVar("ActType")
# pylint: enable=invalid-name


class Action(Enum):
    """
    Action space constants
    """

    # Wait for more information before committing to a decision
    WAIT = 0
    # Decide that dots are moving to the left
    DECISION_LEFT = 1
    # Decide that dots are moving to the right
    DECISION_RIGHT = 2


class RandomDotMotionEnv(gym.Env, ABC):
    """Gym environment implementing a RDM task"""

    # Supported render modes and framerate
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 30}

    def __init__(self, render_mode: Optional[str] = None):
        """
        Initialize the environment
        """
        self.n_dpts = params.N_DOTS
        self.coherence = params.COHERENCE
        self.canvas_size = params.DISPLAY_SIZE

        self.action_space = gym.spaces.Discrete(len(Action))

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        if self.render_mode == "human":
            # Init display used in human rendering mode only
            self.display = RandomDotMotionDisplay(
                render_fps=self.metadata["render_fps"], window_size=self.canvas_size
            )

    def reset(
        self, *, seed: Optional[int] = None, options: Optional[dict[str, Any]] = None
    ) -> tuple[ObsType, dict[str, Any]]:
        # initialize the random number generator
        super().reset(seed=seed)

        if self.render_mode == "human":
            self._render_frame()

    def step(
        self, action: ActType
    ) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        if self.render_mode == "human":
            self._render_frame()

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()
        return None

    def _render_frame(self):
        """
        Render the current state as a frame
        """
        canvas = pygame.Surface((self.canvas_size, self.canvas_size))
        canvas.fill(params.BACKGROUND_COLOR)

        if self.render_mode == "human":
            self.display.update(canvas)
        elif self.render_mode == "rgb_array":
            # Return current state as a RGB pixel grid
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )
        print("Warning: unrecognized render mode during frame rendering")
        return None

    def close(self):
        if self.display is not None:
            self.display.close()
