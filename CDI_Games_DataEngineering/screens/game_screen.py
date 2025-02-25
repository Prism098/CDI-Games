import pygame
import os
import random
from data.dataset import generate_dataset
from utils.styles import WIDTH, HEIGHT, INFO_PANEL_WIDTH, GREY, WHITE, BLACK, COLUMN_COLOR, TITLE_HEIGHT, STUDENT_NUMBER_COLOR, OUTLIER_COLOR, MISSING_COLOR, INCORRECT_COLOR
from screens.end_screen import show_end_screen

TIMER_SECONDS = 30  # Timer van 30 seconden
STUDENT_NUMBER_WIDTH = 150  # Breedte van de studentnummerkolom
MAX_SCORE = 2500  # Maximale score

def start_game():
    pygame.init()

    # Maak het scherm fullscreen
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()

    # Laad de checkmark-, cross- en brush-afbeeldingen
    assets_path = os.path.join(os.path.dirname(__file__), "..", "assets")
    tick_sound = pygame.mixer.Sound(os.path.join(assets_path, "tick.wav"))
    checkmark_image = pygame.image.load(os.path.join(assets_path, "check.png"))
    cross_image = pygame.image.load(os.path.join(assets_path, "cross.png"))
    brush_image = pygame.image.load(os.path.join(assets_path, "brush.png"))

    # Schaal de afbeeldingen
    checkmark_image = pygame.transform.scale(checkmark_image, (60, 60))
    cross_image = pygame.transform.scale(cross_image, (60, 60))
    brush_image = pygame.transform.scale(brush_image, (40, 40))

    # Verberg de standaard cursor
    pygame.mouse.set_visible(False)

    pygame.display.set_caption("Dataset Cleaning Game")

    # Setup dataset
    dataset = generate_dataset()
    rows = len(dataset)
    cols = len(dataset[0])

    # Dynamische breedteberekening voor kolommen
    available_width = WIDTH - INFO_PANEL_WIDTH - STUDENT_NUMBER_WIDTH
    cell_width = available_width // cols
    cell_height = (HEIGHT - TITLE_HEIGHT) // rows

    # Genereer studentnummers
    student_numbers = [f"20{random.randint(10000, 99999)}" for _ in range(rows)]

    score = 0
    wrong_clicks = 0
    remaining_time = TIMER_SECONDS
    clock = pygame.time.Clock()
    running = True

    found_missing = 0
    found_incorrect = 0

    total_missing = sum(1 for row in dataset for cell in row if cell["status"] == "missing")
    total_incorrect = sum(1 for row in dataset for cell in row if cell["status"] == "incorrect")
    total_errors = total_missing + total_incorrect

    # Scorefactor berekenen
    points_per_missing = MAX_SCORE * 0.4 / total_missing if total_missing else 0
    points_per_incorrect = MAX_SCORE * 0.6 / total_incorrect if total_incorrect else 0

    tick_playing = False  # Houdt bij of de tick speelt

    while running:
        dt = clock.tick(60) / 1000.0  # Delta tijd in seconden
        remaining_time -= dt  # Aftellen

        # Controleer en speel de tick-sound tijdens de laatste 10 seconden
        if remaining_time <= 10 and not tick_playing:
            tick_sound.play(loops=-1)  # Herhaal het geluid
            tick_playing = True
        elif remaining_time > 10 and tick_playing:
            tick_sound.stop()  # Stop het geluid als er meer dan 10 seconden over zijn
            tick_playing = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if mouse_x < WIDTH - INFO_PANEL_WIDTH and mouse_y > TITLE_HEIGHT:
                    col = (mouse_x - STUDENT_NUMBER_WIDTH) // cell_width
                    row = (mouse_y - TITLE_HEIGHT) // cell_height
                    if 0 <= row < rows and 0 <= col < cols:
                        cell = dataset[row][col]
                        if not cell["clicked"]:
                            cell["clicked"] = True
                            if cell["status"] == "missing":
                                score += points_per_missing
                                found_missing += 1
                                cell["mark"] = "check"
                                cell["color"] = MISSING_COLOR
                            elif cell["status"] == "incorrect":
                                score += points_per_incorrect
                                found_incorrect += 1
                                cell["mark"] = "check"
                                cell["color"] = INCORRECT_COLOR
                            else:
                                score -= MAX_SCORE * 0.1
                                wrong_clicks += 1
                                cell["mark"] = "cross"
                                cell["color"] = GREY

                            # Zorg ervoor dat de score niet onder 0 gaat
                            score = max(0, score)

        # Controleer of het spel moet eindigen
        if found_missing == total_missing and found_incorrect == total_incorrect:
            tick_sound.stop()  # Stop de tick-sound
            show_end_screen(
                screen,
                round(score),
                TIMER_SECONDS - int(remaining_time),
                found_missing,
                total_missing,
                found_incorrect,
                total_incorrect,
                wrong_clicks
            )
            return

        if remaining_time <= 0:
            tick_sound.stop()  # Stop de tick-sound
            show_end_screen(
                screen,
                round(score),
                TIMER_SECONDS,
                found_missing,
                total_missing,
                found_incorrect,
                total_incorrect,
                wrong_clicks
            )
            return

        screen.fill(BLACK)

        # Teken kolomtitels
        font_title = pygame.font.SysFont(None, 35)
        titles = ["Student Nr.", "Afstand", "Transport", "Gemiddelde cijfer", "Hoogste cijfer", "Geboortedatum", "Startdatum"]
        for i, title in enumerate(titles):
            if i == 0:  # Eerste kolom voor Studentnummer
                rect_x = 0
                rect_width = STUDENT_NUMBER_WIDTH
            else:  # Overige kolommen
                rect_x = STUDENT_NUMBER_WIDTH + (i - 1) * cell_width
                rect_width = cell_width
            rect = pygame.Rect(rect_x, 0, rect_width, TITLE_HEIGHT)
            pygame.draw.rect(screen, COLUMN_COLOR, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            title_text = font_title.render(title, True, WHITE)
            screen.blit(title_text, (rect.x + (rect.width - title_text.get_width()) // 2, rect.y + 10))

        # Teken de grid en waarden
        font = pygame.font.SysFont(None, 30)
        for r, row in enumerate(dataset):
            # Teken studentnummer
            student_rect = pygame.Rect(0, r * cell_height + TITLE_HEIGHT, STUDENT_NUMBER_WIDTH, cell_height)
            pygame.draw.rect(screen, STUDENT_NUMBER_COLOR, student_rect)
            pygame.draw.rect(screen, BLACK, student_rect, 1)
            student_text = font.render(student_numbers[r], True, WHITE)
            student_text_rect = student_text.get_rect(center=student_rect.center)
            screen.blit(student_text, student_text_rect)

            for c, cell in enumerate(row):
                rect = pygame.Rect(c * cell_width + STUDENT_NUMBER_WIDTH, r * cell_height + TITLE_HEIGHT, cell_width, cell_height)
                cell_color = cell.get("color", WHITE) if cell["clicked"] else WHITE
                pygame.draw.rect(screen, cell_color, rect)
                pygame.draw.rect(screen, BLACK, rect, 2)

                text = font.render(cell["value"], True, BLACK)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

                if cell["clicked"] and cell["mark"]:
                    mark_image = checkmark_image if cell["mark"] == "check" else cross_image
                    mark_rect = mark_image.get_rect(center=rect.center)
                    screen.blit(mark_image, mark_rect)

        # Teken info-paneel
        info_panel_x = WIDTH - INFO_PANEL_WIDTH
        pygame.draw.rect(screen, BLACK, (info_panel_x, 0, INFO_PANEL_WIDTH, HEIGHT))

        score_text = font_title.render(f"Score: {round(score)} / {MAX_SCORE}", True, WHITE)
        time_text = font_title.render(f"Tijd: {int(max(remaining_time, 0))}s", True, WHITE)
        missing_text = font_title.render(f"Missing: {found_missing}/{total_missing}", True, MISSING_COLOR)
        incorrect_text = font_title.render(f"Incorrect: {found_incorrect}/{total_incorrect}", True, INCORRECT_COLOR)
        wrong_text = font_title.render(f"Fouten: {wrong_clicks}", True, WHITE)

        screen.blit(score_text, (info_panel_x + 20, 20))
        screen.blit(time_text, (info_panel_x + 20, 60))
        screen.blit(missing_text, (info_panel_x + 20, 120))
        screen.blit(incorrect_text, (info_panel_x + 20, 160))
        screen.blit(wrong_text, (info_panel_x + 20, 200))

        # Teken de bezem op de positie van de muis
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(brush_image, (mouse_x, mouse_y))

        pygame.display.flip()
    pygame.quit()
