import pygame
import random

class Persona:
    def __init__(self, image_path, x, y, width, height, correct_color, correct_image, correct_font):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.correct_color = correct_color
        self.correct_image = correct_image
        self.correct_font = correct_font

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

def randomize_personas_positions(screen_height):
    """Place personas at fixed positions on the left side of the screen"""
    BROWN = (77, 55, 50)
    ORANGE = (255, 98, 40)
    GREY = (150, 150, 150)
    
    personas_list = [
        Persona("assets/ChildPersona.png", 40, 200, 175, 175, 
                ORANGE, "assets/CartoonHappyPhoto.png", "comicsansms"),
        Persona("assets/AdultPersona.png", 40, 200, 175, 175, 
                BROWN, "assets/ProfessionalManPhoto.png", "timesnewroman"),
        Persona("assets/OldManPersona.png", 40, 200, 175, 175, 
                GREY, "assets/OldManPhoto.png", "couriernew")
    ]
    
    return random.choice(personas_list)