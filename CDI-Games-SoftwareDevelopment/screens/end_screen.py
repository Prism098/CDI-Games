# Directory: screens/end_screen.py
import pygame
from utils.styles import WIDTH, HEIGHT, WHITE, BACKGROUND_COLOR

def show_end_screen(screen, score):
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        title_font = pygame.font.Font(None, 80)
        text_font = pygame.font.Font(None, 50)

        title = title_font.render("Game Over", True, WHITE)
        score_text = text_font.render(f"Eindscore: {score}", True, WHITE)
        instruction = text_font.render("Druk op Enter om opnieuw te spelen", True, WHITE)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, 3 * HEIGHT // 4))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "restart"
