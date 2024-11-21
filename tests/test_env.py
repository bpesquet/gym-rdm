"""
Unit tests for Random Dot Motion environment.
"""

import gymnasium as gym
from gym_rdm.envs import RandomDotMotionEnv


def test_rdm_env():
    """Test the RDM environment"""

    env = RandomDotMotionEnv()
    obs, info = env.reset()


def test_rdm_env_make():
    """Test registering the RDM environment through Gymnasium"""

    _ = gym.make("RDM-v0")
