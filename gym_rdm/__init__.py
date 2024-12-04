"""
Package definition file.
"""

from gymnasium.envs.registration import register

# Register the RDM environment with Gymnasium
register(id="RDM-v0", entry_point="gym_rdm.envs.env:RandomDotMotionEnv")
