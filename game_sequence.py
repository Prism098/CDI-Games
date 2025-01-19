import os
import subprocess
import pygame
import time
import ctypes

# Initialize the pygame window
pygame.init()
window = pygame.display.set_mode((1400, 800))  # Create a single window
pygame.display.set_caption("Main Window for Pygames")

# Get the SDL window ID
window_id = pygame.display.get_wm_info()["window"]

# Launch multiple pygame applications in sequence
games = [ "CDI-Games-SecurityCloud/SecurityMain.py"]  # List of your game scripts

def run_event_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

for game in games:
    print(f"Launching {game}...")
    # Set SDL_WINDOWID environment variable for the child process
    os.environ["SDL_WINDOWID"] = str(window_id)
    print("SDL_WINDOWID:", os.environ.get("SDL_WINDOWID"))


    # Run the game as a separate process
    process = subprocess.Popen(["python", game])
    
    # Keep the parent window responsive while waiting for the child process
    while process.poll() is None:  # While the child process is running
        run_event_loop()
        time.sleep(0.01)  # Prevent high CPU usage
    
    # Optionally, add a delay between games
    time.sleep(2)

pygame.quit()