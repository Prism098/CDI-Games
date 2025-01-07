import pygame
import sys
import json
import os
import time

pygame.init()

# Basic Config
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boolean Theater")
FONT = pygame.font.SysFont("Arial", 24)

CLOCK = pygame.time.Clock()

# Paths for assets
BG_IMAGE = pygame.image.load("images/stage_bg.jpg")
CURTAIN_IMAGE = pygame.image.load("images/curtain.jpg")
BUTTON_IMAGE = pygame.image.load("images/button.png")
BOX_IMAGES = {
    "AND": pygame.image.load("images/box_and.png"),
    "OR": pygame.image.load("images/box_or.png"),
    "NOT": pygame.image.load("images/box_not.png"),
    "DUMMY": pygame.image.load("images/box_dummy.png")
}

CLICK_SOUND = pygame.mixer.Sound("sounds/click.wav")
COMPLETE_SOUND = pygame.mixer.Sound("sounds/complete.wav")
ERROR_SOUND = pygame.mixer.Sound("sounds/error.wav")

# Simple data storage
SCORES_FILE = "scores.json"
if not os.path.exists(SCORES_FILE):
    with open(SCORES_FILE, "w") as f:
        json.dump([], f)

# Global game parameters
TOTAL_TIME = 300  # 5 minutes total for all levels
LIVES = 3
NUM_LEVELS = 5

# Example level data
# Each level: correct_sequence = ["AND", "OR", "NOT", ...]
# available_boxes (mix of correct + dummy)
LEVELS = [
    {"correct": ["AND", "OR"], "extra": ["NOT", "DUMMY"]},
    {"correct": ["OR", "AND", "NOT"], "extra": ["DUMMY", "DUMMY"]},
    {"correct": ["AND", "AND", "OR"], "extra": ["NOT", "DUMMY"]},
    {"correct": ["NOT", "OR", "OR", "AND"], "extra": ["DUMMY", "DUMMY"]},
    {"correct": ["AND", "NOT", "AND", "OR"], "extra": ["DUMMY", "DUMMY", "DUMMY"]}
]

class Button:
    def __init__(self, x, y, text):
        self.image = BUTTON_IMAGE
        self.rect = self.image.get_rect(topleft=(x,y))
        self.text = text
    
    def draw(self, surf):
        surf.blit(self.image, self.rect)
        txt_surf = FONT.render(self.text, True, (0,0,0))
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surf.blit(txt_surf, txt_rect)
    
    def clicked(self, pos):
        return self.rect.collidepoint(pos)

class Box:
    def __init__(self, box_type, x, y):
        self.type = box_type
        self.image = BOX_IMAGES[box_type]
        self.rect = self.image.get_rect(topleft=(x,y))
        self.dragging = False

    def draw(self, surf):
        surf.blit(self.image, self.rect)

class Slot:
    def __init__(self, x, y, width=80, height=80):
        self.rect = pygame.Rect(x,y,width,height)
        self.filled = None

    def draw(self, surf):
        pygame.draw.rect(surf, (200,200,200), self.rect, 2)
        if self.filled:
            self.filled.draw(surf)

def load_scores():
    with open(SCORES_FILE, "r") as f:
        return json.load(f)

def save_score(name, email, score):
    scores = load_scores()
    scores.append({"name": name, "email": email, "score": score})
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]  # top 10
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f)

def main_menu():
    start_btn = Button(WIDTH//2 - 60, HEIGHT//2 - 30, "Start")
    leaderboard_btn = Button(WIDTH//2 - 100, HEIGHT//2 + 50, "Leaderboard")
    exit_btn = Button(WIDTH//2 - 50, HEIGHT//2 + 130, "Exit")

    running = True
    while running:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if start_btn.clicked(pos):
                    return "play"
                if leaderboard_btn.clicked(pos):
                    return "leaderboard"
                if exit_btn.clicked(pos):
                    pygame.quit()
                    sys.exit()

        SCREEN.blit(BG_IMAGE, (0,0))
        # Title
        title_surf = FONT.render("Boolean Theater", True, (255,255,255))
        SCREEN.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 100))

        start_btn.draw(SCREEN)
        leaderboard_btn.draw(SCREEN)
        exit_btn.draw(SCREEN)

        pygame.display.flip()

def leaderboard_screen():
    back_btn = Button(WIDTH//2 - 40, HEIGHT - 80, "Back")
    scores = load_scores()

    running = True
    while running:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.clicked(event.pos):
                    return "menu"

        SCREEN.blit(BG_IMAGE, (0,0))
        title_surf = FONT.render("Leaderboard", True, (255,255,255))
        SCREEN.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 50))

        y_off = 120
        for i, entry in enumerate(scores):
            score_str = f"{i+1}. {entry['name']} - {entry['score']} ({entry['email']})"
            score_surf = FONT.render(score_str, True, (255,255,255))
            SCREEN.blit(score_surf, (WIDTH//2 - score_surf.get_width()//2, y_off))
            y_off += 40

        back_btn.draw(SCREEN)
        pygame.display.flip()

def input_player_data(final_score):
    # Simple text input for name and email
    name = ""
    email = ""
    mode = "name"  # first ask name, then email
    done_btn = Button(WIDTH//2 - 40, HEIGHT//2 + 100, "Done")

    active_color = (255,255,255)
    inactive_color = (200,200,200)

    running = True
    while running:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if mode == "name":
                    if event.key == pygame.K_RETURN:
                        mode = "email"
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode
                else:
                    if event.key == pygame.K_RETURN:
                        # finalize
                        pass
                    elif event.key == pygame.K_BACKSPACE:
                        email = email[:-1]
                    else:
                        email += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if done_btn.clicked(pos) and name and email:
                    save_score(name, email, final_score)
                    return "menu"

        SCREEN.fill((0,0,0))
        prompt_surf = FONT.render("Enter your details", True, (255,255,255))
        SCREEN.blit(prompt_surf, (WIDTH//2 - prompt_surf.get_width()//2, 100))

        name_label = FONT.render("Name:", True, (255,255,255))
        SCREEN.blit(name_label, (WIDTH//2 - 150, HEIGHT//2 - 60))
        email_label = FONT.render("Email:", True, (255,255,255))
        SCREEN.blit(email_label, (WIDTH//2 - 150, HEIGHT//2))

        pygame.draw.rect(SCREEN, active_color if mode=="name" else inactive_color, (WIDTH//2 - 50, HEIGHT//2 - 60, 200, 30), 2)
        pygame.draw.rect(SCREEN, active_color if mode=="email" else inactive_color, (WIDTH//2 - 50, HEIGHT//2, 200, 30), 2)

        name_surf = FONT.render(name, True, (255,255,255))
        SCREEN.blit(name_surf, (WIDTH//2 - 45, HEIGHT//2 - 55))
        email_surf = FONT.render(email, True, (255,255,255))
        SCREEN.blit(email_surf, (WIDTH//2 - 45, HEIGHT//2 + 5))

        done_btn.draw(SCREEN)
        pygame.display.flip()

def play_game():
    # Global game parameters
    time_left = TOTAL_TIME
    lives = LIVES
    current_level = 0
    score = 0

    running = True
    start_time = time.time()

    while running:
        if current_level >= NUM_LEVELS:
            # Completed all levels
            final_score = score + int(time_left) * 10
            return input_player_data(final_score)

        # Setup current level
        level_data = LEVELS[current_level]
        correct_seq = level_data["correct"]
        extra_seq = level_data["extra"]

        puzzle_boxes = correct_seq + extra_seq
        import random
        random.shuffle(puzzle_boxes)

        # Prepare draggable boxes on left side
        boxes = []
        start_x = 50
        start_y = 150
        for b_type in puzzle_boxes:
            box = Box(b_type, start_x, start_y)
            boxes.append(box)
            start_y += 90  # stack vertically

        # Prepare slots on right side
        slots = []
        slot_start_x = WIDTH - 350
        slot_start_y = 150
        for _ in correct_seq:
            slot = Slot(slot_start_x, slot_start_y)
            slots.append(slot)
            slot_start_y += 90

        # A simple curtain animation state (fake)
        show_curtains = True
        curtain_pos = 0
        curtain_speed = 20  # just a dummy animation

        level_done = False
        submitted = False
        # Track dragging
        dragged_box = None
        offset_x, offset_y = 0, 0

        while not level_done:
            dt = CLOCK.tick(60) / 1000.0
            time_passed = time.time() - start_time
            time_left = TOTAL_TIME - time_passed
            if time_left <= 0:
                # Time out - game over
                return input_player_data(score)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    # Check if clicking a box
                    for box in boxes:
                        if box.rect.collidepoint(pos):
                            dragged_box = box
                            offset_x = box.rect.x - pos[0]
                            offset_y = box.rect.y - pos[1]
                            box.dragging = True
                            CLICK_SOUND.play()
                            break
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if dragged_box:
                        # Try to place in slot if overlapping
                        placed = False
                        for slot in slots:
                            if slot.rect.colliderect(dragged_box.rect):
                                # Place the box in this slot
                                if slot.filled is None:
                                    slot.filled = dragged_box
                                    dragged_box.rect.topleft = slot.rect.topleft
                                    placed = True
                                else:
                                    # Slot already filled - swap?
                                    # For simplicity, just revert
                                    pass
                        if not placed:
                            # Put it back to left side start area if not placed
                            # Or leave it where released
                            pass

                        dragged_box.dragging = False
                        dragged_box = None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Submit answer and check correctness
                        # Extract filled sequence
                        filled_sequence = []
                        for slot in slots:
                            if slot.filled:
                                filled_sequence.append(slot.filled.type)
                            else:
                                filled_sequence.append(None)
                        
                        if None in filled_sequence:
                            # Not all filled
                            ERROR_SOUND.play()
                        else:
                            # Compare to correct_seq
                            correct_count = 0
                            for c, f in zip(correct_seq, filled_sequence):
                                if c == f:
                                    correct_count += 1
                            if correct_count == len(correct_seq):
                                # All correct
                                COMPLETE_SOUND.play()
                                # Increase score: basic formula
                                level_score = 100 * len(correct_seq)
                                score += level_score
                                current_level += 1
                                level_done = True
                            else:
                                # Some incorrect
                                ERROR_SOUND.play()
                                lives -= 1
                                if lives <= 0:
                                    # Game over
                                    final_score = score
                                    return input_player_data(final_score)
                                # Highlight incorrect ones: For simplicity, just print to console
                                # (You would visually show red/green here.)
                                # Reset level or let them try again?
                                # Let's let them rearrange again.
                                submitted = True

            # Update positions if dragging
            if dragged_box and dragged_box.dragging:
                mx, my = pygame.mouse.get_pos()
                dragged_box.rect.x = mx + offset_x
                dragged_box.rect.y = my + offset_y

            # Draw scene
            SCREEN.blit(BG_IMAGE, (0,0))
            
            # Curtains (not a real animation, just a placeholder)
            # Imagine curtains open at start of level
            if show_curtains:
                curtain_pos += curtain_speed
                if curtain_pos > WIDTH//2:
                    show_curtains = False
                # left curtain
                SCREEN.blit(CURTAIN_IMAGE, (0 - (WIDTH//2 - curtain_pos), 0))
                # right curtain
                SCREEN.blit(CURTAIN_IMAGE, (WIDTH - curtain_pos, 0))

            # Draw HUD
            hud_text = f"Level: {current_level+1}/{NUM_LEVELS} | Time: {int(time_left)}s | Lives: {lives} | Score: {score}"
            hud_surf = FONT.render(hud_text, True, (255,255,255))
            SCREEN.blit(hud_surf, (10,10))

            # Draw boxes
            for box in boxes:
                # Draw only if not placed in a slot
                # If a box is placed in slot, slot will draw it
                in_slot = False
                for slot in slots:
                    if slot.filled == box:
                        in_slot = True
                        break
                if not in_slot:
                    box.draw(SCREEN)

            # Draw slots
            for slot in slots:
                slot.draw(SCREEN)

            # Instructions
            instr_surf = FONT.render("Arrange boxes and press ENTER to submit.", True, (255,255,255))
            SCREEN.blit(instr_surf, (10,50))

            pygame.display.flip()

def main():
    state = "menu"
    while True:
        if state == "menu":
            state = main_menu()
        elif state == "play":
            state = play_game()
        elif state == "leaderboard":
            state = leaderboard_screen()
        elif state == "exit":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
