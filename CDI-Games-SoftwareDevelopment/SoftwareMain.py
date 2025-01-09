import pygame
import sys
import random
import time

pygame.init()

# Window setup
WIDTH, HEIGHT = 1400, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boolean Bakery")

# Fonts & Colors
TITLE_FONT = pygame.font.SysFont("Arial", 48, bold=True)
INSTR_FONT = pygame.font.SysFont("Arial", 32)
FONT = pygame.font.SysFont("Arial", 24)
SMALL_FONT = pygame.font.SysFont("Arial", 20)

# Color palette based on mockups
RED_BG = (194, 0, 48)   # Background red
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (242, 159, 93)
GREEN = (135, 211, 124)
RED = (235, 106, 106)
LIGHT_GREY = (230, 230, 230)

# Game constants
STEPS = [
    "Pak alle tools & ingrediënten",
    "Vul de bakblik met bakmix",
    "Mix de Ingrediënten",
    "Bak de cake"
]
CORRECT_ORDER = STEPS[:]  # The correct order is as defined above
TIME_LIMIT = 60  # 60 seconds to solve
POINTS_PER_CORRECT = 10

class Button:
    def __init__(self, x, y, text, width=120, height=50):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surf):
        # Draw a white rounded button
        pygame.draw.rect(surf, WHITE, self.rect, border_radius=25)
        txt_surf = FONT.render(self.text, True, BLACK)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surf.blit(txt_surf, txt_rect)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

class DraggableStep:
    def __init__(self, text, x, y, width=300, height=50):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.correct = False
        self.checked = False

    def draw(self, surf):
        # White pill-shaped rectangle with black text
        color = WHITE if not self.checked else (GREEN if self.correct else RED)
        pygame.draw.rect(surf, color, self.rect, border_radius=25)
        txt_surf = FONT.render(self.text, True, BLACK if color == WHITE else WHITE)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surf.blit(txt_surf, txt_rect)

        # If checked, draw symbol next to it
        if self.checked:
            symbol = "✓" if self.correct else "✗"
            sym_color = WHITE if not self.correct else BLACK
            sym_surf = FONT.render(symbol, True, sym_color)
            sym_rect = sym_surf.get_rect(midleft=(self.rect.right + 10, self.rect.centery))
            surf.blit(sym_surf, sym_rect)

class Slot:
    def __init__(self, x, y, width=300, height=50, index=1):
        self.rect = pygame.Rect(x, y, width, height)
        self.filled_by = None
        self.index = index

    def draw(self, surf):
        # Show a circle with the index on the left and white rectangle slot to the right
        circle_radius = 25
        circle_center = (self.rect.left - 60, self.rect.centery)
        
        # Draw circle with index
        pygame.draw.circle(surf, WHITE, circle_center, circle_radius)
        num_surf = FONT.render(str(self.index), True, BLACK)
        num_rect = num_surf.get_rect(center=circle_center)
        surf.blit(num_surf, num_rect)

        # Draw the slot as a white pill-shaped rectangle
        pygame.draw.rect(surf, WHITE, self.rect, border_radius=25)


def main():
    # Shuffle steps on the left side
    puzzle_steps = STEPS[:]
    random.shuffle(puzzle_steps)

    # Create draggable steps
    # Left column: steps at x=100, y starting at 150
    step_y = 200
    draggable_steps = []
    for step in puzzle_steps:
        ds = DraggableStep(step, 100, step_y)
        draggable_steps.append(ds)
        step_y += 90

    # Create slots on the right side
    slot_start_y = 200
    slots = []
    for i in range(len(CORRECT_ORDER)):
        s = Slot(WIDTH - 400, slot_start_y, index=i+1)
        slots.append(s)
        slot_start_y += 90

    check_button = Button(WIDTH - 200, HEIGHT - 100, "Check!")
    start_time = time.time()
    solved = False
    score = 0
    dragged_step = None

    running = True

    while running:
        dt = pygame.time.Clock().tick(60) / 1000.0
        # Time left
        elapsed = time.time() - start_time
        time_left = TIME_LIMIT - elapsed
        if time_left <= 0 and not solved:
            # Time's up, force check
            for slot in slots:
                if slot.filled_by:
                    slot.filled_by.checked = True
                    slot.filled_by.correct = (slot.filled_by.text == CORRECT_ORDER[slot.index-1])
            score = sum(POINTS_PER_CORRECT for slot in slots if slot.filled_by and slot.filled_by.correct)
            solved = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if not solved:
                    for ds in draggable_steps:
                        if ds.rect.collidepoint(pos):
                            dragged_step = ds
                            ds.dragging = True
                            ds.offset_x = ds.rect.x - pos[0]
                            ds.offset_y = ds.rect.y - pos[1]
                            break
                # Check button
                if check_button.clicked(pos) and not solved:
                    for slot in slots:
                        if slot.filled_by:
                            slot.filled_by.checked = True
                            correct_text = CORRECT_ORDER[slot.index-1]
                            slot.filled_by.correct = (slot.filled_by.text == correct_text)
                    correct_count = sum(1 for s in slots if s.filled_by and s.filled_by.correct)
                    score = correct_count * POINTS_PER_CORRECT
                    if correct_count == len(CORRECT_ORDER):
                        score += int(time_left)  # time bonus if all correct
                    solved = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if dragged_step:
                    # Snap to slot if overlapping
                    placed = False
                    for slot in slots:
                        if slot.rect.colliderect(dragged_step.rect):
                            # If slot empty, place here
                            if slot.filled_by is None:
                                slot.filled_by = dragged_step
                                dragged_step.rect.topleft = slot.rect.topleft
                                placed = True
                            # If filled, leave as is
                    dragged_step.dragging = False
                    dragged_step = None

            elif event.type == pygame.MOUSEMOTION:
                if dragged_step and dragged_step.dragging:
                    mx, my = event.pos
                    dragged_step.rect.x = mx + dragged_step.offset_x
                    dragged_step.rect.y = my + dragged_step.offset_y

        # Draw background
        SCREEN.fill(RED_BG)

        # Draw title (white pill at top center)
        title_w = 300
        title_h = 60
        title_rect = pygame.Rect(WIDTH//2 - title_w//2, 50, title_w, title_h)
        pygame.draw.rect(SCREEN, WHITE, title_rect, border_radius=30)
        title_surf = SMALL_FONT.render("Boolean Bakery", True, BLACK)
        title_txt_rect = title_surf.get_rect(center=title_rect.center)
        SCREEN.blit(title_surf, title_txt_rect)

        # Instructions if not solved:
        if not solved:
            instr_surf = INSTR_FONT.render("Let's break down baking a cake", True, WHITE)
            SCREEN.blit(instr_surf, (WIDTH//2 - instr_surf.get_width()//2, 120))
            # Another line of instruction could be:
            add_instr_surf = FONT.render("Sleep de stappen in de juiste volgorde en klik op 'Check!'", True, WHITE)
            SCREEN.blit(add_instr_surf, (WIDTH//2 - add_instr_surf.get_width()//2, 160))

        # Draw slots
        for slot in slots:
            slot.draw(SCREEN)
            
        # Draw steps
        if dragged_step:
            # Draw all steps except the one currently dragged
            for ds in draggable_steps:
                if ds != dragged_step:
                    ds.draw(SCREEN)
            # Draw the dragged step last so it appears on top
            dragged_step.draw(SCREEN)
        else:
            # If no step is being dragged, just draw them normally
            for ds in draggable_steps:
                ds.draw(SCREEN)

        # Draw button if not solved
        if not solved:
            check_button.draw(SCREEN)

        # Draw timer (top right) as a simple white circle with remaining time
        timer_x = WIDTH - 100
        timer_y = 50
        pygame.draw.circle(SCREEN, WHITE, (timer_x, timer_y), 40)
        time_txt = str(int(time_left)) if time_left > 0 else "0"
        time_surf = FONT.render(time_txt, True, BLACK)
        time_rect = time_surf.get_rect(center=(timer_x, timer_y))
        SCREEN.blit(time_surf, time_rect)

        # If solved, show score feedback
        if solved:
            result_surf = FONT.render(f"Score: {score}", True, WHITE)
            SCREEN.blit(result_surf, (WIDTH//2 - result_surf.get_width()//2, HEIGHT - 140))

            correct_count = sum(1 for s in slots if s.filled_by and s.filled_by.correct)
            if correct_count == len(CORRECT_ORDER):
                msg = "Goed gedaan! Alle stappen zijn correct!"
            else:
                msg = "Niet alle stappen zijn correct, probeer het opnieuw!"
            msg_surf = FONT.render(msg, True, WHITE)
            SCREEN.blit(msg_surf, (WIDTH//2 - msg_surf.get_width()//2, HEIGHT - 100))

        pygame.display.flip()

    # Print final score
    print(f"Score: {score}")

if __name__ == "__main__":
    main()
