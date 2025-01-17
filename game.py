import pygame
from UI_element import DraggableUIElement
from UI_config import create_ui_elements

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
ui_elements_color, ui_elements_photo, ui_elements_font = create_ui_elements(canvas_x, canvas_y, canvas_width, canvas_height, 50)

# Set the initial canvas color
canvas_color = GREY

# Set the initial round
round = 1

# Main game loop
def run_game():
    global canvas_color, round

    running = True
    while running:
        # Control frame rate
        pygame.time.Clock().tick(60)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Round 1: Color selection
            if round == 1:
                for ui_element in ui_elements_color:
                    color = ui_element.handle_event(event, canvas_rect)  # Pass the canvas_rect to check if it's inside the canvas
                    if color:
                        canvas_color = color  # Apply color to the canvas if dropped inside it
                        round = 2  # Move to the next round

            # Round 2: Image dragging
            elif round == 2:
                for ui_element in ui_elements_photo:
                    image = ui_element.handle_event(event, canvas_rect)  # Pass the canvas_rect to check if it's inside the canvas
                    if image:
                        round = 3  # Move to the next round

            # Round 3: Font dragging
            elif round == 3:
                for ui_element in ui_elements_font:
                    font = ui_element.handle_event(event, canvas_rect)  # Pass the canvas_rect to check if it's inside the canvas
                    if font:
                        round = 1  # End game or reset to round 1 (you can change this logic based on what happens after font is chosen)

        # Fill the screen with white
        screen.fill(WHITE)
        
        # Draw the browser image
        screen.blit(browser_image, (250, 10))  # Draw the browser image at the top

        # Draw the canvas (background color)
        pygame.draw.rect(screen, canvas_color, (canvas_x, canvas_y, canvas_width, canvas_height))
        
        # Draw the draggable UI elements based on the current round
        if round == 1:
            for ui_element in ui_elements_color:
                ui_element.draw(screen)
        elif round == 2:
            for ui_element in ui_elements_photo:
                ui_element.draw(screen)
        elif round == 3:
            for ui_element in ui_elements_font:
                ui_element.draw(screen)

        # Update the screen display
        pygame.display.flip()

    pygame.quit()

run_game()
