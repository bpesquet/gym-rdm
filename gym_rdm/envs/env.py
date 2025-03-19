"""
Random Dot Motion environment for Gymnasium.
"""

from abc import ABC
from enum import Enum, StrEnum
from typing import Any
import numpy as np
import gymnasium as gym
from gym_rdm.task import Task
from gym_rdm.config import Config
from gym_rdm.typing import GymFrame, GymObs, GymInfo, GymAction


class Action(Enum):
    """
    Possible actions for the agent
    """

    # Wait for more information before committing to a decision
    WAIT = 0
    # Decide that dots are moving to the left
    DECISION_LEFT = 1
    # Decide that dots are moving to the right
    DECISION_RIGHT = 2


class RenderMode(StrEnum):
    """
    Possible render modes for the environment
    """

    HUMAN = "human"
    RGB_ARRAY = "rgb_array"
    NONE = "None"


class RandomDotMotionEnv(gym.Env[GymObs, GymAction], ABC):
    """Gym environment implementing a RDM task"""

    def __init__(
        self,
        render_mode: RenderMode = RenderMode.NONE,
        fps: int = 30,
        config: Config = Config(),
    ):
        """
        Initialize the environment
        """
        self.render_mode = render_mode

        # Init the RDM task
        self.task = Task(
            show_window=self.render_mode == RenderMode.HUMAN,
            fps=fps,
            config=config,
        )

        self.action_space = gym.spaces.Discrete(len(Action))

        # Observations are the pixels of the dot area
        self.observation_space = gym.spaces.Box(
            low=0, high=255, shape=self.task.get_frame().shape, dtype=np.uint8
        )

    def reset(
        self, *, seed: int | None = None, options: dict[str, Any] | None = None
    ) -> tuple[GymObs, GymInfo]:
        # initialize the random number generator
        super().reset(seed=seed)

        observation = self._get_obs()

        if self.render_mode == RenderMode.HUMAN:
            self.task.render_frame()

        return observation, {}

    def step(
        self, action: GymAction | Action
    ) -> tuple[GymObs, float, bool, bool, GymInfo]:
        self.task.run_frame()

        terminated = action != Action.WAIT
        reward = 0  # No learning for now
        observation = self._get_obs()

        if self.render_mode == RenderMode.HUMAN:
            self.task.render_frame()

        return observation, reward, terminated, False, {}

    # Ignoring incompatible return type error from mypy
    # https://github.com/Farama-Foundation/Gymnasium/issues/845
    # https://mypy.readthedocs.io/en/stable/common_issues.html#incompatible-overrides
    def render(self) -> GymFrame | None:  # type: ignore[override]
        if self.render_mode == RenderMode.RGB_ARRAY:
            self.task.render_frame()
            return self.task.get_frame()

        return None

    def close(self) -> None:
        self.task.quit()

    def _get_obs(self) -> GymObs:
        """Construct observation from current state"""

        # Observations are the pixel values of the current frame
        return self.task.get_frame()
