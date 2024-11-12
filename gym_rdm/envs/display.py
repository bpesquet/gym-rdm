"""
Pygame-powered display for a RDM task
"""

import pygame
from gym_rdm.envs import params


class RandomDotMotionDisplay:
    """
    Display window for a RDM task
    """

    def __init__(self, render_fps, window_size):
        self.render_fps = render_fps
        self.window_size = window_size

        pygame.init()
        pygame.display.init()
        pygame.display.set_caption(params.WINDOW_TITLE)

        # Reference to the window we draw to
        self.window = pygame.display.set_mode((self.window_size, self.window_size))

        # Clock used to ensure that the environment is rendered at the correct framerate
        self.clock = pygame.time.Clock()

    def update(self, canvas):
        """Update display window to show the current state to the user"""

        # The following line copies our drawings from the canvas to the visible window
        self.window.blit(canvas, canvas.get_rect())
        pygame.event.pump()
        pygame.display.update()

        # We need to ensure that human-rendering occurs at the predefined framerate.
        # The following line will automatically add a delay to keep the framerate stable.
        self.clock.tick(self.render_fps)

    def close(self):
        """Close display window"""

        pygame.display.quit()
        pygame.quit()
