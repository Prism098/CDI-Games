import pygame
from utils.styles import WIDTH, HEIGHT, BLACK, WHITE, OUTLIER_COLOR, MISSING_COLOR, INCORRECT_COLOR

def show_end_screen(screen, score, elapsed_time, found_outliers, total_outliers, found_missing, total_missing, found_incorrect, total_incorrect):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                running = False

        screen.fill(BLACK)

        # Grote titel voor Game Over
        title_font = pygame.font.SysFont(None, 80)
        text_font = pygame.font.SysFont(None, 50)

        title_text = title_font.render("Game Over", True, WHITE)
        score_text = text_font.render(f"Final Score: {score}", True, WHITE)
        time_text = text_font.render(f"Time Taken: {elapsed_time}s", True, WHITE)
        instruction_text = text_font.render("Press Enter to Exit", True, WHITE)

        # Found values in bijhorende kleuren
        outliers_text = text_font.render(f"Outliers Found: {found_outliers}/{total_outliers}", True, OUTLIER_COLOR)
        missing_text = text_font.render(f"Missing Values Found: {found_missing}/{total_missing}", True, MISSING_COLOR)
        incorrect_text = text_font.render(f"Incorrect Values Found: {found_incorrect}/{total_incorrect}", True, INCORRECT_COLOR)

        # Positioneer teksten
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3))
        screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT // 3 + 50))
        screen.blit(outliers_text, (WIDTH // 2 - outliers_text.get_width() // 2, HEIGHT // 3 + 120))
        screen.blit(missing_text, (WIDTH // 2 - missing_text.get_width() // 2, HEIGHT // 3 + 170))
        screen.blit(incorrect_text, (WIDTH // 2 - incorrect_text.get_width() // 2, HEIGHT // 3 + 220))
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT - 100))

        pygame.display.flip()

    pygame.quit()
