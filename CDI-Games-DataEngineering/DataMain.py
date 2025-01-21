import pygame
import sys
import time
import random

# pygame.init()

# --- CONSTANTEN & VENSTEREIGENSCHAPPEN ---
WIDTH = 1400
HEIGHT = 800
INFO_PANEL_WIDTH = 300  # Paneel aan de rechterkant
FPS = 60

# Kleuren
GREY = (160, 160, 160)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 100, 255)
DARKGREY = (50, 50, 50)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Dataset Cleaning Game")
pygame.font.init()

clock = pygame.time.Clock()

GAME_AREA_WIDTH = WIDTH - INFO_PANEL_WIDTH
GAME_AREA_HEIGHT = HEIGHT

# --- STATES ---
GAME_STATE_PLAY = 0
GAME_STATE_END = 1
game_state = GAME_STATE_PLAY

# --- DATASET ---
COLUMNS = 6
ROWS = 8
CELL_WIDTH = GAME_AREA_WIDTH // COLUMNS
CELL_HEIGHT = (GAME_AREA_HEIGHT - 100) // ROWS

dataset = []
outlier_count = 0
missing_count = 0
incorrect_count = 0

for r in range(ROWS):
    row_data = []
    for c in range(COLUMNS):
        rnd = random.random()
        if rnd < 0.10:
            status = "missing"
            missing_count += 1
        elif rnd < 0.25:
            status = "outlier"
            outlier_count += 1
        elif rnd < 0.40:
            status = "incorrect"
            incorrect_count += 1
        else:
            status = "correct"

        if status == "missing":
            value_str = ""
        elif status == "outlier":
            value_str = str(random.randint(-50, -1)) + "km"
        elif status == "incorrect":
            value_str = str(random.randint(-5, 5)) + "??"
        else:
            value_str = str(random.randint(0, 20)) + "km"

        row_data.append({
            "status": status,
            "value": value_str,
            "clicked": False,
            "mark": None  # "check" of "cross"
        })
    dataset.append(row_data)

# Tellen welke al gevonden zijn
found_outliers = 0
found_missing = 0
found_incorrect = 0

score = 0
start_time = time.time()
final_time = None

# Punten
POINTS_OUTLIER = 2
POINTS_MISSING = 1
POINTS_INCORRECT = 3
PENALTY_WRONG = -1


def calculate_multiplier(elapsed):
    if elapsed <= 10:
        return 2.0
    elif elapsed <= 30:
        return 1.5
    else:
        return 1.0


def all_errors_found():
    return (found_outliers >= outlier_count and
            found_missing >= missing_count and
            found_incorrect >= incorrect_count)


running = True
while running:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == GAME_STATE_PLAY:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x < GAME_AREA_WIDTH:
                    col = mouse_x // CELL_WIDTH
                    row = mouse_y // CELL_HEIGHT
                    if row < ROWS and col < COLUMNS:
                        cell = dataset[row][col]
                        if not cell["clicked"]:
                            cell["clicked"] = True
                            status = cell["status"]
                            if status == "outlier":
                                score += POINTS_OUTLIER
                                found_outliers += 1
                                cell["mark"] = "check"
                            elif status == "missing":
                                score += POINTS_MISSING
                                found_missing += 1
                                cell["mark"] = "check"
                            elif status == "incorrect":
                                score += POINTS_INCORRECT
                                found_incorrect += 1
                                cell["mark"] = "check"
                            else:
                                # correct aangeklikt = fout
                                score += PENALTY_WRONG
                                cell["mark"] = "cross"

                            if all_errors_found():
                                # Game over
                                game_state = GAME_STATE_END
                                final_time = time.time() - start_time

        elif game_state == GAME_STATE_END:
            # Geen interactie nodig, eventueel knoppen om opnieuw te starten kunnen hier
            print(f"Score: {int(score * multiplier)}")  # Voeg deze regel toe
            running = False  # Zorg ervoor dat het spel stopt


    # --- TEKENEN ---
    screen.fill(BLACK)

    if game_state == GAME_STATE_PLAY:
        elapsed_time = time.time() - start_time
        multiplier = calculate_multiplier(elapsed_time)
        display_score = int(score * multiplier)

        # Teken cells
        for r in range(ROWS):
            for c in range(COLUMNS):
                x = c * CELL_WIDTH
                y = r * CELL_HEIGHT
                rect = pygame.Rect(x, y, CELL_WIDTH, CELL_HEIGHT)

                cell = dataset[r][c]

                # Altijd grijze achtergrond
                pygame.draw.rect(screen, GREY, rect)

                # Data tekst tekenen (altijd zichtbaar)
                font = pygame.font.SysFont(None, 30)
                text_surf = font.render(cell["value"], True, BLACK)
                text_rect = text_surf.get_rect(center=rect.center)
                screen.blit(text_surf, text_rect)

                # Als de cel is aangeklikt, geef deze een gekleurde rand + markering
                if cell["clicked"]:
                    status = cell["status"]

                    # Bepaal de randkleur op basis van status
                    if status == "outlier":
                        border_color = BLUE
                    elif status == "missing":
                        border_color = YELLOW
                    elif status == "incorrect":
                        border_color = RED
                    else:
                        border_color = GREY

                    # Teken een dikkere rand om de cel
                    border_thickness = 5
                    pygame.draw.rect(screen, border_color, rect, border_thickness)

                # Data-tekst
                font = pygame.font.SysFont(None, 30)
                text_surf = font.render(cell["value"], True, BLACK)
                text_rect = text_surf.get_rect(center=rect.center)
                screen.blit(text_surf, text_rect)

                # Checkmark of cross groot en centraal
                if cell["mark"] == "check":
                    check_font = pygame.font.SysFont(None, int(min(CELL_WIDTH, CELL_HEIGHT) * 0.8), bold=True)
                    check_surf = check_font.render("V", True, GREEN)
                    check_rect = check_surf.get_rect(center=rect.center)
                    screen.blit(check_surf, check_rect)
                elif cell["mark"] == "cross":
                    cross_font = pygame.font.SysFont(None, int(min(CELL_WIDTH, CELL_HEIGHT) * 0.8), bold=True)
                    cross_surf = cross_font.render("X", True, RED)
                    cross_rect = cross_surf.get_rect(center=rect.center)
                    screen.blit(cross_surf, cross_rect)

                # Rand
                pygame.draw.rect(screen, BLACK, rect, 2)

        # Infopaneel rechts
        panel_rect = pygame.Rect(GAME_AREA_WIDTH, 0, INFO_PANEL_WIDTH, HEIGHT)
        pygame.draw.rect(screen, DARKGREY, panel_rect)

        font_panel = pygame.font.SysFont(None, 36)
        title_surf = font_panel.render("Instructies:", True, WHITE)
        screen.blit(title_surf, (GAME_AREA_WIDTH + 20, 20))

        # Zet simpelweg neer: Zoek alle outliers, missing, incorrect
        instruct_line1 = "Zoek Outliers (blauw),"
        instruct_line2 = "Missing (geel),"
        instruct_line3 = "Foutief (rood)."

        l1 = font_panel.render(instruct_line1, True, WHITE)
        l2 = font_panel.render(instruct_line2, True, WHITE)
        l3 = font_panel.render(instruct_line3, True, WHITE)

        screen.blit(l1, (GAME_AREA_WIDTH + 20, 60))
        screen.blit(l2, (GAME_AREA_WIDTH + 20, 100))
        screen.blit(l3, (GAME_AREA_WIDTH + 20, 140))

        # Toon aantallen gevonden
        text_outliers = f"Outliers: {found_outliers}/{outlier_count}"
        text_missing = f"Missing:  {found_missing}/{missing_count}"
        text_incorrect = f"Foutief:  {found_incorrect}/{incorrect_count}"

        outlier_surf = font_panel.render(text_outliers, True, BLUE)
        missing_surf = font_panel.render(text_missing, True, YELLOW)
        incorrect_surf = font_panel.render(text_incorrect, True, RED)

        screen.blit(outlier_surf, (GAME_AREA_WIDTH + 20, 200))
        screen.blit(missing_surf, (GAME_AREA_WIDTH + 20, 240))
        screen.blit(incorrect_surf, (GAME_AREA_WIDTH + 20, 280))

        penalty_text = f"Fout: {PENALTY_WRONG} pnt"
        penalty_surf = font_panel.render(penalty_text, True, WHITE)
        screen.blit(penalty_surf, (GAME_AREA_WIDTH + 20, 320))

        # Score en tijd onderin links
        score_font = pygame.font.SysFont(None, 50)
        score_text = f"Score: {display_score} | Tijd: {elapsed_time:.1f}s"
        score_surf = score_font.render(score_text, True, WHITE)
        screen.blit(score_surf, (20, HEIGHT - 80))

    else:
        # EINDSCHERM
        # Gebruik final_time (gestopt toen alles gevonden was)
        multiplier = calculate_multiplier(final_time)
        final_score = int(score * multiplier)

        screen.fill(BLACK)
        font_end = pygame.font.SysFont(None, 80)
        end_text = f"GAME OVER"
        end_surf = font_end.render(end_text, True, WHITE)
        end_rect = end_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        screen.blit(end_surf, end_rect)

        # Toon eindscore
        score_font = pygame.font.SysFont(None, 60)
        score_text = f"Eindscore: {final_score}"
        score_surf = score_font.render(score_text, True, WHITE)
        score_rect = score_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(score_surf, score_rect)

        # Toon totale tijd
        time_text = f"Totale tijd: {final_time:.1f}s"
        time_surf = score_font.render(time_text, True, WHITE)
        time_rect = time_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        screen.blit(time_surf, time_rect)

        # Sluit tekst
        font_small = pygame.font.SysFont(None, 40)
        close_text = "Sluit dit venster om af te sluiten."
        close_surf = font_small.render(close_text, True, WHITE)
        close_rect = close_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 160))
        screen.blit(close_surf, close_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
