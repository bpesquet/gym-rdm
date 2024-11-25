"""
Unit tests for Random Dot Motion environment.
"""

import gymnasium as gym
from gym_rdm.envs import RandomDotMotionEnv, Action
from gym_rdm import params


def test_env_registration():
    """Test registering the RDM environment through Gymnasium"""

    _ = gym.make("RDM-v0")


def test_env():
    """Test the RDM environment"""

    expected_obs_shape = (params.DISPLAY_SIZE, params.DISPLAY_SIZE, 3)

    env = RandomDotMotionEnv()
    observation, info = env.reset()
    assert observation.shape == expected_obs_shape
    assert info is None

    observation, reward, terminated, truncated, info = env.step(Action.WAIT)
    assert observation.shape == expected_obs_shape
    assert reward == 0  # Temporary
    assert terminated is False
    assert truncated is False
    assert info is None

    observation, reward, terminated, truncated, info = env.step(Action.DECISION_LEFT)
    assert observation.shape == expected_obs_shape
    assert reward == 0  # Temporary
    assert terminated is True
    assert truncated is False
    assert info is None
