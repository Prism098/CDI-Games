import pygame
import os

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonts
FONT = pygame.font.SysFont("arial", 24)

class Persona:
    def __init__(self, image_path, position, text=""):
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (350, 300))
        except pygame.error as e:
            print(f"Error loading image: {e}")
            self.image = None

        self.image_rect = (
            self.image.get_rect(topleft=position)
            if self.image
            else pygame.Rect(0, 0, 0, 0)
        )
        self.text = text
        self.additional_text = "Kenmerken: Energieker, Opgewonden, Prikkelig"

    def draw(self, screen):
        if self.text:
            lines = self.text.split("\n")
            for i, line in enumerate(lines):
                text_surface = FONT.render(line, True, BLACK)
                text_rect = text_surface.get_rect(
                    center=(
                        self.image_rect.centerx,
                        self.image_rect.top - 20 - (30 * (len(lines) - i - 1)),
                    )
                )
                screen.blit(text_surface, text_rect)
        if self.image:
            screen.blit(self.image, self.image_rect)
        else:
            pygame.draw.rect(screen, (220, 20, 60), self.image_rect)
            message = FONT.render("Image Load Failed", True, WHITE)
            screen.blit(message, self.image_rect.center)
        additional_text_surface = FONT.render(self.additional_text, True, BLACK)
        additional_text_rect = additional_text_surface.get_rect(
            center=(self.image_rect.centerx, self.image_rect.bottom + 10)
        )
        screen.blit(additional_text_surface, additional_text_rect)
