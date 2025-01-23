# menu_screen.py
import pygame
from utils.styles import WIDTH, HEIGHT, WHITE, BACKGROUND_COLOR

def show_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Code Racer - Menu")

    running = True
    while running:
        pygame.font.init()
        screen.fill(BACKGROUND_COLOR)
        title_font = pygame.font.Font(None, 80)
        text_font = pygame.font.Font(None, 40)

        title = title_font.render("Welkom bij Code Racer", True, WHITE)
        instruction = text_font.render("Druk op Enter om te starten", True, WHITE)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
        screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "start"
                elif event.key == pygame.K_ESCAPE:
                    return "quit"
