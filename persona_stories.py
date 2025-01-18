import pygame

PERSONA_STORIES = {
    "timesnewroman": """John is een drukke professional die efficiëntie en duidelijke communicatie waardeert. Hij begint elke dag om 6 uur 's ochtends met het doornemen van e-mails, terwijl hij geniet van zijn ochtendkoffie. Zijn zorgvuldig georganiseerde agenda helpt hem om klantvergaderingen en teammanagementverantwoordelijkheden in balans te houden.""",
    "comicsansms": """Timmy houdt ervan om tijd door te brengen in zijn gezellige speelkamer! Zijn favoriete activiteiten zijn het tekenen van plaatjes van dinosaurussen, het bouwen van enorme Lego kastelen en het verzinnen van spannende verhalen met zijn actiefiguren. Elke dag is een nieuw avontuur!""",
    "brushscript":
"""Albert geniet van zijn rustige pensioen dagen in de tuin en het delen van verhalen met zijn kleinkinderen. Zijn wijsheid komt van decennia aan ervaring en hij is trots op het doorgeven van familietradities aan de jongere generaties.""",
}


def draw_story_text(screen, story, font_name, canvas_rect, color=(0, 0, 0)):
    """
    Renders a story text on the screen with word wrapping and proper positioning.

    Args:
        screen: Pygame screen surface to draw on
        story: String containing the story text
        font_name: Name of the font to use
        canvas_rect: Pygame Rect object defining the canvas area
        color: RGB tuple for text color (default: black)
    """
    story_font = pygame.font.SysFont(font_name, 24)

    words = story.split()
    lines = []
    current_line = []

    # Adjust max_width to allow some padding inside the canvas
    max_width = int(canvas_rect.width * 0.8)

    # Wrap the text into lines
    for word in words:
        test_line = " ".join(current_line + [word])
        test_surface = story_font.render(test_line, True, color)
        if test_surface.get_width() <= max_width:
            current_line.append(word)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
    lines.append(" ".join(current_line))  # Add the last line

    line_height = story_font.get_linesize()  # Get the height of each line of text

    # Set the starting Y position to near the top of the canvas
    start_y = canvas_rect.top + 20  # 20 pixels margin from the top of the canvas

    # Draw each line of text
    for i, line in enumerate(lines):
        text_surface = story_font.render(line, True, color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = canvas_rect.centerx
        text_rect.top = start_y + (i * line_height)
        screen.blit(text_surface, text_rect)


def get_story_for_persona(font_name):
    """
    Returns the story associated with a given persona's font.

    Args:
        font_name: String name of the font

    Returns:
        String containing the story
    """
    return PERSONA_STORIES.get(font_name)
