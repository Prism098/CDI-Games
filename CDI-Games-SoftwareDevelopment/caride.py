import pygame
import sys
import random
import time
# Import show_menu function
from screens.menu_screen import show_menu

from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH, SCREEN_HEIGHT = 1920 , 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)


pygame.display.set_caption("CAR I.D.E")


#old trash code 

WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


# Colors
# Fonts & Colors
FONT = pygame.font.SysFont(None, 25)
TITLE_FONT = pygame.font.SysFont("None", 50,)
INSTR_FONT = pygame.font.SysFont("None", 32)
FONT = pygame.font.SysFont("None", 25)

WHITE = (244, 244, 244)
BLACK = (51, 60, 87)
GREEN = (58, 93, 201)
RED = (255, 0, 0)
YELLOW = (65, 166, 246)
BLUE = (41, 54, 111)
BORDER_COLOR = (26, 28, 44)  # #1a1c2c

# Load images
background = pygame.image.load("CDI-Games-SoftwareDevelopment\images\Software Dev\caride_dropzone.png")
turn_left_img = pygame.image.load("CDI-Games-SoftwareDevelopment\images\Software Dev\caride_turn_left.png")
move_forward_img = pygame.image.load("CDI-Games-SoftwareDevelopment\images\Software Dev\caride_Forward.png")
turn_right_img = pygame.image.load("CDI-Games-SoftwareDevelopment\images\Software Dev\caride_turn_right.png")
run_button_img = pygame.image.load("CDI-Games-SoftwareDevelopment\images\Software Dev\Run button.png")
# Load "Memory Full" image
memory_full_img = pygame.image.load("CDI-Games-SoftwareDevelopment\\images\\Car Memory FULL HIT RUN !.png")

# move image down to add timer on screen 
image_top_padding = 50
image_right_padding = 5

# Scale images to desired sizes
turn_left_img = pygame.transform.scale(turn_left_img, (120, 125))
move_forward_img = pygame.transform.scale(move_forward_img, (120, 125))
turn_right_img = pygame.transform.scale(turn_right_img, (120, 125))
run_button_img = pygame.transform.scale(run_button_img, (245, 68))
background = pygame.transform.scale(background, (561, 903))


# Positions for the UI elements
background_pos = (50, 50)
turn_left_pos = (680 + image_right_padding, 75 + image_top_padding)
move_forward_pos = (860+ image_right_padding, 75 + image_top_padding)
turn_right_pos = (1040+ image_right_padding, 75 + image_top_padding)
run_button_pos = (1220+ image_right_padding, 100 + image_top_padding)

# Define Rects for clickable areas
turn_left_rect = pygame.Rect(turn_left_pos[0], turn_left_pos[1], 120, 125)
move_forward_rect = pygame.Rect(move_forward_pos[0], move_forward_pos[1], 120, 125)
turn_right_rect = pygame.Rect(turn_right_pos[0], turn_right_pos[1], 120, 125)
run_button_rect = pygame.Rect(run_button_pos[0], run_button_pos[1], 245, 68)

# Game settings
GRID_SIZE = 5
TILE_SIZE = 110
COMMANDS = ["Move Forward", "Turn Left", "Turn Right"]
player_x, player_y = 2, 4
player_dir = "UP"
commands = []
destination = (4, 0)  # Fixed destination to new grids

# Timer and scoring
TIME_LIMIT = 60  # in seconds
timer_start = time.time()
score = 0
final_score_displayed = False
is_animation_complete = True  # Default to True, meaning no animation is in progress


# Background grid details
grid_rows, grid_cols = 3, 5
background_width, background_height = 530, 320
square_width = background_width / grid_cols
square_height = background_height / grid_rows

# Starting position of the background
grid_start_x, grid_start_y = (50,200)

# Drop Zone
MAX_STEPS = 15  # Number of drop zones
DROP_ZONE_PADDING = 140
drop_zones = [pygame.Rect(DROP_ZONE_PADDING, 250 + i * 70, 250, 50) for i in range(MAX_STEPS)]
memory_full = False  # Flag to track if memory is full

# Grid alignment
GRID_PADDING_RIGHT = 0
GRID_OFFSET_X = 1250 - GRID_PADDING_RIGHT - (GRID_SIZE * TILE_SIZE)
GRID_OFFSET_Y = 390

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

grids = [grid1, grid2, grid3]

# Randomly select a grid
grid = random.choice(grids)

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

# List to store placed commands and their positions
placed_commands = []
memory_popup_start_time = None
popup_duration = 2000  # Display for 3 seconds (3000 ms)


# Add command to grid
def add_command_to_grid(command_image):
    global memory_full, memory_popup_start_time

    if len(placed_commands) >= grid_rows * grid_cols:
        memory_full = True
        memory_popup_start_time = pygame.time.get_ticks()  # Record popup start time
        return

    # Scale the image down by 10%
    scaled_image = pygame.transform.scale(
        command_image,
        (int(square_width * 0.7), int(square_height * 0.7))
    )

    # Determine position in the grid
    grid_index = len(placed_commands)
    row = grid_index // grid_cols
    col = grid_index % grid_cols
    x = grid_start_x + col * square_width + (square_width - scaled_image.get_width()) // 2
    y = grid_start_y + row * (square_height + DROP_ZONE_PADDING) + (square_height - scaled_image.get_height()) // 2

    placed_commands.append((scaled_image, (x, y)))
    if len(placed_commands) >= 14:
        memory_full = True
        memory_popup_start_time = pygame.time.get_ticks()  # Record popup start time
        return


# Draw commands in the grid
def draw_placed_commands():
    for command_image, position in placed_commands:
        screen.blit(command_image, position)


# Draw grid and elements
def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            tile_type = grid[y][x]
            if tile_type == "D":
                screen.blit(
                    FINISHLINE_IMAGE,
                    (GRID_OFFSET_X + x * TILE_SIZE + 2, GRID_OFFSET_Y + y * TILE_SIZE + 2)
                )
            elif tile_type == "G":
                screen.blit(
                    GRASS_IMAGE,
                    (GRID_OFFSET_X + x * TILE_SIZE + 2, GRID_OFFSET_Y + y * TILE_SIZE + 2)
                )
            else:  # Default road
                screen.blit(
                    ROAD_IMAGE,
                    (GRID_OFFSET_X + x * TILE_SIZE + 2, GRID_OFFSET_Y + y * TILE_SIZE + 2)
                )

    # Draw border around the grid
    border_rect = pygame.Rect(GRID_OFFSET_X - 10, GRID_OFFSET_Y - 10, GRID_SIZE * TILE_SIZE + 20, GRID_SIZE * TILE_SIZE + 20)
    pygame.draw.rect(screen, BORDER_COLOR, border_rect, 10)

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
    screen.blit(car_image, car_rect)

def wait():
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:  # return on any key pressed
                return

def draw_timer(screen):
    """
    Draw the countdown timer on the screen.
    """
    elapsed_time = time.time() - timer_start
    time_left = max(0, TIME_LIMIT - elapsed_time)  # Ensure non-negative time
    timer_text = pygame.font.SysFont(None, 150).render(f"Time: {int(time_left)}", True, WHITE)
    
    # Position the timer visibly on the screen
    screen.blit(timer_text, ( 1300, 20))  # Top-left corner
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
        bonus_points = int(500-(500 / max(1, time_left)))  # Avoid division by zero

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


def find_nearest_checkpoint():  # Find the nearest checkpoint on the same y-coordinate as the car.

    global player_x, player_y
    nearest_checkpoint = (player_x, player_y)

    # Search for checkpoints on the same y-coordinate
    for x in range(GRID_SIZE):
        if grid[player_y][x] == "C":  # Check for checkpoint on the same y-coordinate
            nearest_checkpoint = (x, player_y)
            break  # Stop at the first checkpoint (closest in x-direction)

    return nearest_checkpoint

def show_feedback(message, color):
    """
    Display feedback on the center of the screen with a colored background.
    """
    feedback_surface = FONT.render(message, True, WHITE)
    feedback_rect = feedback_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    # Draw a colored rectangle behind the text
    pygame.draw.rect(screen, color, feedback_rect.inflate(20, 10))
    screen.blit(feedback_surface, feedback_rect)
    pygame.display.update()
    pygame.time.wait(1500)  # Pause to show feedback

def move_forward():
    global player_x, player_y, score, is_animation_complete

    # Prevent movement if animation is still running
    if not is_animation_complete:
        return

    is_animation_complete = False  # Set flag to False while animating

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

    # Check the tile type BEFORE animation
    if grid[new_y][new_x] == "G":  # Grass
        show_feedback("Sensors Detect Lava...", RED)
        player_x, player_y = find_nearest_checkpoint()
        is_animation_complete = True  # Allow further actions
        return

    # Animate the car movement
    steps = 5  # Number of steps for smooth animation
    start_x = GRID_OFFSET_X + player_x * TILE_SIZE + TILE_SIZE // 2
    start_y = GRID_OFFSET_Y + player_y * TILE_SIZE + TILE_SIZE // 2
    end_x = GRID_OFFSET_X + new_x * TILE_SIZE + TILE_SIZE // 2
    end_y = GRID_OFFSET_Y + new_y * TILE_SIZE + TILE_SIZE // 2

    for step in range(steps + 1):
        interpolated_x = start_x + (end_x - start_x) * (step / steps)
        interpolated_y = start_y + (end_y - start_y) * (step / steps)

        # Redraw the screen
        screen.fill(BLUE)
        screen.blit(background, background_pos)
        draw_grid()
        draw_placed_commands()
        draw_timer(screen)
        draw_run_button()
        draw_drop_zones()
        draw_car_at_position(interpolated_x, interpolated_y)
        pygame.display.update()
        pygame.time.wait(10)  # Adjust animation speed

    # Update car's position
    player_x, player_y = new_x, new_y

    # Handle tile type AFTER animation completes
    if grid[new_y][new_x] == "C":  # Checkpoint
        score += 500
        show_feedback("Checkpoint! +500 points", GREEN)
    elif grid[new_y][new_x] == "D":  # Finish line
        score += 500
        show_feedback("Destination Reached! +500 points", YELLOW)
        is_animation_complete = True  # Allow game to end after animation
        end_game(max(0, TIME_LIMIT - (time.time() - timer_start)))
        return

    # Allow next movement after animation finishes
    is_animation_complete = True



def draw_car_at_position(x, y):
    """
    Draw the car at a specific interpolated position.
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

    car_rect = car_image.get_rect(center=(x, y))
    screen.blit(car_image, car_rect)



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


#######################################adjust #############################

def draw_drop_zones():
    DROP_ROWS, DROP_COLS = 3, 5  # Drop zone layout
    
    drop_zones = [
    pygame.Rect(
        DROP_ZONE_PADDING + (i % DROP_COLS) * 160,  # Horizontal position
        250 + (i // DROP_COLS) * (50 + 200),       # Vertical position with padding
        150, 50                                    # Width and height of the drop zone
    )
    for i in range(DROP_ROWS * DROP_COLS)
]

def draw_run_button():
    screen.blit(run_button_img, run_button_rect)


def execute_commands():
    global player_x, player_y, memory_full

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

    # Clear commands and reset the memory full flag
    commands.clear()
    placed_commands.clear()
    memory_full = False



def handle_mouse_click(pos):
    global commands

    if turn_left_rect.collidepoint(pos) and len(commands) < MAX_STEPS:
        commands.append("Turn Left")
        add_command_to_grid(turn_left_img)
    elif move_forward_rect.collidepoint(pos) and len(commands) < MAX_STEPS:
        commands.append("Move Forward")
        add_command_to_grid(move_forward_img)
    elif turn_right_rect.collidepoint(pos) and len(commands) < MAX_STEPS:
        commands.append("Turn Right")
        add_command_to_grid(turn_right_img)

    # Check if the run button image was clicked
    if run_button_rect.collidepoint(pos):
        execute_commands()


# Main Game Logic
def main():
    # Show the menu screen
    menu_action = show_menu()

    if menu_action == "quit":
        pygame.quit()
        sys.exit()  # Exit the program if the player chooses to quit

    # Start the game
    running = True
    while running:
        time_left = max(0, TIME_LIMIT - (time.time() - timer_start))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_click(event.pos)

        # End game if time runs out
        if time_left <= 0:
            end_game(time_left)

        # Draw elements
        screen.fill(BLUE)
        screen.blit(background, background_pos)
        draw_placed_commands()  # Draw scaled-down commands in the grid
        screen.blit(turn_left_img, turn_left_pos)
        screen.blit(move_forward_img, move_forward_pos)
        screen.blit(turn_right_img, turn_right_pos)
        draw_timer(screen)
        draw_run_button()
        draw_drop_zones()
        draw_grid()
        draw_car()

        # Display the memory full popup if the flag is set
        if memory_full:
            popup_x = grid_start_x + (background_width - memory_full_img.get_width()) // 2
            popup_y = grid_start_y + (background_height - memory_full_img.get_height()) // 2
            screen.blit(memory_full_img, (popup_x, popup_y))

        # Update the display
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
