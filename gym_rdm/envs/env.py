"""
Random Dot Motion environment for Gymnasium.
"""

from abc import ABC
from enum import Enum
from typing import Optional, Any, TypeVar, SupportsFloat
import numpy as np
import gymnasium as gym
from gym_rdm.task import Task
from gym_rdm import params

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

    def __init__(
        self,
        render_mode: Optional[str] = None,
        coherence: Optional[float] = params.COHERENCE,
    ):
        """
        Initialize the environment
        """
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        # Init the RDM task
        self.task = Task(
            show_window=self.render_mode == "human",
            fps=self.metadata["render_fps"],
            coherence=coherence,
        )

        self.action_space = gym.spaces.Discrete(len(Action))

        # Observations are the pixels of the dot area
        self.observation_space = gym.spaces.Box(
            low=0, high=255, shape=self.task.get_frame().shape, dtype=np.uint8
        )

    def reset(
        self, *, seed: Optional[int] = None, options: Optional[dict[str, Any]] = None
    ) -> tuple[ObsType, dict[str, Any]]:
        # initialize the random number generator
        super().reset(seed=seed)

        observation = self._get_obs()

        if self.render_mode == "human":
            self.task.render_frame()

        return observation, None

    def step(
        self, action: Action
    ) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        self.task.run_frame()

        terminated = action != Action.WAIT
        reward = 0  # No learning for now
        observation = self._get_obs()

        if self.render_mode == "human":
            self.task.render_frame()

        return observation, reward, terminated, False, None

    def render(self):
        if self.render_mode == "rgb_array":
            self.task.render_frame()
            return self.task.get_frame()

        return None

    def close(self):
        self.task.quit()

    def _get_obs(self):
        """Construct observation from current state"""

        # Observations are the pixel values of the current frame
        return self.task.get_frame()
