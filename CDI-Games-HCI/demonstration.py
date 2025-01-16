import pygame
import sys
import cv2

# Initialize Pygame and the font module
pygame.init()
pygame.font.init()

# Screen dimensions
ORANGE = (255, 98, 40)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
DARK_GREY = (150, 150, 150)
FONT = None
TITLE_FONT = None
BUTTON_FONT = None
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Persona Perfect")

# Initialize fonts
def initialize_fonts():
    global FONT, TITLE_FONT, BUTTON_FONT
    FONT = pygame.font.SysFont("arial", 36)
    TITLE_FONT = pygame.font.SysFont("arial", 60)
    BUTTON_FONT = pygame.font.SysFont("arial", 28)

# Function to get the current frame of the video
def get_video_frame(page_number):
    if page_number == 1:
        ret, frame = video_capture_page1.read()
    elif page_number == 2:
        ret, frame = video_capture_page2.read()
    else:
        return None  # No video on other pages

    if not ret:
        # If the video reaches the end, reset it to the beginning
        if page_number == 1:
            video_capture_page1.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset to the first frame for page 1
            ret, frame = video_capture_page1.read()
        elif page_number == 2:
            video_capture_page2.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset to the first frame for page 2
            ret, frame = video_capture_page2.read()

    # Flip the frame horizontally to mirror it
    frame = cv2.flip(frame, 1)  # 1 for horizontal flip
    # Convert the BGR frame to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame


# Draw a page with a page number and specific content and title for each page
# Draw a page with a page number and specific content and title for each page
def draw_page(screen, page_number, video_playing=False):
    screen.fill(WHITE)  # Clear the screen

    # Define specific titles for each page
    if page_number == 1:
        title_text = TITLE_FONT.render("Analyseer", True, ORANGE)
    elif page_number == 2:
        title_text = TITLE_FONT.render("Sleep", True, ORANGE)
    elif page_number == 3:
        title_text = TITLE_FONT.render("Design!", True, ORANGE)
    else:
        title_text = TITLE_FONT.render("Onbekende Pagina", True, ORANGE)

    # Center the title
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 6))
    screen.blit(title_text, title_rect)

    # If video is playing on this page, show the video (on pages 1 and 2)
    if video_playing:
        video_frame = get_video_frame(page_number)
        if video_frame is not None:
            # Rotate the video 90 degrees counterclockwise
            video_frame = cv2.rotate(video_frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            # Resize the video to a smaller width, keeping the aspect ratio
            video_frame = cv2.resize(video_frame, (420, 600))  # Resize as desired
            video_frame = pygame.surfarray.make_surface(video_frame)
            # Position the video in the center horizontally and move it upwards
            video_rect = video_frame.get_rect(centerx=WIDTH // 2, top=HEIGHT // 3.5)  # Keep video at the same position
            screen.blit(video_frame, video_rect.topleft)  # Draw the resized video

    # Define specific content for each page
    if page_number == 1:
        content_text = "Bekijk deze persoon en hou rekening met de gegeven kenmerken."
    elif page_number == 2:
        content_text = "Sleep de objecten naar het vlak."
    elif page_number == 3:
        content_text = "Design een passende website voor deze persoon.\nDenk goed na over welke elementen het meest passen bij deze persoon."
    else:
        content_text = "Onbekende inhoud"

    # If it's page 3, split and center the content text
    if page_number == 3:
        # Split the text into multiple lines based on \n
        lines = content_text.split("\n")
        line_height = FONT.get_height()
        # Calculate the y-coordinate to center the text
        total_height = line_height * len(lines)
        start_y = (HEIGHT - total_height) // 2  # This centers the text vertically

        # Render each line and position it
        for i, line in enumerate(lines):
            rendered_text = FONT.render(line, True, BLACK)
            line_rect = rendered_text.get_rect(center=(WIDTH // 2, start_y + i * line_height))
            screen.blit(rendered_text, line_rect)
    else:
        # For other pages, center the content text as before
        content_text_rendered = FONT.render(content_text, True, BLACK)
        content_rect = content_text_rendered.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(content_text_rendered, content_rect)



# Draw navigation buttons
def draw_navigation_buttons(screen, current_page):
    button_width = 150
    button_height = 50

    # Define the "Prev" button
    prev_button_rect = pygame.Rect(100, HEIGHT - 100, button_width, button_height)
    pygame.draw.rect(screen, DARK_GREY if current_page > 1 else WHITE, prev_button_rect)
    prev_text = BUTTON_FONT.render("Terug", True, BLACK if current_page > 1 else WHITE)
    prev_text_rect = prev_text.get_rect(center=prev_button_rect.center)
    screen.blit(prev_text, prev_text_rect)

    # Define the "Next" button
    next_button_rect = pygame.Rect(WIDTH - 100 - button_width, HEIGHT - 100, button_width, button_height)
    pygame.draw.rect(screen, DARK_GREY if current_page < 3 else WHITE, next_button_rect)
    next_text = BUTTON_FONT.render("Volgende", True, BLACK if current_page < 3 else WHITE)
    next_text_rect = next_text.get_rect(center=next_button_rect.center)
    screen.blit(next_text, next_text_rect)

    # Define the "Start Game" button (only on Page 3)
    start_button_rect = None
    if current_page == 3:
        start_button_rect = pygame.Rect((WIDTH - button_width) // 2, HEIGHT - 150, button_width, button_height)
        pygame.draw.rect(screen, ORANGE, start_button_rect)
        start_text = BUTTON_FONT.render("Start!", True, BLACK)
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        screen.blit(start_text, start_text_rect)

    return prev_button_rect, next_button_rect, start_button_rect

# Function to show pages
def show_pages():
    initialize_fonts()

    # Open the video files for both pages
    global video_capture_page1, video_capture_page2
    video_capture_page1 = cv2.VideoCapture("CDI-Games-HCI/assets/Demo_Page1.mp4")  # Path for page 1 video
    video_capture_page2 = cv2.VideoCapture("CDI-Games-HCI/assets/Demo_Page2.mp4")  # Path for page 2 video

    current_page = 1
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle button clicks
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()

                # Check for "Prev" button click
                if prev_button_rect.collidepoint(mouse_pos) and current_page > 1:
                    current_page -= 1

                # Check for "Next" button click
                if next_button_rect.collidepoint(mouse_pos) and current_page < 3:
                    current_page += 1

                # Check for "Start Game" button click
                if start_button_rect and start_button_rect.collidepoint(mouse_pos):
                    running = False  # Exit page manager to start the game

        # Draw the current page
        video_playing = current_page == 1 or current_page == 2  # Play video on page 1 and page 2
        draw_page(screen, current_page, video_playing)

        # Draw navigation buttons
        prev_button_rect, next_button_rect, start_button_rect = draw_navigation_buttons(screen, current_page)

        pygame.display.flip()
        clock.tick(60)