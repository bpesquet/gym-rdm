"""
Random Dot Motion Gymnasium environment.
"""

from abc import ABC
from enum import Enum
from typing import Optional, Any, TypeVar, SupportsFloat
import numpy as np
import gymnasium as gym
import pygame
from gym_rdm.envs import params

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
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 25}

    def __init__(
        self,
        render_mode: Optional[str] = None,
        n_dots: Optional[int] = params.N_DOTS,
        coherence: Optional[float] = params.COHERENCE,
    ):
        """
        Initialize the environment
        """
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.n_dpts = n_dots
        self.coherence = coherence
        self.window_size = params.WINDOW_SIZE

        self.action_space = gym.spaces.Discrete(len(Action))

        """
        If human-rendering is used, `self.window` will be a reference to the window that we draw to. 
        `self.clock` will be a clock that is used to ensure that the environment is rendered at the correct framerate in human-mode.
        They will remain `None` until human-mode is used for the first time.
        """
        self.window = None
        self.clock = None

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
        Render the current state of the environment as a frame
        """
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))

        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.window_size, self.window_size))
        canvas.fill(params.BACKGROUND_COLOR)

        if self.render_mode == "human":
            # The following line copies our drawings from the canvas to the visible window
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
