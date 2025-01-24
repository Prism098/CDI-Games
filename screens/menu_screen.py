import pygame
from screens import game_screen
from utils.styles import WHITE, BACKGROUND_COLOR, WIDTH, HEIGHT,MISSING_COLOR, INCORRECT_COLOR, ERROR_COLOR

def show_menu():
    # Maak het scherm fullscreen
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()

    pygame.display.set_caption("Dataset Cleaning Game - Menu")

    # Laad voorbeeldafbeeldingen
    assets_path = "assets"
    example_image = pygame.image.load(f"{assets_path}/gamescreen1.png")

    # Schaal afbeelding
    example_image = pygame.transform.scale(example_image, (1100, 650))

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        # Fonts instellen
        title_font = pygame.font.Font(None, 80)  # Grote titel
        text_font = pygame.font.Font(None, 40)  # Normale tekst
        info_font = pygame.font.Font(None, 60)  # Voor instructies

        # Titel
        title = title_font.render("Welkom bij de Dataset Cleaning Game", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 15))

        # Initialiseer explanation_start_y
        explanation_start_y = HEIGHT // 6

        # Uitleg
        explanation_title_part1 = text_font.render("Hieronder volgt de uitleg over welke waarden je moet opruimen (", True, WHITE)
        explanation_title_part2 = text_font.render("op klikken", True, ERROR_COLOR)  # ERROR_COLOR = #b13e53
        explanation_title_part3 = text_font.render("):", True, WHITE)
        explanation1 = text_font.render("Missing Value: Het vakje is helemaal leeg. Er ontbreekt dus data! (zie voorbeelden hieronder!)", True, MISSING_COLOR)
        explanation2 = text_font.render("Incorrect: Er staat data wat niet klopt. (zie voorbeelden hieronder!)", True, INCORRECT_COLOR)

        # Positie van de gesplitste uitleg
        title_x = WIDTH // 2 - (
                explanation_title_part1.get_width()
                + explanation_title_part2.get_width()
                + explanation_title_part3.get_width()
        ) // 2

        # Render de uitleg met "op klikken" in een andere kleur
        screen.blit(explanation_title_part1, (title_x, explanation_start_y - 50))
        screen.blit(explanation_title_part2, (title_x + explanation_title_part1.get_width(), explanation_start_y - 50))
        screen.blit(explanation_title_part3, (
        title_x + explanation_title_part1.get_width() + explanation_title_part2.get_width(), explanation_start_y - 50))

        # Posities en uitleg
        gap = 40
        screen.blit(explanation1, (WIDTH // 2 - explanation1.get_width() // 2, explanation_start_y))
        screen.blit(explanation2, (WIDTH // 2 - explanation2.get_width() // 2, explanation_start_y + gap))

        # Voorbeeldafbeelding
        example_y = explanation_start_y + 2 * gap + 40
        screen.blit(example_image, (WIDTH // 2 - example_image.get_width() // 2, example_y))

        # Instructies met gekleurde woorden
        instruction_part1 = info_font.render("Druk op", True, WHITE)
        instruction_enter = info_font.render(" Enter ", True, (56, 183, 100))  # Groen (#38b764)
        instruction_part2 = info_font.render("om te starten. Je hebt 30 seconden.", True, WHITE)

        # Y-positie van de instructies
        instructions_y = example_y + example_image.get_height() + 50

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
