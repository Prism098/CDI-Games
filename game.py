import pygame
from UI_element import DraggableUIElement
from UI_config import create_ui_elements
from personas import randomize_personas_positions
from score import ScoreSystem

class GameState:
    def __init__(self):
        self.canvas_color = (250, 250, 250)  # GREY
        self.canvas_image = None
        self.canvas_font = None
        self.round = 1
        self.score_system = ScoreSystem(initial_score=700, penalty=300)
        self.selected_persona = None

    def reset_canvas(self):
        self.canvas_color = (250, 250, 250)
        self.canvas_image = None
        self.canvas_font = None

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

    running = True
    while running:
        pygame.time.Clock().tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle different rounds
            if game_state.round == 1:  # Color selection
                for ui_element in ui_elements_color:
                    color = ui_element.handle_event(event, canvas_rect)
                    if color:
                        if color == game_state.selected_persona.correct_color:
                            game_state.canvas_color = color
                            game_state.round = 2  # Move to image selection
                        else:
                            game_state.score_system.apply_penalty()
                            ui_element.reset_position()

            elif game_state.round == 2:  # Image selection
                for ui_element in ui_elements_photo:
                    if ui_element.handle_event(event, canvas_rect):
                        if ui_element.color_or_image == game_state.selected_persona.correct_image:
                            # Load and scale the correct image
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
                        else:
                            game_state.score_system.apply_penalty()
                            ui_element.reset_position()

            elif game_state.round == 3:  # Font selection
                for ui_element in ui_elements_font:
                    if ui_element.handle_event(event, canvas_rect):
                        if ui_element.font_name == game_state.selected_persona.correct_font:
                            game_state.canvas_font = ui_element.font_name
                            pygame.time.wait(1000)  # Show completed design for 1 second
                            # Reset for next round
                            game_state.round = 1
                            game_state.selected_persona = randomize_personas_positions(screen_height)
                            game_state.reset_canvas()
                        else:
                            game_state.score_system.apply_penalty()
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

        # Draw current UI elements based on round
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

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    run_game()