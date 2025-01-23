import pygame
import sys
import time
import random

pygame.init()

# Window setup
WIDTH, HEIGHT = 1400, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Code Racer")

# Fonts & Colors
TITLE_FONT = pygame.font.SysFont("None", 50,)
INSTR_FONT = pygame.font.SysFont("None", 32)
FONT = pygame.font.SysFont("None", 25)

# New color palette
RED_BG = (41, 54, 111)  # #29366f
WHITE = (244, 244, 244)  # #f4f4f4
BLACK = (51, 60, 87)  # #333c57
GREEN = (58, 93, 201)  # #3b5dc9
YELLOW = (65, 166, 246)  # #41a6f6
BLUE = (115, 239, 247)  # #73eff7
GRAY = (148, 176, 194)  # #94b0c2


# Game settings
GRID_SIZE = 5
TILE_SIZE = 100
COMMANDS = ["Move Forward", "Turn Left", "Turn Right"]
player_x, player_y = 2, 4
player_dir = "UP"
commands = []
destination = (4, 0)

# Timer and scoring
TIME_LIMIT = 35  # in seconds
timer_start = time.time()
score = 0 
final_score_displayed = False

# Drop Zone
MAX_STEPS = 5  # Number of drop zones
DROP_ZONE_PADDING = 20
drop_zones = [pygame.Rect(DROP_ZONE_PADDING, 250 + i * 70, 250, 50) for i in range(MAX_STEPS)]
 
# Command positions
COMMAND_BLOCK_X = 300
COMMAND_BLOCK_Y = 150
COMMAND_SPACING = 70

# Grid alignment
GRID_PADDING_RIGHT = 40
GRID_OFFSET_X = WIDTH - GRID_PADDING_RIGHT - (GRID_SIZE * TILE_SIZE)
GRID_OFFSET_Y = 200

# Grid layout
grid1 = (
    ("R", "C", "R", "G", "D"),  # Finish line at (0, 4)
    ("R", "G", "R", "R", "C"),
    ("R", "G", "G", "G", "R"),  # Checkpoints at C , Bonus points (4,0), (0,0),(3,4)
    ("C", "R", "R", "G", "R"),
    ("R", "G", "R", "G", "G"),  # Start point at (4, 2)
)

grid2 = (
    ("R", "C", "R", "C", "D"),  # Finish line at (0, 4)
    ("R", "G", "G", "R", "G"),
    ("R", "G", "R", "R", "G"),  # Checkpoints at C , Bonus points (4,3), (0,0),(2,0)
    ("G", "G", "C", "G", "G"),
    ("G", "G", "R", "R", "G"),  # Start point at (4, 2)
)

grid3 = (
    ("R", "G", "G", "R", "D"),  # Finish line at (0, 4)
    ("C", "R", "R", "C", "G"),
    ("R", "G", "G", "R", "R"),  # Checkpoints at C , Bonus points (0,0), (2,4),(3,2)
    ("R", "G", "C", "G", "G"),
    ("R", "R", "R", "G", "G"),  # Start point at (4, 2)
)

grids = [grid1,  grid2, grid3]

# Randomly select a grid
grid = random.choice(grids)

# Run Button
run_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)

# Load and scale car image
CAR_IMAGE = pygame.image.load("CDI-Games-SoftwareDevelopment\\images\\Car_Green_Front.svg")
CAR_IMAGE = pygame.transform.scale(CAR_IMAGE, (TILE_SIZE / 2, TILE_SIZE / 1.2))
CAR_IMAGE = pygame.transform.rotate(CAR_IMAGE, 180)  # Rotate to face RIGHT
FINISHLINE_IMAGE = pygame.image.load("CDI-Games-SoftwareDevelopment\\images\\FinishLine.png")
FINISHLINE_IMAGE = pygame.transform.scale(FINISHLINE_IMAGE, (TILE_SIZE , TILE_SIZE - 1))

GRASS_IMAGE = pygame.image.load("CDI-Games-SoftwareDevelopment\\images\\Lava_CodeRacer.png")
GRASS_IMAGE = pygame.transform.scale(GRASS_IMAGE, (TILE_SIZE, TILE_SIZE - 1))

ROAD_IMAGE = pygame.image.load("CDI-Games-SoftwareDevelopment\\images\\weg_gravel.png")
ROAD_IMAGE = pygame.transform.scale(ROAD_IMAGE, (TILE_SIZE - 3, TILE_SIZE - 3))

TURN_LEFT_ICON = pygame.image.load("CDI-Games-SoftwareDevelopment\\images\\draai_icon.png").convert_alpha()
TURN_LEFT_ICON = pygame.transform.scale(TURN_LEFT_ICON, (30, 30))

TURN_RIGHT_ICON = pygame.transform.flip(TURN_LEFT_ICON, True, False)  # Mirror the image horizontally for "Turn Right"

# Classes for Command Blocks
class CommandBlock:
    def __init__(self, text, x, y, color, icon=None):
        self.text = text
        self.rect = pygame.Rect(x, y, 160, 50)
        self.color = color
        self.icon = icon

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.rect, border_radius=25)
        txt_surf = FONT.render(self.text, True, BLACK)
        txt_rect = txt_surf.get_rect(center=(self.rect.centerx + 20, self.rect.centery))
        SCREEN.blit(txt_surf, txt_rect)

        if self.icon:
            icon_rect = self.icon.get_rect(center=(self.rect.left + 30, self.rect.centery))
            SCREEN.blit(self.icon, icon_rect)


# Create command blocks
command_blocks = [
    CommandBlock("Turn Left", COMMAND_BLOCK_X, COMMAND_BLOCK_Y, GREEN, TURN_LEFT_ICON),
    CommandBlock("Move Forward", COMMAND_BLOCK_X + 200, COMMAND_BLOCK_Y, BLUE),
    CommandBlock("Turn Right", COMMAND_BLOCK_X + 400, COMMAND_BLOCK_Y, YELLOW, TURN_RIGHT_ICON),
]

# Draw grid and elements
def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            tile_type = grid[y][x]
            if tile_type == "D":
                SCREEN.blit(
                    FINISHLINE_IMAGE,
                    (GRID_OFFSET_X + x * TILE_SIZE + 2, GRID_OFFSET_Y + y * TILE_SIZE + 2)
                )
            elif tile_type == "G":
                SCREEN.blit(
                    GRASS_IMAGE,
                    (GRID_OFFSET_X + x * TILE_SIZE + 2, GRID_OFFSET_Y + y * TILE_SIZE + 2)
                )
            else:  # Default road
                SCREEN.blit(
                    ROAD_IMAGE,
                    (GRID_OFFSET_X + x * TILE_SIZE + 2, GRID_OFFSET_Y + y * TILE_SIZE + 2)
                )

def draw_car():
    global player_dir
    car_image = CAR_IMAGE

    if player_dir == "RIGHT":
        car_image = pygame.transform.rotate(CAR_IMAGE, -90)
    elif player_dir == "LEFT":
        car_image = pygame.transform.rotate(CAR_IMAGE, 90)
    elif player_dir == "UP":
        car_image = pygame.transform.rotate(CAR_IMAGE, 0)
    elif player_dir == "DOWN":
        car_image = pygame.transform.rotate(CAR_IMAGE, 180)

    car_rect = car_image.get_rect(center=(
        GRID_OFFSET_X + player_x * TILE_SIZE + TILE_SIZE // 2,
        GRID_OFFSET_Y + player_y * TILE_SIZE + TILE_SIZE // 2,
    ))
    SCREEN.blit(car_image, car_rect)
def draw_car_position(x, y):
    """
    Draws the car at an intermediate position on the grid.
    """
    car_image = CAR_IMAGE
    if player_dir == "RIGHT":
        car_image = pygame.transform.rotate(CAR_IMAGE, -90)
    elif player_dir == "LEFT":
        car_image = pygame.transform.rotate(CAR_IMAGE, 90)
    elif player_dir == "UP":
        car_image = pygame.transform.rotate(CAR_IMAGE, 0)
    elif player_dir == "DOWN":
        car_image = pygame.transform.rotate(CAR_IMAGE, 180)

    car_rect = car_image.get_rect(center=(
        GRID_OFFSET_X + x * TILE_SIZE + TILE_SIZE // 2,
        GRID_OFFSET_Y + y * TILE_SIZE + TILE_SIZE // 2,
    ))
    SCREEN.blit(car_image, car_rect)


def draw_timer():
    # Calculate time left
    elapsed_time = time.time() - timer_start
    time_left = TIME_LIMIT - elapsed_time

    # Timer circle
    timer_x, timer_y = WIDTH - 100, 50
    pygame.draw.circle(SCREEN, YELLOW if time_left > 30 else GREEN, (timer_x, timer_y), 40)
    timer_text = FONT.render(str(max(0, int(time_left))), True, BLACK)
    timer_rect = timer_text.get_rect(center=(timer_x, timer_y))
    SCREEN.blit(timer_text, timer_rect)

    return time_left

def draw_score():
    score_text = FONT.render(f"Score: {score} Press any key to continue", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    SCREEN.blit(score_text, score_rect)

def end_game(time_left):
    global final_score_displayed

    # Calculate bonus points for remaining time
    if time_left >= 10:
        bonus_points = 500
    else:
        bonus_points = int(500 / max(1, time_left))  # Avoid division by zero

    total_score = score + bonus_points

    # Display final score
    if not final_score_displayed:
        SCREEN.fill(BLACK)
        popup_surf = TITLE_FONT.render(f"Final Score: {total_score}", True, WHITE)
        popup_rect = popup_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        SCREEN.blit(popup_surf, popup_rect)

        score_text = FONT.render("Press any key to exit", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        SCREEN.blit(score_text, score_rect)

        pygame.display.flip()

        # Wait for player input
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pygame.quit()
                    sys.exit()



def find_nearest_checkpoint():#Find the nearest checkpoint on the same y-coordinate as the car.
    
    global player_x, player_y
    nearest_checkpoint = (player_x, player_y)

    # Search for checkpoints on the same y-coordinate
    for x in range(GRID_SIZE):
        if grid[player_y][x] == "C":  # Check for checkpoint on the same y-coordinate
            nearest_checkpoint = (x, player_y)
            break  # Stop at the first checkpoint (closest in x-direction)

    return nearest_checkpoint


def move_forward():
    """
    Move the car forward in the current direction with animation.
    """
    global player_x, player_y, score

    # Calculate the target position
    new_x, new_y = player_x, player_y
    if player_dir == "RIGHT" and player_x < GRID_SIZE - 1:
        new_x += 1
    elif player_dir == "LEFT" and player_x > 0:
        new_x -= 1
    elif player_dir == "UP" and player_y > 0:
        new_y -= 1
    elif player_dir == "DOWN" and player_y < GRID_SIZE - 1:
        new_y += 1

    # Animate the movement
    steps = 10
    for step in range(steps):
        intermediate_x = player_x + (new_x - player_x) * (step / steps)
        intermediate_y = player_y + (new_y - player_y) * (step / steps)

        SCREEN.fill(RED_BG)
        draw_grid()
        draw_car_position(intermediate_x, intermediate_y)
        draw_timer()
        draw_drop_zones()
        draw_run_button()
        pygame.display.flip()
        pygame.time.wait(50)  # Adjust for smoother/slower animations

    # Update to the new position
    player_x, player_y = new_x, new_y

    # Check if the car reaches the yellow block (destination)
    if (player_x, player_y) == destination:
        score += 500  # Award points for reaching the destination
        print(f"Score: {int(score)}")
        end_game(0)

  
def turn_left():
    global player_dir
    if player_dir == "RIGHT":
        player_dir = "UP"
    elif player_dir == "UP":
        player_dir = "LEFT"
    elif player_dir == "LEFT":
        player_dir = "DOWN"
    elif player_dir == "DOWN":
        player_dir = "RIGHT"

def turn_right():
    global player_dir
    if player_dir == "RIGHT":
        player_dir = "DOWN"
    elif player_dir == "DOWN":
        player_dir = "LEFT"
    elif player_dir == "LEFT":
        player_dir = "UP"
    elif player_dir == "UP":
        player_dir = "RIGHT"

def draw_drop_zones():
    for i, zone in enumerate(drop_zones):
        pygame.draw.rect(SCREEN, WHITE, zone, border_radius=15)
        pygame.draw.rect(SCREEN, BLACK, zone, 2, border_radius=15)
        step_txt = FONT.render(f"S{i + 1}:  ", True, BLACK)
        step_rect = step_txt.get_rect(midleft=(zone.left + 10, zone.centery))
        SCREEN.blit(step_txt, step_rect)

        if i < len(commands):
            x_button_rect = pygame.Rect(zone.right - 40, zone.top + 10, 30, 30)
            pygame.draw.rect(SCREEN, RED_BG, x_button_rect, border_radius=5)
            x_txt = FONT.render("X", True, WHITE)
            x_txt_rect = x_txt.get_rect(center=x_button_rect.center)
            SCREEN.blit(x_txt, x_txt_rect)

def draw_run_button():
    pygame.draw.rect(SCREEN, WHITE, run_button, border_radius=15)
    pygame.draw.rect(SCREEN, BLACK, run_button, 2, border_radius=15)
    run_txt = FONT.render("RUN", True, BLACK)
    run_rect = run_txt.get_rect(center=run_button.center)
    SCREEN.blit(run_txt, run_rect)

def execute_commands():
    global player_x, player_y
    for cmd in commands:
        pygame.time.wait(100)
        if cmd == "Move Forward":
            move_forward()
        elif cmd == "Turn Left":
            turn_left()
        elif cmd == "Turn Right":
            turn_right()
        draw_grid()
        draw_car()
        pygame.display.update()
        pygame.time.wait(100)
    commands.clear()

def handle_mouse_click(pos):
    global commands

    for block in command_blocks:
        if block.rect.collidepoint(pos):
            if len(commands) < MAX_STEPS:
                commands.append(block.text)

    for i, zone in enumerate(drop_zones):
        if i < len(commands):
            x_button_rect = pygame.Rect(zone.right - 40, zone.top + 10, 30, 30)
            if x_button_rect.collidepoint(pos):
                commands.pop(i)
                break

def main():
    global commands, score
    clock = pygame.time.Clock()
    running = True

    while running:
        SCREEN.fill(RED_BG)

        title_surf = TITLE_FONT.render("Code Racer", True, WHITE)
        SCREEN.blit(title_surf, (50, 10))
        instr_surf = INSTR_FONT.render("Click commands to add them to the sequence!", True, WHITE)
        SCREEN.blit(instr_surf, (50, 60))

        for block in command_blocks:
            block.draw()

        draw_drop_zones()
        for i, cmd in enumerate(commands):
            cmd_txt = FONT.render(cmd, True, BLACK)
            cmd_rect = cmd_txt.get_rect(center=drop_zones[i].center)
            SCREEN.blit(cmd_txt, cmd_rect)

        draw_grid()
        draw_car()
        draw_run_button()
        draw_timer()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(f"Score: {int(score)}")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if run_button.collidepoint(event.pos):
                    execute_commands()
                else:
                    handle_mouse_click(event.pos)

        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    main()
