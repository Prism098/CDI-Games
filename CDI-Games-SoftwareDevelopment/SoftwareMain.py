import pygame
import sys
import time
from pygame.locals import * 

pygame.init()

# Window setup
WIDTH, HEIGHT = 1400, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Code Racer")

# Fonts & Colors
TITLE_FONT = pygame.font.SysFont("Arial", 48, bold=True)
INSTR_FONT = pygame.font.SysFont("Arial", 32)
FONT = pygame.font.SysFont("Arial", 24)

RED_BG = (194, 0, 48)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (135, 211, 124)
YELLOW = (255, 255, 0)
BLUE = (93, 173, 226)
GRAY = (51, 60, 87)

# Game settings
GRID_SIZE = 5
TILE_SIZE = 100
COMMANDS = ["Move Forward", "Turn Left", "Turn Right"]
player_x, player_y = 0, 4
player_dir = "RIGHT"
commands = []
destination = (4, 0)

# Timer and scoring
TIME_LIMIT = 60  # in seconds
timer_start = time.time()
score = 0
final_score_displayed = False

# Drop Zone
MAX_STEPS = 5  # Number of drop zones
DROP_ZONE_PADDING = 20
drop_zones = [pygame.Rect(DROP_ZONE_PADDING, 250 + i * 70, 250, 50) for i in range(MAX_STEPS)]

# Command positions
COMMAND_BLOCK_X = 300
COMMAND_BLOCK_Y = 50
COMMAND_SPACING = 70

# Grid alignment
GRID_PADDING_RIGHT = 40
GRID_OFFSET_X = WIDTH - GRID_PADDING_RIGHT - (GRID_SIZE * TILE_SIZE)
GRID_OFFSET_Y = 200

# Grid layout
grid = [
    ["R", "R", "R", "R", "D"],
    ["G", "G", "G", "R", "G"],
    ["G", "G", "G", "R", "G"],
    ["G", "G", "C", "R", "G"],
    ["R", "C", "R", "R", "C"],
]

# Run Button
run_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)

# Load and scale car image
CAR_IMAGE = pygame.image.load("CDI-Games-SoftwareDevelopment\\images\\Car_Green_Front.svg")
CAR_IMAGE = pygame.transform.scale(CAR_IMAGE, (TILE_SIZE - 5, TILE_SIZE - 1))
CAR_IMAGE = pygame.transform.rotate(CAR_IMAGE, 180)  # Rotate to face RIGHT

FINISHLINE_IMAGE = pygame.image.load("CDI-Games-SoftwareDevelopment\\images\\FinishLine.svg")
FINISHLINE_IMAGE = pygame.transform.scale(FINISHLINE_IMAGE, (TILE_SIZE - 5, TILE_SIZE - 1))

GRASS_IMAGE = pygame.image.load("CDI-Games-SoftwareDevelopment\\images\\gras.svg")
GRASS_IMAGE = pygame.transform.scale(GRASS_IMAGE, (TILE_SIZE - 5, TILE_SIZE - 1))

ROAD_TOPLEFT_IMAGE = pygame.image.load("CDI-Games-SoftwareDevelopment\\images\\weg_links_boven.svg")
ROAD_TOPLEFT_IMAGE = pygame.transform.scale(ROAD_TOPLEFT_IMAGE, (TILE_SIZE - 5, TILE_SIZE - 1))

ROAD_BOTTOMLEFT_IMAGE = pygame.image.load("CDI-Games-SoftwareDevelopment\\images\\weg_links_onder.svg")
ROAD_BOTTOMLEFT_IMAGE = pygame.transform.scale(ROAD_BOTTOMLEFT_IMAGE, (TILE_SIZE - 5, TILE_SIZE - 1))

ROAD_STRAIGHT_IMAGE = pygame.image.load("CDI-Games-SoftwareDevelopment\\images\\weg_normaal.svg")
ROAD_STRAIGHT_IMAGE = pygame.transform.scale(ROAD_STRAIGHT_IMAGE, (TILE_SIZE - 5, TILE_SIZE - 1))

ROAD_TOPRIGHT_IMAGE = pygame.image.load("CDI-Games-SoftwareDevelopment\\images\\weg_rechts_boven.svg")
ROAD_TOPRIGHT_IMAGE = pygame.transform.scale(ROAD_TOPRIGHT_IMAGE, (TILE_SIZE - 5, TILE_SIZE - 1))

ROAD_BOTTOMRIGHT_IMAGE = pygame.image.load("CDI-Games-SoftwareDevelopment\\images\\weg_rechts_onder.svg")
ROAD_BOTTOMRIGHT_IMAGE = pygame.transform.scale(ROAD_BOTTOMRIGHT_IMAGE, (TILE_SIZE - 5, TILE_SIZE - 1))

FLAG_IMAGE = pygame.image.load("CDI-Games-SoftwareDevelopment\\images\\vlag.svg") #Does not get recognized, not sure why
FLAG_IMAGE = pygame.transform.scale(FLAG_IMAGE, (TILE_SIZE - 5, TILE_SIZE - 1))


# Classes for Command Blocks
class CommandBlock:
    def __init__(self, text, x, y, color):
        self.text = text
        self.rect = pygame.Rect(x, y, 150, 50)
        self.color = color

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.rect, border_radius=25)
        txt_surf = FONT.render(self.text, True, BLACK)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        SCREEN.blit(txt_surf, txt_rect)

# Create command blocks
command_blocks = [
    CommandBlock("Move Forward", COMMAND_BLOCK_X, COMMAND_BLOCK_Y, GREEN),
    CommandBlock("Turn Left", COMMAND_BLOCK_X, COMMAND_BLOCK_Y + COMMAND_SPACING, BLUE),
    CommandBlock("Turn Right", COMMAND_BLOCK_X, COMMAND_BLOCK_Y + 2 * COMMAND_SPACING, YELLOW),
]

# Draw grid and elements
def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            tile_type = grid[y][x]
            color = GRAY if tile_type == "R" else WHITE
            if tile_type == "D":
                color = YELLOW
            elif tile_type == "C":
                SCREEN.blit(
                    GRASS_IMAGE,
                    (GRID_OFFSET_X + x * TILE_SIZE + 2, GRID_OFFSET_Y + y * TILE_SIZE + 2)
                )
               
            rect = pygame.Rect(
                GRID_OFFSET_X + x * TILE_SIZE,
                GRID_OFFSET_Y + y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE,
            )
            pygame.draw.rect(SCREEN, color, rect)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)

            # If the tile is "D", draw the finish line image
            if tile_type == "D":
                SCREEN.blit(
                    FINISHLINE_IMAGE,
                    (GRID_OFFSET_X + x * TILE_SIZE + 2, GRID_OFFSET_Y + y * TILE_SIZE + 2)
                )
            elif tile_type == "C":
                SCREEN.blit(
                    FLAG_IMAGE,
                    (GRID_OFFSET_X + x * TILE_SIZE + 2, GRID_OFFSET_Y + y * TILE_SIZE + 2)
                )
            elif tile_type == "G":
                SCREEN.blit(
                    GRASS_IMAGE,
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
def wait():
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN: # return on any key pressed
                return
            
def draw_timer():
    # Calculate time left
    elapsed_time = time.time() - timer_start
    time_left = TIME_LIMIT - elapsed_time

    # Timer circle
    timer_x, timer_y = WIDTH - 100, 50
    pygame.draw.circle(SCREEN, YELLOW if time_left > 30 else RED_BG, (timer_x, timer_y), 40)
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

    # Show the final score at the bottom of the screen for 10 seconds
    if not final_score_displayed:
        draw_score()
        pygame.display.flip()
        final_score_displayed = True
        wait()
        pygame.quit()
        sys.exit()


def move_forward():
    global player_x, player_y, score
    if player_dir == "RIGHT" and player_x < GRID_SIZE - 1:
        player_x += 1
    elif player_dir == "LEFT" and player_x > 0:
        player_x -= 1
    elif player_dir == "UP" and player_y > 0:
        player_y -= 1
    elif player_dir == "DOWN" and player_y < GRID_SIZE - 1:
        player_y += 1

    # Check if the car reaches the yellow block (destination)
    if (player_x, player_y) == destination:
        score += 100  # Award points for reaching the destination
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

        clock.tick(30)


if __name__ == "__main__":
    main()
