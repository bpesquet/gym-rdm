"""
Random Dot Motion task.
"""

import numpy as np
import pygame
from gym_rdm import params
from .dot import Dot
from gym_rdm import params


class Task:
    """Random Dot Motion task"""

    def __init__(
        self,
        show_window: bool = True,
        fps: int = 30,
        coherence: float = params.COHERENCE,
    ):
        self.show_window = show_window
        self.fps = fps

        # Pygame setup
        pygame.init()

        # Clock used to ensure that the environment is rendered at the correct framerate
        self.clock = pygame.time.Clock()

        # Size of the display surface and window
        display_size = params.DISPLAY_SIZE

        # Define the surface we draw dots upon
        self.canvas = pygame.Surface((display_size, display_size))

        if self.show_window:
            # Define the window shown to the user
            self.window = pygame.display.set_mode((display_size, display_size))

            pygame.display.set_caption(params.WINDOW_TITLE)

        self._init_dots(display_size=display_size, coherence=coherence)

    def _init_dots(self, display_size: int, coherence: float):
        """Setup the moving dots"""

        # Center of the circular area containing the dots
        center = (display_size / 2, display_size / 2)
        n_dots = params.N_DOTS

        aperture_radius = params.APERTURE_RADIUS

        # Use weighted sampling distribution to avoid dots clustering close to center
        weights = np.arange(aperture_radius) / sum(np.arange(aperture_radius))
        radii = np.random.choice(a=aperture_radius, size=n_dots, p=weights)

        self.dots = pygame.sprite.Group()
        for i in range(n_dots):
            self.dots.add(
                Dot(
                    radius=radii[i],
                    center=center,
                    aperture_radius=aperture_radius,
                    motion_angle=params.MOTION_ANGLE,
                    coherence=coherence,
                )
            )

        self._draw_dots()

    def run(self, n_frames: int = None):
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

    def run_frame(self):
        """Run the task for one frame"""

        # Move all dots
        self.dots.update()

        self._draw_dots()

    def render_frame(self):
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

    def get_frame(self) -> np.ndarray:
        """Return the current frame as an array of pixels"""

        return np.transpose(
            np.array(pygame.surfarray.pixels3d(self.canvas)), axes=(1, 0, 2)
        )

    def quit(self):
        """Quit the task"""

        # Pygame cleanup
        pygame.quit()

    def _draw_dots(self):
        """Draw the dots on the screen"""

        # fill the canvas with a color to wipe away anything from last frame
        self.canvas.fill(params.BACKGROUND_COLOR)

        # Draw dots to the screen
        self.dots.draw(self.canvas)
