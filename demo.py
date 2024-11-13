import numpy as np
import pygame
from gym_rdm.envs import params
from gym_rdm.envs.dot import Dot

# pygame setup
pygame.init()
screen = pygame.display.set_mode((params.CANVAS_SIZE, params.CANVAS_SIZE))
clock = pygame.time.Clock()

center = (params.CANVAS_SIZE / 2, params.CANVAS_SIZE / 2)
aperture_radius = int(params.CANVAS_SIZE / 2 - 50)
n_dots = 200

weights = np.arange(aperture_radius) / sum(np.arange(aperture_radius))
radii = np.random.choice(a=aperture_radius, size=n_dots, p=weights)

dots = pygame.sprite.Group()
for i in range(n_dots):
    dots.add(
        Dot(
            radius=radii[i],
            center=center,
            aperture_radius=aperture_radius,
            motion_angle=180,
        )
    )

running = True
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(params.BACKGROUND_COLOR)

    # Move all dots
    dots.update()

    # Draw dots to the screen
    dots.draw(screen)

    # Update whole screen
    pygame.display.flip()

    # Limit framerate
    clock.tick(30)

pygame.quit()
