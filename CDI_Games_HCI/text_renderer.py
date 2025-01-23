# text_renderer.py

import pygame

def render_multiline_text(screen, text, font, color, x, y):
    """
    Renders multiline text with line breaks at "\n".

    Args:
        screen (pygame.Surface): The surface to render the text on.
        text (str): The text to render, with "\n" as line breaks.
        font (pygame.font.Font): The font to use for rendering the text.
        color (tuple): The color to render the text (R, G, B).
        x (int): The x-coordinate of where the text should start.
        y (int): The y-coordinate of where the text should start.
    """
    # Split the text into lines based on "\n"
    lines = text.split("\n")
    
    # Define the Y-position to start drawing text
    current_y = y

    for line in lines:
        # Render each line of text
        line_surface = font.render(line, True, color)
        line_rect = line_surface.get_rect(x=x, y=current_y)
        
        # Draw the text line on the screen
        screen.blit(line_surface, line_rect)
        
        # Move the Y-position down for the next line
        current_y += line_rect.height
