import pygame

class DraggableUIElement:
    def __init__(self, x, y, width, height, color_or_image, text=None, font=None, font_name=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color_or_image = color_or_image
        self.text = text
        self.font = font
        self.font_name = font_name
        
        # Store the initial position
        self.initial_x = x
        self.initial_y = y
        
        if isinstance(self.color_or_image, tuple):
            self.is_image = False
            self.color = self.color_or_image
        elif self.color_or_image is not None:
            self.is_image = True
            self.image = pygame.image.load(self.color_or_image)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        else:
            self.is_image = False
            self.color = None

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.dragging = False

    def reset_position(self):
        """Reset the element to its initial position"""
        self.x = self.initial_x
        self.y = self.initial_y
        self.rect.topleft = (self.x, self.y)

    def handle_event(self, event, canvas_rect):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                return None
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Update position while dragging
                mouse_x, mouse_y = event.pos
                self.x = mouse_x - self.width // 2
                self.y = mouse_y - self.height // 2
                self.rect.topleft = (self.x, self.y)
                return None
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                if canvas_rect.colliderect(self.rect):
                    if self.is_image:
                        return self.color_or_image  # Return image path
                    elif self.color:
                        return self.color  # Return color tuple
                    elif self.font_name:
                        return self.font_name  # Return font name
                self.reset_position()
        return None

    def draw(self, screen):
        if self.is_image:
            screen.blit(self.image, (self.x, self.y))
        elif self.color:
            pygame.draw.rect(screen, self.color, self.rect)
        
        if self.text:
            text_surface = self.font.render(self.text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect.topleft)