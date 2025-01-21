import pygame
import cv2
import numpy as np
from game import run_game

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
    video = cv2.VideoCapture("assets/DemoVideo.mp4")
    if not video.isOpened():
        print("Error: Could not load video.")
        return

    video_width = 400
    video_height = 300

    # Load and resize the tutorial image
    tutorial_image = pygame.image.load("assets/TutorialHCI.png")
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
    video_x = (screen_width - video_width) - 350  # Center horizontally
    video_y = image_rect.top - video_height + 250  # Position 250px above the image

    # Create button
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

    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if start_button.handle_event(event):
                video.release()
                run_game()

        # Draw background
        screen.fill((26, 28, 44))

        # Draw tutorial image first
        screen.blit(tutorial_image, image_rect)

        # Read and display video frame
        ret, frame = video.read()
        if ret:
            # If the video ends, loop it with a 1-second delay
            if video.get(cv2.CAP_PROP_POS_FRAMES) >= video.get(cv2.CAP_PROP_FRAME_COUNT):
                pygame.time.wait(1000)  # Wait for 1 second (1000 milliseconds)
                video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = video.read()

            # Resize frame
            frame = cv2.resize(frame, (video_width, video_height))

            # Convert frame from BGR to RGB for Pygame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert frame to Pygame surface
            frame_surface = pygame.surfarray.make_surface(np.flipud(np.rot90(frame)))

            # Draw the video on the screen
            screen.blit(frame_surface, (video_x, video_y))

        else:
            # If video cannot be read, reset to the beginning with a delay
            pygame.time.wait(1000)  # Wait for 1 second (1000 milliseconds)
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)

        # Draw title and button after the video and image
        screen.blit(title_text, title_rect)
        start_button.draw(screen)

        pygame.display.flip()

        if not pygame.get_init():
            break

    # Cleanup
    video.release()
    pygame.quit()
