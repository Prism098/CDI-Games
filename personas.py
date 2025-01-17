import pygame
import random

class Persona:
    def __init__(self, image_path, x, y, width, height):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))  # Scale the image to desired size
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# List of personas with their respective image paths and initial positions
personas_list = [
    Persona("assets/ChildPersona.png", 0, 0, 150, 150),  # Example: ChildPersona
    Persona("assets/AdultPersona.png", 0, 0, 150, 150),  # Example: AdultPersona
    Persona("assets/OldManPersona.png", 0, 0, 150, 150),  # Example: OldManPersona
]

# Function to randomly select a persona and place it at a random position
def randomize_personas_positions(screen_width, screen_height):
    """Randomly select one persona and randomize its position"""
    selected_persona = random.choice(personas_list)  # Select a random persona
    selected_persona.rect.topleft = (random.randint(0, screen_width - selected_persona.rect.width),
                                     random.randint(0, screen_height - selected_persona.rect.height))
    return selected_persona  # Return the selected persona

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Persona Display Game")

# Randomly select and place one persona on the screen at the start
selected_persona = randomize_personas_positions(screen_width, screen_height)

# Main game loop
running = True
while running:
    screen.fill((255, 255, 255))  # Clear the screen with a white background
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Draw the selected persona
    selected_persona.draw(screen)
    
    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
