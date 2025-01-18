import pygame

PERSONA_STORIES = {
    "timesnewroman": """John is a busy professional who values 
efficiency and clear communication. He starts each day at 6 AM,
reviewing emails while enjoying his morning coffee. His carefully
organized calendar helps him balance client meetings with team
management responsibilities.""",
    
    "comicsansms": """Sarah loves spending time in her colorful
playroom! Her favorite activities include drawing pictures of
unicorns, building towering block castles, and making up silly
stories with her stuffed animals. Every day is a new adventure!""",
    
    "couriernew": """Robert enjoys his peaceful retirement days
tending to his garden and sharing stories with his grandchildren.
His wisdom comes from decades of experience, and he takes pride
in passing down family traditions to the younger generations."""
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
    
    max_width = int(canvas_rect.width * 0.8)
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        test_surface = story_font.render(test_line, True, color)
        if test_surface.get_width() <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line))
    
    line_height = story_font.get_linesize()
    total_height = line_height * len(lines)
    
    start_y = canvas_rect.top + (canvas_rect.height * 0.3)
    
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