import pygame
import sys

# Initialize Pygame and the font module
pygame.init()
pygame.font.init()

from game import GameState

# Screen dimensions
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Website Interface Builder Game")

def main():
    game_state = GameState()
    clock = pygame.time.Clock()

    running = True
    while running:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game_state.handle_event(event)

        game_state.update_timer(dt)
        game_state.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()