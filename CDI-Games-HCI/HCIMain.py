import pygame
import sys
from persona import Persona
from ui_element import UIElement

pygame.init()

# Scherminstellingen
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Website Interface Builder Game")

# Kleuren
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 98, 40)

# Fonts
FONT = pygame.font.SysFont("arial", 24)

class GameState:
    def __init__(self):
        self.running = True
        self.score = 0
        self.stage = "colors"
        self.timer = 20  # Tijdslimiet in seconden
        self.start_time = pygame.time.get_ticks()

        # Persona object
        self.persona = Persona(
            "CDI-Games-HCI/assets/Childpersona.png",
            (75, 250),
            "Design een passend interface \n voor de persoon in de onderstaande foto:"
        )

        # UI Elements
        self.ui_elements = [
            UIElement(540, 650, 125, 125, color=ORANGE),
            UIElement(770, 650, 125, 125, color=(150, 150, 150)),
            UIElement(990, 650, 125, 125, color=(77, 55, 50)),
        ]

    def handle_event(self, event):
        # Verwerk muisgebeurtenissen voor de UI
        if event.type == pygame.MOUSEBUTTONUP:
            for element in self.ui_elements:
                if element.rect.collidepoint(event.pos) and self.stage == "colors":
                    # Als de juiste kleur wordt gekozen, verhoog de score
                    if element.color == ORANGE:
                        self.score += 1000
                    self.stage = "complete"  # Ga naar de volgende stage

    def update_timer(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        if elapsed_time >= self.timer:
            self.running = False

    def draw(self, screen):
        # Achtergrond tekenen
        screen.fill(WHITE)

        # Persona tekenen
        self.persona.draw(screen)

        # UI Elements tekenen
        if self.stage == "colors":
            for element in self.ui_elements:
                element.draw(screen)

        # Timer tekenen
        timer_font = pygame.font.SysFont("arial", 36)
        timer_text = timer_font.render(f"Tijd: {max(0, self.timer - int((pygame.time.get_ticks() - self.start_time) / 1000))}s", True, BLACK)
        screen.blit(timer_text, (20, 20))

        # Score tekenen
        score_text = FONT.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (20, 60))

def main():
    # Initialiseer game state
    game_state = GameState()
    clock = pygame.time.Clock()

    while game_state.running:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state.running = False
            game_state.handle_event(event)

        game_state.update_timer()
        game_state.draw(screen)
        pygame.display.flip()

    # Print de uiteindelijke score
    final_score = game_state.score
    pygame.quit()
    print(f"Score: {final_score}")

if __name__ == "__main__":
    main()
