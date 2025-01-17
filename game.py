import pygame
from UI_config import create_ui_elements  # Import the UI element creation function

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
GREY = (250, 250, 250)

# Define canvas dimensions
browser_width = 800
browser_height = 600
canvas_width = 800
canvas_height = 500
canvas_x = 250
canvas_y = 100
canvas_rect = pygame.Rect(canvas_x, canvas_y, canvas_width, canvas_height)  # Canvas for collision detection

# Set up the screen
screen_width = 1300
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Color Drag and Drop")

# Load the browser image
browser_image = pygame.image.load("assets/Browser.png")
browser_image = pygame.transform.scale(browser_image, (browser_width, browser_height))  # Scale to fit browser dimensions

# Create UI elements (draggable)
ui_elements = create_ui_elements(canvas_x, canvas_y, canvas_width, canvas_height, 50)

# Set the initial canvas color
canvas_color = GREY

# Main game loop
def run_game():
    global canvas_color

    running = True
    while running:
        # Control frame rate
        pygame.time.Clock().tick(60)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle events for each draggable UI element
            for ui_element in ui_elements:
                color = ui_element.handle_event(event, canvas_rect)  # Pass the canvas_rect to check if it's inside the canvas
                if color:
                    canvas_color = color  # Apply color to the canvas if dropped inside it

        # Fill the screen with white
        screen.fill(WHITE)
        
        # Draw the browser image
        screen.blit(browser_image, (250, 10))  # Draw the browser image at the top

        # Draw the canvas (background color)
        pygame.draw.rect(screen, canvas_color, (canvas_x, canvas_y, canvas_width, canvas_height))
        
        # Draw the draggable UI elements
        for ui_element in ui_elements:
            ui_element.draw(screen)
        
        # Update the screen display
        pygame.display.flip()

    pygame.quit()

run_game()
