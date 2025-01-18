import pygame
import random

class Persona:
    def __init__(self, image_path, x, y, width, height, correct_color, correct_image, correct_font, name, age, description):
        # Load and set the persona image
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

        # Persona characteristics
        self.correct_color = correct_color
        self.correct_image = correct_image
        self.correct_font = correct_font

        # Characteristics for display
        self.name = name
        self.age = age
        self.description = description
        self.text_color = (0, 0, 0)  # Black color for text

    def draw(self, screen):
        # Draw persona image
        screen.blit(self.image, self.rect.topleft)

        # Draw characteristics below the persona's image
        font = pygame.font.SysFont('Arial', 24)  # Set font size
        name_text = font.render(f"Naam: {self.name}", True, self.text_color)
        age_text = font.render(f"Leeftijd: {self.age}", True, self.text_color)
        description_text = font.render(f" {self.description}", True, self.text_color)

        # Get the positions for the characteristics below the persona image
        name_rect = name_text.get_rect(centerx=self.rect.centerx, top=self.rect.bottom + 5)
        age_rect = age_text.get_rect(centerx=self.rect.centerx, top=name_rect.bottom + 5)
        description_rect = description_text.get_rect(centerx=self.rect.centerx, top=age_rect.bottom + 5)

        # Draw the text
        screen.blit(name_text, name_rect)
        screen.blit(age_text, age_rect)
        screen.blit(description_text, description_rect)


def randomize_personas_positions(screen_height):
    """Place personas at fixed positions on the left side of the screen"""
    BROWN = (77, 55, 50)
    ORANGE = (255, 98, 40)
    GREY = (150, 150, 150)

    # Define the personas with characteristics (name, age, description)
    personas_list = [
        Persona("assets/ChildPersona.png", 40, 200, 175, 175, 
                ORANGE, "assets/CartoonHappyPhoto.png", "comicsansms", "Timmy", 7, "Houd van kleur."),
        Persona("assets/AdultPersona.png",  40, 200, 175, 175, 
                BROWN, "assets/ProfessionalManPhoto.png", "timesnewroman", "John", 35, "Houd van professionaliteit."),
        Persona("assets/OldManPersona.png",  40, 200, 175, 175, 
                GREY, "assets/OldManPhoto.png", "couriernew", "Albert", 75, "Houd van niet felle kleuren.")
    ]

    # Randomly select and return a persona
    return random.choice(personas_list)
