import pygame
from UI_element import DraggableUIElement
from UI_config import create_ui_elements
from personas import randomize_personas_positions
from score import ScoreSystem
from text_renderer import render_multiline_text  # Import the new text rendering logic


class GameState:
    def __init__(self):
        self.canvas_color = (250, 250, 250)  # GREY
        self.canvas_image = None
        self.canvas_font = None
        self.round = 1
        self.score_system = ScoreSystem(initial_score=2100, penalty=300)
        self.selected_persona = None
        self.showing_score = False  # New state for score screen
        self.score_screen_timer = 0  # Timer for score screen
        self.feedback_message = None  # New attribute to hold feedback
        self.feedback_timer = 0  # To track feedback duration
        self.score_printed = False  # Flag to check if score is printed


class Button:
    def __init__(self, x, y, width, height, text, font, text_color, bg_color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color

    def draw(self, screen):
        # Check if the mouse is hovering over the button
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.bg_color, self.rect)
        
        # Draw text on the button
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        # Handle mouse click event
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True  # Return True if the button is clicked
        return False


def draw_score_screen(screen, score, exit_button):
    """Draw the end of round score screen"""
    # Create semi-transparent overlay
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (0, 0, 0, 128), overlay.get_rect())
    screen.blit(overlay, (0, 0))

    # Create score box
    box_width = 400
    box_height = 300
    box_x = (screen.get_width() - box_width) // 2
    box_y = (screen.get_height() - box_height) // 2
    
    # Draw white background box
    pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height), 2)

    # Draw title
    font_large = pygame.font.SysFont('Arial', 48, bold=True)
    font_normal = pygame.font.SysFont('Arial', 32)
    
    title = font_large.render("Game over!", True, (0, 0, 0))
    title_rect = title.get_rect(centerx=screen.get_width()//2, top=box_y + 40)
    screen.blit(title, title_rect)

    # Draw score
    score_text = font_normal.render(f"Eind score: {score}", True, (0, 0, 0))
    score_rect = score_text.get_rect(centerx=screen.get_width()//2, top=box_y + 120)
    screen.blit(score_text, score_rect)

    # Draw "Next Round" message
    next_text = font_normal.render("", True, (0, 0, 0))
    next_rect = next_text.get_rect(centerx=screen.get_width()//2, top=box_y + 200)
    screen.blit(next_text, next_rect)

    # Draw the exit button
    exit_button.draw(screen)


def run_game():
    pygame.init()
    
    # Screen setup
    screen_width = 1300
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Persona Design Game")

    # Canvas setup
    canvas_x = 250
    canvas_y = 100
    canvas_width = 800
    canvas_height = 500
    canvas_rect = pygame.Rect(canvas_x, canvas_y, canvas_width, canvas_height)

    # Load browser image
    browser_image = pygame.image.load("assets/Browser.png")
    browser_image = pygame.transform.scale(browser_image, (800, 600))

    # Create UI elements
    ui_elements_color, ui_elements_photo, ui_elements_font = create_ui_elements(
        canvas_x, canvas_y, canvas_width, canvas_height, 50
    )

    # Initialize game state
    game_state = GameState()
    game_state.selected_persona = randomize_personas_positions(screen_height)

    # Create the exit button (button is drawn on the score screen)
    font = pygame.font.SysFont('Arial', 32)
    exit_button = Button(
        x=(1100) // 2, y=(520), width=200, height=50,
        text="Exit Game", font=font, text_color=(0, 0, 0), bg_color=(150, 150, 150), hover_color=(200, 200, 200)
    )

    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle exit button click on score screen
            if game_state.showing_score and exit_button.handle_event(event):
                running = False  # Exit the game if the button is clicked

            # Only handle drag and drop if not showing score screen
            if not game_state.showing_score:
                if game_state.round == 1:  # Color selection
                    for ui_element in ui_elements_color:
                        color = ui_element.handle_event(event, canvas_rect)
                        if color:
                            if color == game_state.selected_persona.correct_color:
                                game_state.canvas_color = color
                                game_state.round = 2  # Move to image selection
                                game_state.feedback_message = None  # Clear feedback after correct answer
                            else:
                                game_state.score_system.apply_penalty()
                                game_state.feedback_message = "Hou rekening\nmet de persona!"  # Wrong color feedback
                                ui_element.reset_position()

                elif game_state.round == 2:  # Image selection
                    for ui_element in ui_elements_photo:
                        if ui_element.handle_event(event, canvas_rect):
                            if ui_element.color_or_image == game_state.selected_persona.correct_image:
                                margin = 20
                                image = pygame.image.load(ui_element.color_or_image)
                                image = pygame.transform.scale(image, (200, 200))
                                image_rect = image.get_rect()
                                image_rect.bottomright = (
                                    canvas_rect.right - margin,
                                    canvas_rect.bottom - margin
                                )
                                game_state.canvas_image = (image, image_rect)
                                game_state.round = 3  # Move to font selection
                                game_state.feedback_message = None  # Clear feedback after correct answer
                            else:
                                game_state.score_system.apply_penalty()
                                game_state.feedback_message = "Hou rekening\nmet de persona!"  # Wrong image feedback
                                ui_element.reset_position()

                elif game_state.round == 3:  # Font selection
                    for ui_element in ui_elements_font:
                        if ui_element.handle_event(event, canvas_rect):
                            if ui_element.font_name == game_state.selected_persona.correct_font:
                                game_state.canvas_font = ui_element.font_name
                                # Show score screen
                                game_state.showing_score = True
                                game_state.score_screen_timer = pygame.time.get_ticks()
                                game_state.feedback_message = None  # Clear feedback after correct answer
                            else:
                                game_state.score_system.apply_penalty()
                                game_state.feedback_message = "Hou rekening\nmet de persona!"  # Wrong font feedback
                                ui_element.reset_position()

        # Draw everything
        screen.fill((255, 255, 255))  # White background
        screen.blit(browser_image, (250, 10))
        
        # Draw canvas with current color
        pygame.draw.rect(screen, game_state.canvas_color, canvas_rect)
        
        # Draw selected persona
        game_state.selected_persona.draw(screen)
        
        # Draw applied image if exists
        if game_state.canvas_image:
            image, image_rect = game_state.canvas_image
            screen.blit(image, image_rect.topleft)

        # Draw applied font if exists
        if game_state.canvas_font:
            font = pygame.font.SysFont(game_state.canvas_font, 36)
            text = font.render("Sample Text", True, (0, 0, 0))
            text_rect = text.get_rect(center=canvas_rect.center)
            screen.blit(text, text_rect)

        # Draw current UI elements if not showing score
        if not game_state.showing_score:
            current_elements = {
                1: ui_elements_color,
                2: ui_elements_photo,
                3: ui_elements_font
            }.get(game_state.round, [])
            
            for ui_element in current_elements:
                ui_element.draw(screen)

        # Draw score
        font = pygame.font.SysFont('Arial', 30)
        score_text = font.render(f"Score: {game_state.score_system.get_score()}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # Handle feedback message with line breaks
        if game_state.feedback_message:
            feedback_font = pygame.font.SysFont('Arial', 24, bold=True)
            render_multiline_text(screen, game_state.feedback_message, feedback_font, (255, 0, 0), screen.get_width() - 200, screen.get_height() - 700)

        # Handle score screen
        if game_state.showing_score:
            draw_score_screen(screen, game_state.score_system.get_score(), exit_button)

            # Print the score to the terminal only once
            if not game_state.score_printed:
                print(f"Final score: {game_state.score_system.get_score()}")
                game_state.score_printed = True  # Set the flag to prevent printing again

        pygame.display.flip()

    pygame.quit()
