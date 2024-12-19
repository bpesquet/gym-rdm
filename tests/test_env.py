"""
Unit tests for Random Dot Motion environment.
"""

from pathlib import Path
import matplotlib.pyplot as plt
from gym_rdm.envs import RandomDotMotionEnv, Action
from gym_rdm.config import Config

config = Config()
EXPECTED_SHAPE = (config.display_size, config.display_size, 3)
OUTPUT_DIR = "_output"


def test_env() -> None:
    """Test the RDM environment"""

    env = RandomDotMotionEnv()
    obs, info = env.reset()
    assert obs.shape == EXPECTED_SHAPE
    assert not info

    obs, reward, terminated, truncated, info = env.step(Action.WAIT)
    assert obs.shape == EXPECTED_SHAPE
    assert reward == 0  # Temporary
    assert terminated is False
    assert truncated is False
    assert not info

    obs, reward, terminated, truncated, info = env.step(Action.DECISION_LEFT)
    assert obs.shape == EXPECTED_SHAPE
    assert reward == 0  # Temporary
    assert terminated is True
    assert truncated is False
    assert not info


def test_env_render_human() -> None:
    """Test environment rendering for humans"""

    env = RandomDotMotionEnv(render_mode="human", config=Config(motion_coherence=0))
    env.reset()
    for _ in range(60):
        env.step(env.action_space.sample())
    env.close()


def test_env_render_rgb() -> None:
    """Test environment rendering as rgb frames"""

    env = RandomDotMotionEnv(render_mode="rgb_array")
    env.reset()
    env.step(env.action_space.sample())
    frame = env.render()
    if frame is not None:
        assert frame.shape == EXPECTED_SHAPE

        plt.imshow(frame)
        # Save the frame to disk
        Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
        plt.savefig(f"{OUTPUT_DIR}/env_frame_rgb.png")
