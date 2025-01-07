import pygame
import os


pygame.init()
pygame.font.init()
# Colors
BLACK = (0, 0, 0)

class UIElement:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        image_path=None,
        color=None,
        text="",
        font=None,
        font_name=None,
        draggable=True,
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.original_width = width
        self.original_height = height
        self.color = color
        self.image = None
        self.text = text
        self.font = font
        self.font_name = font_name
        self.dragging = False
        self.draggable = draggable
        self.original_pos = (x, y)
        self.visible = True
        self.hovered = False
        self.scale_factor = 2
        self.scale_speed = 0.1
        self.placed = False
        self.offset_x = 0
        self.offset_y = 0

        if image_path and os.path.isfile(image_path):
            try:
                self.image = pygame.image.load(image_path).convert_alpha()
                self.original_image = self.image  # Store the original image
                self.image = pygame.transform.scale(self.image, (width, height))
            except pygame.error as e:
                print(f"Error loading image: {e}")

    def draw(self, screen, show_score_window):
        if self.visible:
            mouse_pos = pygame.mouse.get_pos()
            self.hovered = self.rect.collidepoint(mouse_pos) and not show_score_window

            if self.placed:
                # When placed, draw at full photo_rect size without scaling effects
                if self.image:
                    scaled_image = pygame.transform.scale(
                        self.original_image, (self.rect.width, self.rect.height)
                    )
                    screen.blit(scaled_image, self.rect)
            else:
                # Normal drawing behavior for unplaced elements
                if self.hovered:
                    self.scale_factor = min(self.scale_factor + self.scale_speed, 1.2)
                else:
                    self.scale_factor = max(self.scale_factor - self.scale_speed, 1)

                scaled_width = int(self.original_width * self.scale_factor)
                scaled_height = int(self.original_height * self.scale_factor)

                scaled_rect = pygame.Rect(
                    self.rect.centerx - scaled_width // 2,
                    self.rect.centery - scaled_height // 2,
                    scaled_width,
                    scaled_height,
                )

                if self.image:
                    scaled_image = pygame.transform.scale(
                        self.original_image, (scaled_width, scaled_height)
                    )
                    screen.blit(scaled_image, scaled_rect.topleft)
                elif self.color:
                    pygame.draw.rect(screen, self.color, scaled_rect)

                if self.text and self.font:
                    text_surface = self.font.render(self.text, True, BLACK)
                    text_width = int(text_surface.get_width() * self.scale_factor)
                    text_height = int(text_surface.get_height() * self.scale_factor)
                    text_surface = pygame.transform.scale(
                        text_surface, (text_width, text_height)
                    )
                    text_rect = text_surface.get_rect(center=scaled_rect.center)
                    screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if not self.visible or not self.draggable:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.rect.collidepoint(event.pos):
                    self.dragging = True
                    mouse_x, mouse_y = event.pos
                    self.offset_x = self.rect.x - mouse_x
                    self.offset_y = self.rect.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x + self.offset_x
                self.rect.y = mouse_y + self.offset_y

    def reset_position(self):
        self.rect.topleft = self.original_pos

    def is_dragging(self):
        return self.dragging