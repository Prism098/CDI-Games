import pygame
from UI_element import DraggableUIElement
from UI_config import create_ui_elements
from personas import randomize_personas_positions  # Import the randomize function from persona.py

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
canvas_rect = pygame.Rect(canvas_x, canvas_y, canvas_width, canvas_height)

# Set up the screen
screen_width = 1300
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Color Drag and Drop")

# Load the browser image
browser_image = pygame.image.load("assets/Browser.png")
browser_image = pygame.transform.scale(browser_image, (browser_width, browser_height))

# Create UI elements (draggable)
ui_elements_color, ui_elements_photo, ui_elements_font = create_ui_elements(
    canvas_x, canvas_y, canvas_width, canvas_height, 50
)

# Set the initial canvas color
canvas_color = GREY

# Set the initial round
round = 1

# Variable to store the image for the canvas
canvas_image = None


# Main game loop
def run_game():
    global canvas_color, canvas_image, round

    # Randomly select and place one persona on the left side of the screen at the start
    selected_persona = randomize_personas_positions(screen_height)

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
                    color = ui_element.handle_event(event, canvas_rect)
                    if color:
                        canvas_color = color
                        round = 2

            # Round 2: Image dragging
            elif round == 2:
                image = None  # Initialize the variable to prevent the UnboundLocalError
                for ui_element in ui_elements_photo:
                    image = ui_element.handle_event(event, canvas_rect)
                    if image:
                        # Check if the image is the CartoonHappyPhoto
                        if ui_element.color_or_image == "assets/CartoonHappyPhoto.png":
                            # Stretch the image vertically while scaling
                            stretch_factor_width = 1.5
                            stretch_factor_height = 2

                            scaled_width = int(image.get_width() * stretch_factor_width)
                            scaled_height = int(image.get_height() * stretch_factor_height)

                            image = pygame.transform.scale(
                                image, (scaled_width, scaled_height)
                            )
                        else:
                            # Scale the other images normally
                            scaled_width = int(image.get_width() * 2)
                            scaled_height = int(image.get_height() * 2)
                            image = pygame.transform.scale(
                                image, (scaled_width, scaled_height)
                            )

                        # Position the image at the bottom-right of the canvas with a margin
                        margin = 20
                        image_rect = image.get_rect()
                        image_rect.bottomright = (
                            canvas_rect.right - margin,
                            canvas_rect.bottom - margin,
                        )

                        # Store the image and its rect for rendering
                        canvas_image = (image, image_rect)
                        round = 3
                        break

            # Round 3: Font dragging
            elif round == 3:
                for ui_element in ui_elements_font:
                    font = ui_element.handle_event(event, canvas_rect)
                    if font:
                        round = 1

        # Fill the screen with white
        screen.fill(WHITE)

        # Draw the browser image
        screen.blit(browser_image, (250, 10))

        # Draw the canvas (background color)
        pygame.draw.rect(
            screen, canvas_color, (canvas_x, canvas_y, canvas_width, canvas_height)
        )

        # Draw the selected persona on the left side of the screen
        selected_persona.draw(screen)

        # Draw the applied image on the canvas if it exists
        if canvas_image:
            image, image_rect = canvas_image
            screen.blit(image, image_rect.topleft)

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
