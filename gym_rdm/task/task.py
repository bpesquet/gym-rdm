"""
Random Dot Motion task.
"""

import numpy as np
from numpy.typing import NDArray
import pygame
from pygame.sprite import Group
from gym_rdm.config import Config
from .dot import Dot

# Frame type: a NumPy array containing pisel values as 8-bits RGB triplets
FrameType = NDArray[np.uint8]


class Task:
    """Random Dot Motion task"""

    def __init__(
        self,
        show_window: bool = True,
        fps: int = 30,
        config: Config = Config(),
    ):
        self.show_window = show_window
        self.fps = fps
        self.config = config

        # Pygame setup
        pygame.init()

        # Clock used to ensure that the environment is rendered at the correct framerate
        self.clock = pygame.time.Clock()

        # Define the surface we draw dots upon
        self.canvas = pygame.Surface((config.display_size, config.display_size))

        if self.show_window:
            # Define the window shown to the user
            self.window = pygame.display.set_mode(
                (config.display_size, config.display_size)
            )

            pygame.display.set_caption(config.window_title)

        self._init_dots()

    def _init_dots(self) -> None:
        """Setup the moving dots"""

        # Center of the circular area containing the dots
        center = (self.config.display_size / 2, self.config.display_size / 2)

        # Use weighted sampling distribution to avoid dots clustering close to center
        weights = np.arange(self.config.dot_area_radius) / sum(
            np.arange(self.config.dot_area_radius)
        )
        radii = np.random.choice(
            a=self.config.dot_area_radius, size=self.config.n_dots, p=weights
        )

        self.dots: Group[Dot] = Group()
        for i in range(self.config.n_dots):
            self.dots.add(
                Dot(
                    initial_radius=radii[i],
                    center_position=center,
                    config=self.config,
                )
            )

        self._draw_dots()

    def run(self, n_frames: int | None = None) -> None:
        """Run the task for a specified number of frames or indefinitely"""

        frame = 0
        running = n_frames is None or frame < n_frames
        while running:
            frame += 1
            running = n_frames is None or frame < n_frames

            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.run_frame()
            self.render_frame()

        self.quit()

    def run_frame(self) -> None:
        """Run the task for one frame"""

        # Move all dots
        self.dots.update()

        self._draw_dots()

    def render_frame(self) -> None:
        """Render the current frame to the screen"""

        if self.show_window:
            # Copy the updated canvas to the visible window
            self.window.blit(self.canvas, self.canvas.get_rect())

            # Process pygame internal events
            pygame.event.pump()

            # Update the window
            pygame.display.flip()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.fps)

    def get_frame(self) -> FrameType:
        """Return the current frame as an array of pixels"""

        return np.transpose(
            np.array(pygame.surfarray.pixels3d(self.canvas)), axes=(1, 0, 2)
        )

    def quit(self) -> None:
        """Quit the task"""

        # Pygame cleanup
        pygame.quit()

    def _draw_dots(self) -> None:
        """Draw the dots on the screen"""

        # fill the canvas with a color to wipe away anything from last frame
        self.canvas.fill(self.config.background_color)

        # Draw dots to the screen
        self.dots.draw(self.canvas)
