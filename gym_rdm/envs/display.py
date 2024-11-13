"""
Display window for a RDM task.
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
        pygame.display.set_caption(params.WINDOW_TITLE)

        # Reference to the screen we draw to
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))

        # Clock used to ensure that the environment is rendered at the correct framerate
        self.clock = pygame.time.Clock()

    def update(self, canvas):
        """Update display window to show the current state to the user"""

        # Copy the updated canvas to the screen
        self.screen.blit(source=canvas, dest=canvas.get_rect())

        # Process pygame internal events
        pygame.event.pump()

        # Update the screen
        pygame.display.flip()

        # Limit framerate to desired value
        self.clock.tick(self.render_fps)

    def close(self):
        """Close display window"""

        pygame.quit()
