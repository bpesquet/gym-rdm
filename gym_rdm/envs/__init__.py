"""
Package definition file.
"""

from gymnasium.envs.registration import register
from .env import RandomDotMotionEnv, Action

# Register the RDM environment with Gymnasium
register(id="RDM-v0", entry_point="gym_rdm.envs:RandomDotMotionEnv")
