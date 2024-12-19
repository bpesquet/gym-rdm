"""
Random Dot Motion environment for Gymnasium.
"""

from abc import ABC
from enum import Enum
from typing import Any
import numpy as np
from numpy.typing import NDArray
import gymnasium as gym
from gym_rdm.task import Task, FrameType
from gym_rdm.config import Config

# Observation type: a NumPy array containing pisel values as 8-bits RGB triplets
ObsType = NDArray[np.uint8]

# Information type: a plain Python dictionary
InfoType = dict[str, Any]

# Action type: integer values corresponding to possible actions
ActionType = np.int64


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


class RandomDotMotionEnv(gym.Env[ObsType, ActionType], ABC):
    """Gym environment implementing a RDM task"""

    # Supported render modes and framerate
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 30}

    def __init__(
        self,
        render_mode: str | None = None,
        config: Config = Config(),
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
            config=config,
        )

        self.action_space = gym.spaces.Discrete(len(Action))

        # Observations are the pixels of the dot area
        self.observation_space = gym.spaces.Box(
            low=0, high=255, shape=self.task.get_frame().shape, dtype=np.uint8
        )

    def reset(
        self, *, seed: int | None = None, options: dict[str, Any] | None = None
    ) -> tuple[ObsType, InfoType]:
        # initialize the random number generator
        super().reset(seed=seed)

        observation = self._get_obs()

        if self.render_mode == "human":
            self.task.render_frame()

        return observation, {}

    def step(
        self, action: ActionType | Action
    ) -> tuple[ObsType, float, bool, bool, InfoType]:
        self.task.run_frame()

        terminated = action != Action.WAIT
        reward = 0  # No learning for now
        observation = self._get_obs()

        if self.render_mode == "human":
            self.task.render_frame()

        return observation, reward, terminated, False, {}

    # Ignoring incompatible return type error from mypy
    # https://github.com/Farama-Foundation/Gymnasium/issues/845
    # https://mypy.readthedocs.io/en/stable/common_issues.html#incompatible-overrides
    def render(self) -> FrameType | None:  # type: ignore[override]
        if self.render_mode == "rgb_array":
            self.task.render_frame()
            return self.task.get_frame()

        return None

    def close(self) -> None:
        self.task.quit()

    def _get_obs(self) -> ObsType:
        """Construct observation from current state"""

        # Observations are the pixel values of the current frame
        return self.task.get_frame()
