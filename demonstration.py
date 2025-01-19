import pygame

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
                return True  # Return True if the button is clicked
        return False

def show_demo_page():
    pygame.init()

    # Set screen dimensions
    screen_width = 1200
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("HCI game - Tutorial")

    # Load the TutorialHCI image
    tutorial_image = pygame.image.load("assets/TutorialHCI.png")  # Assuming the image is in the 'assets' folder

    # Set the new dimensions directly (smaller than original size)
    new_width = 1000  # For example, width is reduced to 1000px
    new_height = 650  # For example, height is reduced to 650px

    # Resize the image to the new dimensions
    tutorial_image = pygame.transform.scale(tutorial_image, (new_width, new_height))

    # Set up font
    font = pygame.font.SysFont("Arial", 28)
    button_font = pygame.font.SysFont("Arial", 24)

    # Create the "Start Game" button at the bottom
    start_button = Button(
        x=(screen_width // 2) - 100, y=screen_height - 75, width=200, height=50,
        text="Start Game", font=button_font, text_color=(0, 0, 0), bg_color=(239, 125, 87), hover_color=(200, 200, 200)
    )

    running = True
    clock = pygame.time.Clock()

    # Demo page loop
    while running:
        clock.tick(60)  # Run at 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()  # Quit pygame safely

            if start_button.handle_event(event):  # If button is clicked, start the game
                from game import run_game  # Import and run the game
                run_game()

        if not pygame.get_init():
            break  # If pygame has been quit, stop the loop

        screen.fill((59, 92, 201))  # Set the background to white

        # Draw the TutorialHCI image (fits between the header and the button)
        # Position the image in the center horizontally and below the header
        image_x = (screen_width - new_width) // 2  # Center the image horizontally
        screen.blit(tutorial_image, (image_x, 50))  # Display image below the header (50px is header height)

        # Title text (move higher by setting a smaller top value)
        title_font = pygame.font.SysFont("Arial", 48, bold=True)
        title_text = title_font.render("HCI game - Tutorial", True, (255, 255, 255))
        
        # Adjust the title's position (move it closer to the top)
        title_rect = title_text.get_rect(centerx=screen_width // 2, top=10)  # Set top to 10px for higher placement
        screen.blit(title_text, title_rect)

        # Draw the Start Game button
        start_button.draw(screen)

        pygame.display.flip()

    pygame.quit()  # Ensure that pygame.quit() is called when the loop ends

