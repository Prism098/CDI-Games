#game screen 
import pygame
import time
import sys
from utils.styles import WIDTH, HEIGHT, RED_BG, WHITE, BLACK, GREEN, YELLOW, BLUE, SCREEN, FONT, screen ,TITLE_FONT

# Game settings
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Code Racer")
GRID_SIZE = 5
TILE_SIZE = 100
COMMANDS = ["Move Forward", "Turn Left", "Turn Right"]
player_x, player_y = 2, 4
player_dir = "UP"
commands = []
destination = (0, 2)

# Global variables
command_blocks = []  # Initialize as an empty list


# Timer and scoring
TIME_LIMIT = 35  # in seconds
timer_start = time.time()
score = 0

# Drop Zone
MAX_STEPS = 10
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
grid = [
    ["R", "R", "R", "R", "R"],
    ["R", "G", "G", "R", "G"],
    ["D", "G", "G", "R", "G"],
    ["G", "G", "C", "R", "G"],
    ["R", "C", "R", "R", "C"],
]
# Run Button
run_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)


# Classes for Command Blocks
class CommandBlock:
    def __init__(self, text, x, y, color, icon=None):
        self.text = text
        self.rect = pygame.Rect(x, y, 160, 50)
        self.color = color
        self.icon = icon

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=25)
        txt_surf = pygame.font.SysFont(None, 25).render(self.text, True, BLACK)
        txt_rect = txt_surf.get_rect(center=(self.rect.centerx + 20, self.rect.centery))
        screen.blit(txt_surf, txt_rect)
        if self.icon:
            icon_rect = self.icon.get_rect(center=(self.rect.left + 30, self.rect.centery))
            screen.blit(self.icon, icon_rect)
    


# Draw grid and elements
def draw_grid(screen):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[y][x] == "D":
                screen.blit(
                    FINISHLINE_IMAGE,
                    (GRID_OFFSET_X + x * TILE_SIZE + 2, GRID_OFFSET_Y + y * TILE_SIZE + 2),
                )
            elif grid[y][x] == "G":
                screen.blit(
                    GRASS_IMAGE,
                    (GRID_OFFSET_X + x * TILE_SIZE + 2, GRID_OFFSET_Y + y * TILE_SIZE + 2),
                )
            else:
                screen.blit(
                    ROAD_IMAGE,
                    (GRID_OFFSET_X + x * TILE_SIZE + 2, GRID_OFFSET_Y + y * TILE_SIZE + 2),
                )

def draw_car(screen):
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
    screen.blit(car_image, car_rect)

def draw_car_position(x, y):
    """
    Draws the car at an intermediate position.
    """
    car_rect = pygame.Rect(
        GRID_OFFSET_X + x * TILE_SIZE + TILE_SIZE // 2,
        GRID_OFFSET_Y + y * TILE_SIZE + TILE_SIZE // 2,
        TILE_SIZE // 2,
        TILE_SIZE // 2,
    )
    pygame.draw.rect(SCREEN, GREEN, car_rect)


def draw_timer(screen):
    elapsed_time = time.time() - timer_start
    time_left = max(0, TIME_LIMIT - elapsed_time)
    timer_text = pygame.font.SysFont(None, 50).render(f"Time: {int(time_left)}", True, WHITE)
    screen.blit(timer_text, (WIDTH - 200, 20))
    return time_left

def draw_drop_zones(screen):
    for i, zone in enumerate(drop_zones):
        pygame.draw.rect(screen, WHITE, zone, border_radius=15)
        pygame.draw.rect(screen, BLACK, zone, 2, border_radius=15)

        if i < len(commands):
            command_text = FONT.render(commands[i], True, BLACK)
            SCREEN.blit(command_text, (zone.x + 10, zone.y + 10))
            x_button = pygame.Rect(zone.right - 40, zone.y + 10, 30, 30)
            pygame.draw.rect(screen, RED_BG, x_button, border_radius=5)
            x_text = FONT.render("X", True, WHITE)
            SCREEN.blit(x_text, (x_button.x + 10, x_button.y))


def draw_run_button(screen):
    pygame.draw.rect(screen, WHITE, run_button, border_radius=15)
    pygame.draw.rect(screen, BLACK, run_button, 2, border_radius=15)
    run_txt = pygame.font.SysFont(None, 25).render("RUN", True, BLACK)
    run_rect = run_txt.get_rect(center=run_button.center)
    screen.blit(run_txt, run_rect)

def find_nearest_checkpoint():#Find the nearest checkpoint on the same y-coordinate as the car.
    
    global player_x, player_y
    nearest_checkpoint = (player_x, player_y)

    # Search for checkpoints on the same y-coordinate
    for x in range(GRID_SIZE):
        if grid[player_y][x] == "C":  # Check for checkpoint on the same y-coordinate
            nearest_checkpoint = (x, player_y)
            break  # Stop at the first checkpoint (closest in x-direction)

    return nearest_checkpoint

def end_game():
    """
    Handles the end of the game by displaying the final score and waiting for user input.
    """
    SCREEN.fill(BLACK)
    final_score = FONT.render(f"Final Score: {score}", True, WHITE)
    exit_message = FONT.render("Press any key to exit", True, WHITE)
    SCREEN.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2 - 50))
    SCREEN.blit(exit_message, (WIDTH // 2 - exit_message.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False

    pygame.quit()
    sys.exit()
def move_forward():
    """
    Move the car forward in the current direction with smooth animation.
    """
    global player_x, player_y, score

    # Target position
    new_x, new_y = player_x, player_y
    if player_dir == "UP" and player_y > 0:
        new_y -= 1
    elif player_dir == "DOWN" and player_y < GRID_SIZE - 1:
        new_y += 1
    elif player_dir == "LEFT" and player_x > 0:
        new_x -= 1
    elif player_dir == "RIGHT" and player_x < GRID_SIZE - 1:
        new_x += 1

    # Smooth animation
    steps = 10
    for step in range(steps):
        intermediate_x = player_x + (new_x - player_x) * (step / steps)
        intermediate_y = player_y + (new_y - player_y) * (step / steps)
        SCREEN.fill(RED_BG)
        draw_grid(SCREEN)
        draw_car_position(intermediate_x, intermediate_y)
        draw_drop_zones(SCREEN)
        pygame.display.flip()
        pygame.time.wait(50)

    # Update to the new position
    player_x, player_y = new_x, new_y

    # Check if the car reaches the destination
    if (player_x, player_y) == destination:
        score += 500
        scoreboard("Player", "email@example.com", score)


  
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

def execute_commands():
    global player_x, player_y
    for cmd in commands:
        if cmd == "Move Forward":
            move_forward()
        elif cmd == "Turn Left":
            turn_left()
        elif cmd == "Turn Right":
            turn_right()
        draw_grid(SCREEN)
        draw_car(SCREEN)
        pygame.display.update()
        time.sleep(0.5)
    commands.clear()

def handle_mouse_click(pos):
    global commands

    for i, zone in enumerate(drop_zones):
        if i < len(commands):
            x_button = pygame.Rect(zone.right - 40, zone.y + 10, 30, 30)
            if x_button.collidepoint(pos):
                commands.pop(i)
                return


def show_feedback(message, color):
    """
    Displays a feedback message on the screen for a brief duration.
    """
    feedback = FONT.render(message, True, WHITE)
    feedback_rect = feedback.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(SCREEN, color, feedback_rect.inflate(20, 20), border_radius=10)
    SCREEN.blit(feedback, feedback_rect)
    pygame.display.flip()
    time.sleep(1)

def start_screen():
    input_box_username = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 50)
    input_box_email = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 50)
    username, email = "", ""

    active_box = None  # To track which input box is active

    while True:
        SCREEN.fill(RED_BG)
        title_text = TITLE_FONT.render("Enter Your Details", True, WHITE)
        SCREEN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        # Draw input boxes
        pygame.draw.rect(SCREEN, WHITE, input_box_username, border_radius=10)
        pygame.draw.rect(SCREEN, WHITE, input_box_email, border_radius=10)
        username_text = FONT.render(username, True, BLACK)
        email_text = FONT.render(email, True, BLACK)
        SCREEN.blit(username_text, (input_box_username.x + 10, input_box_username.y + 10))
        SCREEN.blit(email_text, (input_box_email.x + 10, input_box_email.y + 10))

        instructions = FONT.render("Press Enter to Start", True, WHITE)
        SCREEN.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT - 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_username.collidepoint(event.pos):
                    active_box = "username"
                elif input_box_email.collidepoint(event.pos):
                    active_box = "email"
                else:
                    active_box = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username and email:
                    return username, email
                elif event.key == pygame.K_BACKSPACE:
                    if active_box == "username":
                        username = username[:-1]
                    elif active_box == "email":
                        email = email[:-1]
                else:
                    if active_box == "username":
                        username += event.unicode
                    elif active_box == "email":
                        email += event.unicode
def scoreboard(username, email, score):
    """
    Displays the scoreboard with the username, email, and final score.
    """
    while True:
        SCREEN.fill(BLACK)
        title_text = TITLE_FONT.render("Scoreboard", True, WHITE)
        SCREEN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        username_text = FONT.render(f"Username: {username}", True, WHITE)
        email_text = FONT.render(f"Email: {email}", True, WHITE)
        score_text = FONT.render(f"Final Score: {score}", True, WHITE)

        SCREEN.blit(username_text, (WIDTH // 2 - username_text.get_width() // 2, HEIGHT // 2 - 50))
        SCREEN.blit(email_text, (WIDTH // 2 - email_text.get_width() // 2, HEIGHT // 2))
        SCREEN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()


def start_game():
    global CAR_IMAGE, FINISHLINE_IMAGE, GRASS_IMAGE, ROAD_IMAGE, TURN_LEFT_ICON, TURN_RIGHT_ICON, command_blocks

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Code Racer")

    # Load and initialize images after pygame.display initialization
    CAR_IMAGE = pygame.image.load("CDI-Games-SoftwareDevelopment/images/Car_Green_Front.svg")
    CAR_IMAGE = pygame.transform.scale(CAR_IMAGE, (TILE_SIZE // 2, TILE_SIZE // 1.2))
    CAR_IMAGE = pygame.transform.rotate(CAR_IMAGE, 180)

    FINISHLINE_IMAGE = pygame.image.load("CDI-Games-SoftwareDevelopment/images/FinishLine.svg")
    FINISHLINE_IMAGE = pygame.transform.scale(FINISHLINE_IMAGE, (TILE_SIZE - 5, TILE_SIZE - 1))

    GRASS_IMAGE = pygame.image.load("CDI-Games-SoftwareDevelopment/images/gras.svg")
    GRASS_IMAGE = pygame.transform.scale(GRASS_IMAGE, (TILE_SIZE, TILE_SIZE - 1))

    ROAD_IMAGE = pygame.image.load("CDI-Games-SoftwareDevelopment/images/weg_normaal.jpg")
    ROAD_IMAGE = pygame.transform.scale(ROAD_IMAGE, (TILE_SIZE, TILE_SIZE - 1))

    TURN_LEFT_ICON = pygame.image.load("CDI-Games-SoftwareDevelopment/images/draai_icon.png").convert_alpha()
    TURN_LEFT_ICON = pygame.transform.scale(TURN_LEFT_ICON, (30, 30))
    TURN_RIGHT_ICON = pygame.transform.flip(TURN_LEFT_ICON, True, False)

    # Initialize command blocks globally
    command_blocks = [
        CommandBlock("Turn Left", COMMAND_BLOCK_X, COMMAND_BLOCK_Y, GREEN, TURN_LEFT_ICON),
        CommandBlock("Move Forward", COMMAND_BLOCK_X + 200, COMMAND_BLOCK_Y, BLUE),
        CommandBlock("Turn Right", COMMAND_BLOCK_X + 400, COMMAND_BLOCK_Y, YELLOW, TURN_RIGHT_ICON),
    ]

    # Game loop
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(RED_BG)

        draw_grid(screen)
        draw_car(screen)
        draw_timer(screen)
        draw_drop_zones(screen)
        draw_run_button(screen)

        for block in command_blocks:
            block.draw(screen)

        for i, cmd in enumerate(commands):
            cmd_txt = pygame.font.SysFont(None, 25).render(cmd, True, BLACK)
            cmd_rect = cmd_txt.get_rect(center=drop_zones[i].center)
            screen.blit(cmd_txt, cmd_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if run_button.collidepoint(event.pos):
                    execute_commands()
                else:
                    handle_mouse_click(event.pos)

        clock.tick(30)

    pygame.quit()

    
