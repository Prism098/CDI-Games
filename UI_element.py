import pygame

class DraggableUIElement:
    def __init__(self, x, y, width, height, color_or_image, text=None, font=None, font_name=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color_or_image = color_or_image
        self.text = text  # New attribute for text
        self.font = font  # Font for the text
        self.font_name = font_name  # Font name for the text
        
        if isinstance(self.color_or_image, tuple):
            self.is_image = False
            self.color = self.color_or_image  # Color is a tuple like (255, 98, 40)
        else:
            self.is_image = True
            self.image = pygame.image.load(self.color_or_image)  # Load the image if it's a path
            self.image = pygame.transform.scale(self.image, (self.width, self.height))  # Scale to element size
        
        # Store the initial position
        self.initial_x = x
        self.initial_y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.dragging = False

    def handle_event(self, event, canvas_rect):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                return None
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.x, self.y = event.pos
                self.rect.topleft = (self.x, self.y)
                return None
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                if self.rect.collidepoint(event.pos) and canvas_rect.colliderect(self.rect):
                    return self.color  # Return the color if dropped within the canvas
        return None

    def draw(self, screen):
        if self.is_image:
            screen.blit(self.image, (self.x, self.y))  # Draw the image
        else:
            pygame.draw.rect(screen, self.color, self.rect)  # Draw the color (if not an image)

        # Draw the text if it's set
        if self.text:
            screen.blit(self.text_surface, self.text_rect.topleft)
