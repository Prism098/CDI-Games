import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH, SCREEN_HEIGHT = 1920 , 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("CAR I.D.E")

# Colors
BLUE = (0, 0, 128)

# Load images
background = pygame.image.load("CDI-Games-SoftwareDevelopment\images\Software Dev\caride_dropzone.png")
turn_left_img = pygame.image.load("CDI-Games-SoftwareDevelopment\images\Software Dev\caride_turn_left.png")
move_forward_img = pygame.image.load("CDI-Games-SoftwareDevelopment\images\Software Dev\caride_Forward.png")
turn_right_img = pygame.image.load("CDI-Games-SoftwareDevelopment\images\Software Dev\caride_turn_right.png")
run_button_img = pygame.image.load("CDI-Games-SoftwareDevelopment\images\Software Dev\Run button.png")

# Scale images to desired sizes
turn_left_img = pygame.transform.scale(turn_left_img, (120, 125))
move_forward_img = pygame.transform.scale(move_forward_img, (80, 80))
turn_right_img = pygame.transform.scale(turn_right_img, (80, 80))
run_button_img = pygame.transform.scale(run_button_img, (120, 50))
background = pygame.transform.scale(background,(480, 820 ))

# Positions for the UI elements
background_pos = (5, 10)
turn_left_pos = (500, 200)
move_forward_pos = (620, 200)
turn_right_pos = (740, 200)
run_button_pos = (900, 200)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Draw elements
    screen.fill(BLUE)
    screen.blit(background, background_pos)
    screen.blit(turn_left_img, turn_left_pos)
    screen.blit(move_forward_img, move_forward_pos)
    screen.blit(turn_right_img, turn_right_pos)
    screen.blit(run_button_img, run_button_pos)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
