import pygame
from utils.styles import WHITE, BACKGROUND_COLOR, WIDTH, HEIGHT, OUTLIER_COLOR, MISSING_COLOR, INCORRECT_COLOR

def show_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dataset Cleaning Game - Menu")

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)  # Achtergrondkleur aangepast

        # Fonts instellen
        title_font = pygame.font.Font(None, 80)  # Grote titel
        text_font = pygame.font.Font(None, 40)  # Normale tekst
        info_font = pygame.font.Font(None, 60)  # Kleinere instructies

        # Titel
        title = title_font.render("Welkom bij de Dataset Cleaning Game", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 5))

        # Uitleg
        explanation1 = text_font.render("Missing Value: Geen waarde ingevuld in de dataset.", True, MISSING_COLOR)
        explanation2 = text_font.render("Outlier: Waarde die significant buiten het bereik valt.", True, OUTLIER_COLOR)
        explanation3 = text_font.render("Incorrect: Waarde die niet klopt (zoals een foutieve eenheid).", True, INCORRECT_COLOR)

        screen.blit(explanation1, (WIDTH // 2 - explanation1.get_width() // 2, HEIGHT // 3))
        screen.blit(explanation2, (WIDTH // 2 - explanation2.get_width() // 2, HEIGHT // 3 + 50))
        screen.blit(explanation3, (WIDTH // 2 - explanation3.get_width() // 2, HEIGHT // 3 + 100))

        # Instructies met gekleurde woorden
        instruction_part1 = info_font.render("Druk op", True, WHITE)
        instruction_enter = info_font.render(" Enter ", True, (56, 183, 100))  # Groen (#38b764)
        instruction_part2 = info_font.render("om te starten.", True, WHITE)

        instruction_part3 = info_font.render("Druk op", True, WHITE)
        instruction_esc = info_font.render(" Esc ", True, (177, 62, 83))  # Rood (#b13e53)
        instruction_part4 = info_font.render("om te stoppen.", True, WHITE)

        # Posities berekenen
        start_y = HEIGHT - 360
        stop_y = HEIGHT - 80

        # "Druk op Enter om te starten."
        total_width_start = instruction_part1.get_width() + instruction_enter.get_width() + instruction_part2.get_width()
        screen.blit(instruction_part1, (WIDTH // 2 - total_width_start // 2, start_y))
        screen.blit(instruction_enter, (WIDTH // 2 - total_width_start // 2 + instruction_part1.get_width(), start_y))
        screen.blit(instruction_part2, (
        WIDTH // 2 - total_width_start // 2 + instruction_part1.get_width() + instruction_enter.get_width(), start_y))

        # "Druk op Esc om te stoppen."
        total_width_stop = instruction_part3.get_width() + instruction_esc.get_width() + instruction_part4.get_width()
        screen.blit(instruction_part3, (WIDTH // 2 - total_width_stop // 2, stop_y))
        screen.blit(instruction_esc, (WIDTH // 2 - total_width_stop // 2 + instruction_part3.get_width(), stop_y))
        screen.blit(instruction_part4, (
        WIDTH // 2 - total_width_stop // 2 + instruction_part3.get_width() + instruction_esc.get_width(), stop_y))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "start"
                elif event.key == pygame.K_ESCAPE:
                    return "quit"
