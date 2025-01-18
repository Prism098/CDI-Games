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

    # Font for text
     font = pygame.font.SysFont('Arial', 24)  # Set font size
     name_lines = f"Naam: {self.name}".split('\n')
     age_lines = f"Leeftijd: {self.age}".split('\n')
     description_lines = self.description.split('\n')

    # Set initial positions for the text
     name_rect = pygame.Rect(self.rect.centerx - 90, self.rect.bottom + 5, 180, 30)
     age_rect = pygame.Rect(self.rect.centerx - 90, name_rect.bottom + 5, 180, 30)
     description_rect = pygame.Rect(self.rect.centerx - 90, age_rect.bottom + 5, 180, 30)

    # Draw each line of the name
     for line in name_lines:
        name_text = font.render(line, True, self.text_color)
        screen.blit(name_text, name_rect.topleft)
        name_rect.top += name_text.get_height()  # Move down for the next line

    # Draw each line of the age
     for line in age_lines:
        age_text = font.render(line, True, self.text_color)
        screen.blit(age_text, age_rect.topleft)
        age_rect.top += age_text.get_height()  # Move down for the next line

    # Draw each line of the description
     for line in description_lines:
        description_text = font.render(line, True, self.text_color)
        screen.blit(description_text, description_rect.topleft)
        description_rect.top += description_text.get_height()  # Move down for the next line



def randomize_personas_positions(screen_height):
    """Place personas at fixed positions on the left side of the screen"""
    BROWN = (77, 55, 50)
    ORANGE = (255, 98, 40)
    GREY = (150, 150, 150)

    # Define the personas with characteristics (name, age, description)
    personas_list = [
        Persona("assets/ChildPersona.png", 40, 200, 175, 175, 
                ORANGE, "assets/ToyCar.png", "comicsansms", "Timmy", 7, "Houd van kleur en \nrace auto's."),
        Persona("assets/AdultPersona.png",  40, 200, 175, 175, 
                BROWN, "assets/SuitcaseMoney.png", "timesnewroman", "John", 35, "Houd van professionaliteit, \nde kleur bruin en geld."),
        Persona("assets/OldManPersona.png",  40, 200, 175, 175, 
                GREY, "assets/Gramophone.png", "brushscript", "Albert", 75, "Houd niet van felle kleuren. \nLuistert graag naar \nklassieke muziek.")
    ]

    # Randomly select and return a persona
    return random.choice(personas_list)
