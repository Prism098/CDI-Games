# persona.py
import pygame
import random

class Persona:
    def __init__(self, image_path, x, y, width, height):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))  # Scale the image to desired size
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# Function to position personas at fixed locations
def randomize_personas_positions(screen_height):
    """Place personas at fixed positions on the left side of the screen"""
    personas_list = [
        Persona("assets/ChildPersona.png", 40, 200, 175, 175),  # Fixed position for ChildPersona
        Persona("assets/AdultPersona.png", 40, 200, 175, 175),  # Fixed position for AdultPersona
        Persona("assets/OldManPersona.png", 40, 200, 175, 175),  # Fixed position for OldManPersona
    ]
    
    # You can select any persona from the list; for example, just returning a random one
    selected_persona = random.choice(personas_list)  # You can change this to any persona you want
    return selected_persona
