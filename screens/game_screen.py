import pygame
import os
import random
from data.dataset import generate_dataset
from utils.styles import WIDTH, HEIGHT, INFO_PANEL_WIDTH, GREY, WHITE, BLACK, COLUMN_COLOR, TITLE_HEIGHT, \
    STUDENT_NUMBER_COLOR, OUTLIER_COLOR, MISSING_COLOR, INCORRECT_COLOR, ERROR_COLOR
from screens.end_screen import show_end_screen

def start_game():
    pygame.init()

    # Laad de checkmark- en cross-afbeeldingen en bezem afbeelding
    assets_path = os.path.join(os.path.dirname(__file__), "..", "assets")
    checkmark_image = pygame.image.load(os.path.join(assets_path, "check.png"))
    cross_image = pygame.image.load(os.path.join(assets_path, "cross.png"))
    brush_image = pygame.image.load(os.path.join(assets_path, "brush.png"))

    checkmark_image = pygame.transform.scale(checkmark_image, (80, 80))
    cross_image = pygame.transform.scale(cross_image, (80, 80))
    brush_image = pygame.transform.scale(brush_image, (80, 80))

    # Verberg de standaard cursor
    pygame.mouse.set_visible(False)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dataset Cleaning Game")

    dataset = generate_dataset()
    rows = len(dataset)
    cols = len(dataset[0])

    student_number_width = 250  # Breedte van de kolom voor studentnummers
    cell_width = (WIDTH - INFO_PANEL_WIDTH - student_number_width) // cols
    cell_height = (HEIGHT - TITLE_HEIGHT) // rows

    # Genereer studentnummers
    student_numbers = [f"20{random.randint(10000, 99999)}" for _ in range(rows)]

    score = 0
    start_time = pygame.time.get_ticks()
    clock = pygame.time.Clock()
    running = True

    found_outliers = 0
    found_missing = 0
    found_incorrect = 0
    wrong_clicks = 0

    total_outliers = sum(1 for row in dataset for cell in row if cell["status"] == "outlier")
    total_missing = sum(1 for row in dataset for cell in row if cell["status"] == "missing")
    total_incorrect = sum(1 for row in dataset for cell in row if cell["status"] == "incorrect")
    total_errors = total_outliers + total_missing + total_incorrect

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if mouse_x < WIDTH - INFO_PANEL_WIDTH and mouse_y > TITLE_HEIGHT:
                    col = (mouse_x - student_number_width) // cell_width
                    row = (mouse_y - TITLE_HEIGHT) // cell_height
                    if 0 <= row < rows and 0 <= col < cols:
                        cell = dataset[row][col]
                        if not cell["clicked"]:
                            cell["clicked"] = True
                            if cell["status"] == "outlier":
                                score += 2
                                found_outliers += 1
                                cell["mark"] = "check"
                                cell["color"] = OUTLIER_COLOR  # Verander gridkleur
                            elif cell["status"] == "missing":
                                score += 1
                                found_missing += 1
                                cell["mark"] = "check"
                                cell["color"] = MISSING_COLOR  # Verander gridkleur
                            elif cell["status"] == "incorrect":
                                score += 3
                                found_incorrect += 1
                                cell["mark"] = "check"
                                cell["color"] = INCORRECT_COLOR  # Verander gridkleur
                            else:
                                score -= 1
                                wrong_clicks += 1
                                cell["mark"] = "cross"
                                cell["color"] = GREY

                            if found_outliers + found_missing + found_incorrect == total_errors:
                                elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
                                show_end_screen(
                                    screen,
                                    score,
                                    elapsed_time,
                                    found_outliers,
                                    total_outliers,
                                    found_missing,
                                    total_missing,
                                    found_incorrect,
                                    total_incorrect
                                )
                                return

        screen.fill(BLACK)

        # Teken kolomtitels
        font_title = pygame.font.SysFont(None, 40)
        titles = ["Distance", "Transport", "Average Grade", "Highest Grade", "Birth Date", "Start Date"]
        for i, title in enumerate(titles):
            rect = pygame.Rect(i * cell_width + student_number_width, 0, cell_width, TITLE_HEIGHT)
            pygame.draw.rect(screen, COLUMN_COLOR, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            title_text = font_title.render(title, True, WHITE)
            screen.blit(title_text, (rect.x + (cell_width - title_text.get_width()) // 2, rect.y + 10))

        # Teken de grid en waarden
        font = pygame.font.SysFont(None, 40)
        for r, row in enumerate(dataset):
            # Teken studentnummer
            student_rect = pygame.Rect(0, r * cell_height + TITLE_HEIGHT, student_number_width, cell_height)
            pygame.draw.rect(screen, STUDENT_NUMBER_COLOR, student_rect)  # Nieuwe kleur voor studentnummer-vak
            pygame.draw.rect(screen, BLACK, student_rect, 2)  # Zwarte rand
            student_text = font.render(student_numbers[r], True, WHITE)
            student_text_rect = student_text.get_rect(center=student_rect.center)
            screen.blit(student_text, student_text_rect)

            for c, cell in enumerate(row):
                rect = pygame.Rect(c * cell_width + student_number_width, r * cell_height + TITLE_HEIGHT, cell_width, cell_height)
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
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        info_panel_x = WIDTH - INFO_PANEL_WIDTH
        pygame.draw.rect(screen, BLACK, (info_panel_x, 0, INFO_PANEL_WIDTH, HEIGHT))

        # Render score, tijd en aantal gevonden fouten in het info-paneel
        score_text = font_title.render(f"Score: {score}", True, WHITE)
        time_text = font_title.render(f"Time: {elapsed_time}s", True, WHITE)
        outliers_text = font_title.render(f"Outliers: {found_outliers}/{total_outliers}", True, OUTLIER_COLOR)
        missing_text = font_title.render(f"Missing: {found_missing}/{total_missing}", True, MISSING_COLOR)
        incorrect_text = font_title.render(f"Incorrect: {found_incorrect}/{total_incorrect}", True, INCORRECT_COLOR)
        # Render "Fouten = -1 punt" op één regel
        wrong_text_line1 = font_title.render("Fouten = -1 punt", True, ERROR_COLOR)

        # Render "Aantal fouten: {wrong_clicks}" op de volgende regel
        wrong_text_line2 = font_title.render(f"Aantal fouten: {wrong_clicks}", True, ERROR_COLOR)

        screen.blit(score_text, (info_panel_x + 20, 20))
        screen.blit(time_text, (info_panel_x + 20, 60))
        screen.blit(outliers_text, (info_panel_x + 20, 120))
        screen.blit(missing_text, (info_panel_x + 20, 160))
        screen.blit(incorrect_text, (info_panel_x + 20, 200))
        screen.blit(wrong_text_line1, (info_panel_x + 20, 260))
        screen.blit(wrong_text_line2, (info_panel_x + 20, 300))

        # Teken de bezem op de positie van de muis
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(brush_image, (mouse_x, mouse_y))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
