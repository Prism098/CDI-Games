import pygame
import cv2
import numpy as np
from game import run_game  # Ensure this import path matches your project structure

class Button:
    def __init__(self, x, y, width, height, text, font, text_color, bg_color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color

    def draw(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.bg_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

def show_demo_page():
    pygame.init()
    screen_width = 1920
    screen_height = 1080
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("HCI game - Tutorial")

    # Initialize video capture
    video = cv2.VideoCapture("CDI_Games_HCI/assets/DemoVideo.mp4")
    if not video.isOpened():
        print("Error: Could not load video.")
        return

    video_width = 400
    video_height = 300

    # Load and resize the tutorial image
    tutorial_image = pygame.image.load("CDI_Games_HCI/assets/TutorialHCI.png")
    new_width = 1500
    new_height = 840
    tutorial_image = pygame.transform.scale(tutorial_image, (new_width, new_height))

    # Set up fonts
    title_font = pygame.font.SysFont("Arial", 48, bold=True)
    button_font = pygame.font.SysFont("Arial", 24)

    # Position title
    title_text = title_font.render("Human Computer Interaction game - Tutorial", True, (255, 255, 255))
    title_rect = title_text.get_rect(
        centerx=screen_width // 2,
        top=60
    )

    # Position image
    image_rect = tutorial_image.get_rect(
        centerx=screen_width // 2,
        top=title_rect.bottom + 60
    )

    # Position video above the image
    video_x = (screen_width - video_width) - 350
    video_y = image_rect.top - video_height + 300

    # Create Start Game button
    button_width = 200
    start_button = Button(
        x=(screen_width - button_width) // 2,
        y=image_rect.bottom,
        width=button_width,
        height=50,
        text="Start Game",
        font=button_font,
        text_color=(0, 0, 0),
        bg_color=(239, 125, 87),
        hover_color=(200, 200, 200)
    )

    # Global exit flag to track when the entire program should stop
    global_exit = False

    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the demo page
                global_exit = True  # Set flag to exit the entire program

            if start_button.handle_event(event):
                video.release()  # Release video resources
                result = run_game()  # Start the game and capture its result

                if result == "exit":
                    running = False  # Stop the demo page loop
                    global_exit = True  # Ensure the program exits entirely
                    break  # Break out of the loop immediately

        if global_exit:  # Exit the entire program
            break

        # Draw background
        screen.fill((26, 28, 44))

        # Draw tutorial image
        screen.blit(tutorial_image, image_rect)

        # Read and display video frame
        ret, frame = video.read()
        if ret:
            # If video ends, loop it with a 1-second delay
            if video.get(cv2.CAP_PROP_POS_FRAMES) >= video.get(cv2.CAP_PROP_FRAME_COUNT):
                pygame.time.wait(1000)
                video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = video.read()

            # Resize and convert frame to display in Pygame
            frame = cv2.resize(frame, (video_width, video_height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_surface = pygame.surfarray.make_surface(np.flipud(np.rot90(frame)))

            # Display the video frame
            screen.blit(frame_surface, (video_x, video_y))

        else:
            # Reset video if it can't be read
            pygame.time.wait(1000)
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)

        # Draw title and Start Game button
        screen.blit(title_text, title_rect)
        start_button.draw(screen)

        pygame.display.flip()

    # Cleanup
    video.release()
    pygame.quit()

    if global_exit:
        exit()  # Terminate the entire application
