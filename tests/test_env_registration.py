"""
Unit tests for env registration
"""

import gymnasium as gym

# The following import is needed to register the environment with Gymnasium
# pylint: disable=unused-import
import gym_rdm


def test_env_registration():
    """Test registering the RDM environment through Gymnasium"""

    _ = gym.make("RDM-v0")
