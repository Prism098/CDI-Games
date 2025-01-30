import pygame
from utils.styles import WIDTH, HEIGHT, BLACK, WHITE, MISSING_COLOR, INCORRECT_COLOR, ERROR_COLOR, BACKGROUND_COLOR
import sys

def show_end_screen(screen, score, elapsed_time, found_missing, total_missing, found_incorrect, total_incorrect, wrong_clicks):
    # Maak het scherm fullscreen
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                running = False

        screen.fill(BACKGROUND_COLOR)

        # Fonts
        title_font = pygame.font.SysFont(None, 80)
        text_font = pygame.font.SysFont(None, 50)

        # Bereken resterende tijd
        remaining_time = max(0, 30 - elapsed_time)  # Zorg dat het niet negatief wordt

        # Teksten voor het eindscherm
        title_text = title_font.render("Game Over", True, ERROR_COLOR)
        score_text = text_font.render(f"Eindscore: {score}", True, WHITE)
        time_text = text_font.render(f"Tijd over: {int(remaining_time)}s", True, WHITE)
        mistakes_text = text_font.render(f"Aantal fouten: {wrong_clicks}", True, WHITE)

        # Waarden in bijhorende kleuren
        missing_text = text_font.render(f"Missing Values gevonden: {found_missing}/{total_missing}", True, MISSING_COLOR)
        incorrect_text = text_font.render(f"Incorrect Values gevonden: {found_incorrect}/{total_incorrect}", True, INCORRECT_COLOR)

        # Instructies
        instruction_text = text_font.render("Druk op Enter om terug te gaan naar het menu", True, WHITE)

        # Posities bepalen
        title_y = HEIGHT // 6
        score_y = title_y + 80
        time_y = score_y + 50
        mistakes_y = time_y + 50
        missing_y = mistakes_y + 80
        incorrect_y = missing_y + 50
        instruction_y = HEIGHT - 100

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, title_y))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, score_y))
        screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, time_y))
        screen.blit(mistakes_text, (WIDTH // 2 - mistakes_text.get_width() // 2, mistakes_y))
        screen.blit(missing_text, (WIDTH // 2 - missing_text.get_width() // 2, missing_y))
        screen.blit(incorrect_text, (WIDTH // 2 - incorrect_text.get_width() // 2, incorrect_y))
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, instruction_y))

        pygame.display.flip()
    print("Score:" , score)
    pygame.quit()
    sys.exit()
