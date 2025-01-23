import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the screen to windowed mode
screen = pygame.display.set_mode((1400, 800))

# Start the main loop
while True:
    # Check for events
    for event in pygame.event.get():
        # Check for the quit event
        if event.type == pygame.QUIT:
            # Quit the game
            pygame.quit()
            sys.exit()

        # Check for the fullscreen toggle event
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            # Toggle fullscreen mode
            pygame.display.toggle_fullscreen()