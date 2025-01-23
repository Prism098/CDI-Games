import pygame
from screens import game_screen
from utils.styles import WHITE, BACKGROUND_COLOR, WIDTH, HEIGHT, OUTLIER_COLOR, MISSING_COLOR, INCORRECT_COLOR

def show_menu():
    # Maak het scherm fullscreen
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()

    pygame.display.set_caption("Dataset Cleaning Game - Menu")

    # Laad de afbeelding van de game
    assets_path = "CDI-Games-DataEngineering/assets"
    game_preview_image = pygame.image.load(f"{assets_path}/gamescreen4.png")
    game_preview_image = pygame.transform.scale(game_preview_image, (1000, 550))  # Schaal de afbeelding

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        # Fonts instellen
        title_font = pygame.font.Font(None, 80)  # Grote titel
        text_font = pygame.font.Font(None, 40)  # Normale tekst
        info_font = pygame.font.Font(None, 60)  # Voor instructies

        # Titel
        title = title_font.render("Welkom bij de Dataset Cleaning Game", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 10))

        # Initialiseer explanation_start_y
        explanation_start_y = HEIGHT // 4

        # Uitleg
        explanation_title = text_font.render("Hieronder volgt de uitleg over welke waarden je moet opruimen (op klikken):", True, WHITE)
        explanation1 = text_font.render("Missing Value: Geen waarde ingevuld in het vakje.", True, MISSING_COLOR)
        explanation2 = text_font.render("Outlier: Waarde die significant buiten het bereik valt.", True, OUTLIER_COLOR)
        explanation3 = text_font.render("Incorrect: Waarde die niet klopt (zoals een foutieve eenheid).", True, INCORRECT_COLOR)

        explanation_gap = 40  # Afstand tussen uitlegregels
        screen.blit(explanation_title, (WIDTH // 2 - explanation_title.get_width() // 2, explanation_start_y - 50))
        screen.blit(explanation1, (WIDTH // 2 - explanation1.get_width() // 2, explanation_start_y))
        screen.blit(explanation2, (WIDTH // 2 - explanation2.get_width() // 2, explanation_start_y + explanation_gap))
        screen.blit(explanation3, (WIDTH // 2 - explanation3.get_width() // 2, explanation_start_y + 2 * explanation_gap))

        # Afbeelding
        preview_x = WIDTH // 2 - game_preview_image.get_width() // 2
        preview_y = explanation_start_y + 3 * explanation_gap + 20
        screen.blit(game_preview_image, (preview_x, preview_y))

        # Instructies met gekleurde woorden
        instruction_part1 = info_font.render("Druk op", True, WHITE)
        instruction_enter = info_font.render(" Enter ", True, (56, 183, 100))  # Groen (#38b764)
        instruction_part2 = info_font.render("om te starten. Je hebt 30 seconden.", True, WHITE)

        # Bereken y-positie van de instructies
        instructions_y = preview_y + game_preview_image.get_height() + 30

        # "Druk op Enter om te starten."
        total_width_start = instruction_part1.get_width() + instruction_enter.get_width() + instruction_part2.get_width()
        screen.blit(instruction_part1, (WIDTH // 2 - total_width_start // 2, instructions_y))
        screen.blit(instruction_enter, (WIDTH // 2 - total_width_start // 2 + instruction_part1.get_width(), instructions_y))
        screen.blit(instruction_part2, (
            WIDTH // 2 - total_width_start // 2 + instruction_part1.get_width() + instruction_enter.get_width(), instructions_y))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "start"
                elif event.key == pygame.K_ESCAPE:
                    return "quit"
