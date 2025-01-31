import pygame

class DraggableUIElement:
    def __init__(self, x, y, width, height, color_or_image, text=None, font=None, font_name=None, text_color=(255, 255, 255)) :
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color_or_image = color_or_image
        self.text = text
        self.font = font
        self.font_name = font_name
        self.text_color = text_color 
        
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
        self.hovering = False  # Track hover state

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
            if self.rect.collidepoint(event.pos):
                self.hovering = True  # Set hovering to True when the mouse is over the element
            else:
                self.hovering = False  # Set hovering to False when the mouse moves away

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
        # Apply hover effect (e.g., scale up the element)
        scale_factor = 1.2 if self.hovering else 1  # Increase size on hover

        scaled_width = int(self.width * scale_factor)
        scaled_height = int(self.height * scale_factor)
        scaled_x = self.x - (scaled_width - self.width) // 2
        scaled_y = self.y - (scaled_height - self.height) // 2

        if self.is_image:
            scaled_image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
            screen.blit(scaled_image, (scaled_x, scaled_y))
        elif self.color:
            pygame.draw.rect(screen, self.color, pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height))
        
        if self.text:
            # Use self.text_color instead of hardcoded (0, 0, 0)
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=(scaled_x + scaled_width // 2, scaled_y + scaled_height // 2))
            screen.blit(text_surface, text_rect.topleft)
