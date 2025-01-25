import pygame
import cv2
import numpy as np
import os

WIDTH, HEIGHT = 1920, 1080
WHITE = (244, 244, 244)
BACKGROUND_COLOR = (26, 28, 44)
TEXT_COLOR = WHITE
VIDEO_BOX_COLOR = (26, 28, 44)

def show_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Car IDE - Menu")

    video_path = os.path.join("CDI_Games_SoftwareDevelopment", "videos", "tutorial_vid.mp4")
    video = cv2.VideoCapture(video_path)


    if not video.isOpened():
        print("Error: Could not load video.")
        return "quit"

    running = True
    clock = pygame.time.Clock()

    while running:
        pygame.font.init()
        screen.fill(BACKGROUND_COLOR)

        # Fonts
        title_font = pygame.font.Font(None, 80)
        text_font = pygame.font.Font(None, 40)
        instruction_font = pygame.font.Font(None, 30)

        # Render texts
        title = title_font.render("Welkom bij CAR I.D.E", True, TEXT_COLOR)
        instruction = text_font.render("Je hebt 35 seconden om de hoogste score te behalen!", True, TEXT_COLOR)
        explanation = instruction_font.render(
            "Klik op de input-blokken en navigeer de auto naar de finish!", True, TEXT_COLOR
        )
        video_notice = instruction_font.render(
            "Klik ENTER om te starten.", True, TEXT_COLOR
        )

        # Positions
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 8))
        screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT // 4))
        screen.blit(explanation, (WIDTH // 2 - explanation.get_width() // 2, HEIGHT // 3))

        # Draw video box
        video_width, video_height = 600, 400
        video_x = WIDTH // 2 - video_width // 2
        video_y = (HEIGHT // 2 - video_height // 2)+ 100
        pygame.draw.rect(screen, VIDEO_BOX_COLOR, (video_x, video_y, video_width, video_height))

        # Display video frame
        ret, frame = video.read()
        if ret:
            if video.get(cv2.CAP_PROP_POS_FRAMES) >= video.get(cv2.CAP_PROP_FRAME_COUNT):
                video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = video.read()

            frame = cv2.resize(frame, (video_width, video_height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_surface = pygame.surfarray.make_surface(np.flipud(np.rot90(frame)))
            screen.blit(frame_surface, (video_x, video_y + 50))
        else:
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)

        # Display text under the video
        screen.blit(video_notice, (WIDTH // 2 - video_notice.get_width() // 2, video_y + video_height + 80))

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                video.release()
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    video.release()
                    return "start"
                elif event.key == pygame.K_ESCAPE:
                    video.release()
                    return "quit"

        clock.tick(60)  # Limit FPS

    pygame.quit()
