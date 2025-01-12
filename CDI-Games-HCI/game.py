import pygame
from persona import Persona
from ui_element import UIElement

# Initialize pygame and font system
pygame.init()
pygame.font.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 800

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 98, 40)
GREY = (150, 150, 150)
BROWN = (77, 55, 50)
RED = (255, 0, 0)

# Fonts
FONT = pygame.font.SysFont("arial", 24)


class GameState:
    def __init__(self):
        # Game state initialization
        # Game state initialization
        self.stage = "colors"
        self.font_size = 20
        self.font_name = "arial"  # Store the font name here
        self.font = pygame.font.SysFont(self.font_name, self.font_size)
        self.header_font = pygame.font.SysFont(self.font_name, 40)

        # Flags to track the score conditions (if they have been earned once)
        self.color_condition_met = False  # Initialize this flag
        self.sticker_condition_met = False  # Initialize this flag
        self.font_condition_met = False  # Initialize this flag

        self.persona = Persona(
            "CDI-Games-HCI/assets/Childpersona.png",
            (75, 250),
            "Design een passend interface \n voor de persoon in de onderstaande foto:",
        )

        # UI Elements
        self.ui_elements = [
            UIElement(540, 650, 125, 125, color=ORANGE),
            UIElement(770, 650, 125, 125, color=GREY),
            UIElement(990, 650, 125, 125, color=BROWN),
        ]

        # Stickers UI Elements
        self.ui_stickers = [
            UIElement(540, 640, 100, 150, image_path="CDI-Games-HCI/assets/CartoonHappy.png"),
            UIElement(770, 650, 125, 125, image_path="CDI-Games-HCI/assets/CartoonBored.png"),
            UIElement(990, 640, 100, 150, image_path="CDI-Games-HCI/assets/CartoonSad.png"),
        ]

        # Font UI Elements
        self.font_elements = [
            UIElement(
                500,
                650,
                125,
                125,
                text="Aa",
                font=pygame.font.SysFont("timesnewroman", 50),
                font_name="timesnewroman",
            ),
            UIElement(
                762,
                650,
                125,
                125,
                text="Aa",
                font=pygame.font.SysFont("comicsansms", 50),
                font_name="comicsansms",
            ),
            UIElement(
                1025,
                650,
                125,
                125,
                text="Aa",
                font=pygame.font.SysFont("couriernew", 50),
                font_name="couriernew",
            ),
        ]

        # Additional elements
        self.grey_square = pygame.Rect(500, 10, 650, 600)
        self.grey_color = (200, 200, 200)
        self.placed_elements = []
        self.score = 0

        self.header_text = "Webinterface"
        self.description_text = (
            "Het leven is een prachtige reis, gevuld met momenten van vreugde, ontdekking en groei. "
            "Elke nieuwe dag biedt kansen om te glimlachen, te leren en verbinding te maken met anderen. "
            "Koester de eenvoudige momenten — een warme zonsopgang, het lachen met vrienden of de stille rust van de natuur. "
            "Dit zijn de ware vreugden van het leven."
        )

        self.photo_rect = pygame.Rect(
            self.grey_square.centerx - 150, self.grey_square.top + 340, 300, 200
        )

        self.sticker_placed = False

        # Timer settings
        self.total_time = 20  # Total time in seconds
        self.time_left = self.total_time
        self.timer_bar_width = WIDTH
        self.timer_bar_height = 10
        self.timer_bar_color = RED

        # Score window settings
        self.show_score_window = False

    def draw(self, screen):
        # Draw background and main elements
        screen.fill(WHITE)
        pygame.draw.rect(screen, self.grey_color, self.grey_square)

        # Highlight the grey square if an element is being dragged
        if self.is_any_element_dragging():
            pygame.draw.rect(screen, (0, 255, 0), self.grey_square, 5)

        # Stage-based label and element drawing
        label_text = ""
        if self.stage == "colors":
            label_text = "Kleur"
            for element in self.ui_elements:
                element.draw(screen, self.show_score_window)

            # Add instructional text for the "colors" stage
            self.draw_instructions(
                screen,
                "Sleep de objecten \n naar het grijze gebied! ",
                x=WIDTH // 3,
                y=HEIGHT - 100,
            )
        elif self.stage == "sticker":
            label_text = "Sticker"
            for sticker in self.ui_stickers:
                sticker.draw(screen, self.show_score_window)
        elif self.stage == "fonts" and not self.show_score_window:
            label_text = "Lettertype"
            for font_element in self.font_elements:
                font_element.draw(screen, self.show_score_window)

        # Draw header and description
        header_surface = self.header_font.render(self.header_text, True, BLACK)
        header_rect = header_surface.get_rect(
            center=(self.grey_square.centerx, self.grey_square.top + 50)
        )
        screen.blit(header_surface, header_rect)

        self.wrap_text(
            self.description_text,
            screen,
            self.grey_square.left + 10,
            self.grey_square.top + 100,
            self.grey_square.width - 20,
            self.font,
        )

        # Draw the persona image
        self.persona.draw(screen)

        # Draw timer bar
        timer_bar_current_width = int(
            (self.time_left / self.total_time) * self.timer_bar_width
        )
        pygame.draw.rect(
            screen,
            self.timer_bar_color,
            (0, 0, timer_bar_current_width, self.timer_bar_height),
        )

        # Draw label below the grey square
        if label_text:
            label_surface = FONT.render(label_text, True, BLACK)
            label_rect = label_surface.get_rect(
                center=(self.grey_square.centerx, self.grey_square.bottom + 20)
            )
            screen.blit(label_surface, label_rect)

        # Draw photo placeholder or placed sticker
        if not self.sticker_placed:
            pygame.draw.rect(screen, GREY, self.photo_rect)
            photo_text = FONT.render("Foto hier", True, BLACK)
            photo_text_rect = photo_text.get_rect(center=self.photo_rect.center)
            screen.blit(photo_text, photo_text_rect)
        else:
            for sticker in self.ui_stickers:
                if sticker.placed:
                    sticker.draw(screen, self.show_score_window)

    def draw_instructions(self, screen, text, x, y):
        """Draw multi-line instructional text at the given position."""
        instruction_font = pygame.font.SysFont("arial", 17)
        lines = text.split("\n")  # Split the text into multiple lines

        line_height = (
            instruction_font.get_height() + 5
        )  # Add some spacing between lines
        for i, line in enumerate(lines):
            instruction_surface = instruction_font.render(line, True, BLACK)
            instruction_rect = instruction_surface.get_rect(
                center=(x, y + i * line_height)
            )
            screen.blit(instruction_surface, instruction_rect)

    def wrap_text(self, text, screen, x, y, width, font):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            test_surface = font.render(test_line, True, BLACK)
            if test_surface.get_width() <= width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "

        if current_line:
            lines.append(current_line)

        line_height = font.get_height() + 5
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, BLACK)
            text_rect = text_surface.get_rect(topleft=(x, y + i * line_height))
            text_rect.centerx = x + width // 2
            screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if self.show_score_window:
            return

        elements = (
            self.ui_elements
            if self.stage == "colors"
            else self.ui_stickers if self.stage == "sticker" else self.font_elements
        )

        for element in elements:
            element.handle_event(event)

        if event.type == pygame.MOUSEBUTTONUP:
            for element in elements:
                if self.grey_square.colliderect(element.rect) and element.visible:
                    if self.stage == "colors" and element.color:
                        self.grey_color = element.color
                        self.stage = "sticker"
                        return

                    if self.stage == "sticker" and self.grey_square.colliderect(
                        element.rect
                    ):
                        # Automatically place the sticker in the "Foto hier" area
                        scaled_width = int(element.original_width * 2)
                        scaled_height = int(element.original_height * 2)

                        element.rect = pygame.Rect(
                            self.photo_rect.centerx - scaled_width // 2,
                            self.photo_rect.centery - scaled_height // 2,
                            scaled_width,
                            scaled_height,
                        )
                        element.image = pygame.transform.scale(
                            element.original_image, (scaled_width, scaled_height)
                        )
                        element.draggable = False
                        element.placed = True
                        self.sticker_placed = True
                        self.stage = "fonts"
                        return

                    if self.stage == "fonts" and element.font_name:
                        # Update the font and set the flag for scoring
                        self.update_description_and_header_font(element.font_name)
                        self.font_name = element.font_name  # Set the selected font name
                        self.font_condition_met = (
                            False  # Reset condition for next selection
                        )
                        self.show_score_window = True
                        return

    def update_description_and_header_font(self, font_name):
        self.font = pygame.font.SysFont(font_name, self.font_size)
        self.header_font = pygame.font.SysFont(font_name, 40)

    def is_any_element_dragging(self):
        elements = (
            self.ui_elements
            if self.stage == "colors"
            else self.ui_stickers if self.stage == "sticker" else self.font_elements
        )
        return any(element.is_dragging() for element in elements)

    def update_timer(self, dt):
        if not self.show_score_window:
            self.time_left -= dt
            if self.time_left <= 0:
                self.time_left = 0
                self.show_score_window = True
                print("Time's up!")