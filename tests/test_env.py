"""
Unit tests for Random Dot Motion environment.
"""

import gymnasium as gym
import gym_rdm  # Necessary to register the environment


def test_rdm_env():
    """Test the RDM environment"""

    _ = gym.make("RDM-v0")

    assert True
