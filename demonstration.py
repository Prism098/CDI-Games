import pygame
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

    # Load and resize the tutorial image
    tutorial_image = pygame.image.load("assets/TutorialHCI.png")
    new_width = 1500
    new_height = 650
    tutorial_image = pygame.transform.scale(tutorial_image, (new_width, new_height))

    # Set up fonts
    title_font = pygame.font.SysFont("Arial", 48, bold=True)
    button_font = pygame.font.SysFont("Arial", 24)

    # Position title at the top with proper spacing (about 100px from top)
    title_text = title_font.render("HCI game - Tutorial", True, (255, 255, 255))
    title_rect = title_text.get_rect(
        centerx=screen_width // 2,
        top=100  # Fixed position from top
    )

    # Position image below title with some spacing
    image_rect = tutorial_image.get_rect(
        centerx=screen_width // 2,
        top=title_rect.bottom + 60  # Increased spacing after title
    )

    # Create button with more space between image and button
    button_width = 200
    start_button = Button(
        x=(screen_width - button_width) // 2,
        y=image_rect.bottom + 100,  # Increased spacing after image
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
                pygame.quit()
            if start_button.handle_event(event):
                run_game()

        if not pygame.get_init():
            break

        # Draw everything
        screen.fill((59, 92, 201))  # Blue background color
        screen.blit(title_text, title_rect)
        screen.blit(tutorial_image, image_rect)
        start_button.draw(screen)
        pygame.display.flip()

    pygame.quit()