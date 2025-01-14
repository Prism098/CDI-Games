import pygame
import cv2
import sys

# Initialize Pygame and the font module
pygame.init()
pygame.font.init()

from game import GameState

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
pygame.display.set_caption("Website Interface Builder Game")

def initialize_fonts():
    global FONT, TITLE_FONT, BUTTON_FONT
    FONT = pygame.font.SysFont("arial", 24)
    TITLE_FONT = pygame.font.SysFont("arial", 48)
    BUTTON_FONT = pygame.font.SysFont("arial", 36)

def play_video_with_opencv(video_path):
    clock = pygame.time.Clock()

    # Open the video using OpenCV
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video at {video_path}")
        return True  # Start the game directly if video fails to load

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Set up Pygame screen with video dimensions
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Video Playback - Start Screen")

    running = True
    start_game = False

    while running:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop the video
            continue

        # Convert the OpenCV BGR frame to RGB for Pygame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left-click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 0 <= mouse_x <= width and 0 <= mouse_y <= height:  # Double-click starts game
                    start_game = True
                    running = False

        # Display the video frame
        screen.blit(frame_surface, (0, 0))
        pygame.display.update()
        clock.tick(fps)

    cap.release()  # Release OpenCV resources
    return start_game  # Do not call pygame.quit()


def calculate_score(game_state):
    score = 0

    # Check for orange color
    if game_state.grey_color == ORANGE and not game_state.color_condition_met:
        score += 1000
        game_state.color_condition_met = True  # Mark that we've met the color condition

    # Check for happy sticker
    if game_state.sticker_placed and game_state.ui_stickers[0].placed and not game_state.sticker_condition_met:
        score += 1000
        game_state.sticker_condition_met = True  # Mark that we've met the sticker condition

    # Check for Comic Sans
    if game_state.font_name == "comicsansms" and not game_state.font_condition_met:
        score += 1000
        game_state.font_condition_met = True  # Mark that we've met the font condition

    return score

def draw_score_window(screen, total_score, button_rect, mouse_pos):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(150)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    window_width = 400
    window_height = 250  # Increased height to accommodate the button
    window_rect = pygame.Rect(
        (WIDTH - window_width) // 2,
        (HEIGHT - window_height) // 2,
        window_width,
        window_height,
    )
    pygame.draw.rect(screen, WHITE, window_rect)
    pygame.draw.rect(screen, BLACK, window_rect, 2)

    score_text = FONT.render(f"Jouw Score: {total_score}", True, BLACK)
    score_text_rect = score_text.get_rect(center=(window_rect.centerx, window_rect.centery - 40))
    screen.blit(score_text, score_text_rect)

    # Check if the mouse is hovering over the button
    if button_rect.collidepoint(mouse_pos):
        button_color = DARK_GREY
    else:
        button_color = GREY

    # Draw the button
    pygame.draw.rect(screen, button_color, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 2)
    button_text = FONT.render("Exit", True, BLACK)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)

def main():
    # Initialize Pygame and fonts
    pygame.init()
    pygame.font.init()
    initialize_fonts()

    # Path to the video file
    video_path = "CDI-Games-HCI/assets/2025-01-1317-51-44.mp4"  # Replace with your video file name

    # Show the start screen with the video
    if play_video_with_opencv(video_path):
        game_state = GameState()  # Create GameState after fonts are initialized
        clock = pygame.time.Clock()
        running = True
        total_score = 0
        previous_score = total_score  # Initialize previous_score

        # Define button dimensions and position
        button_width = 100
        button_height = 40
        button_x = (WIDTH - button_width) // 2
        button_y = (HEIGHT + 200) // 2  # Positioned below the score window
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        # Print the initial score when the app starts
        print(f"Score: {total_score}")

        while running:
            dt = clock.tick(60) / 1000
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Handle the event
                game_state.handle_event(event)

                # Check if the button is clicked
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                    if button_rect.collidepoint(event.pos):
                        running = False  # Exit the game

                # Calculate score if conditions are met
                score_change = calculate_score(game_state)
                total_score += score_change

                # Ensure the score does not exceed 3000
                total_score = min(total_score, 3000)

                # Update the score in game state
                game_state.score = total_score

                # Print the score only if it has changed
                if total_score != previous_score:
                    print(f"Score: {total_score}")
                    previous_score = total_score

            # Update timer and check for time-based scoring
            game_state.update_timer(dt)

            # Draw everything
            game_state.draw(screen)

            # Draw the score window if the flag is set
            if game_state.show_score_window:
                draw_score_window(screen, total_score, button_rect, mouse_pos)

            pygame.display.flip()

        pygame.quit()
        sys.exit()



if __name__ == "__main__":
    main()
