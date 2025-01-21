import pygame
import subprocess
import sys
import os
import requests

# Stel de werkmap in
script_dir = os.path.dirname(os.path.abspath(__file__))
user_data_path = os.path.join(script_dir, "user_data.json")

# MongoDB server configuratie
SERVER_URL = "http://localhost:4000"

# Lijst van games met absolute paden
games = [
    {"name": "Data Cleaning Game", "script": os.path.join(script_dir, "CDI-Games-DataEngineering", "DataMain.py")},
    {"name": "Website Interface Builder Game", "script": os.path.join(script_dir, "CDI-Games-HCI", "HCIMain.py")},
    {"name": "Network Invaders", "script": os.path.join(script_dir, "CDI-Games-SecurityCloud", "SecurityMain.py")},
    {"name": "Boolean Bakery", "script": os.path.join(script_dir, "CDI-Games-SoftwareDevelopment", "SoftwareMain.py")}
]

# Functie om een game te starten
def run_game(game):
    try:
        print(f"Starting {game['name']}...")
        result = subprocess.run(
            [sys.executable, game["script"]],
            capture_output=True,
            text=True,
            timeout=300
        )
        print(result.stdout)
        for line in result.stdout.splitlines():
            if "Score:" in line:
                return int(line.split(":")[1].strip())
    except Exception as e:
        print(f"Error running {game['name']}: {e}")
    return 0

# Pygame setup
pygame.init()

# Scherminstellingen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Game")
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 64)
label_font = pygame.font.Font(None, 28)

# Kleuren
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (173, 216, 230)

# Status
state = "login"  # Mogelijke staten: login, running, finished
total_score = 0
first_name, last_name, email = "", "", ""

# Inputvelden
input_boxes = [
    pygame.Rect(250, 200, 300, 40),  # Voornaam
    pygame.Rect(250, 260, 300, 40),  # Achternaam
    pygame.Rect(250, 320, 300, 40),  # E-mail
]
active_box = 0
input_text = ["", "", ""]

# Knoppen
submit_button = pygame.Rect(300, 400, 200, 50)

# Functies voor gebruikersgegevens
def save_user_data(first_name, last_name, email):
    data = {
        "name": f"{first_name} {last_name}",
        "email": email,
        "status": "active",
        "totalScore": 0
    }
    try:
        response = requests.post(f"{SERVER_URL}/save", json=data)
        if response.status_code == 201:
            print("Gebruikersgegevens succesvol opgeslagen in MongoDB.")
        else:
            print(f"Fout bij opslaan in MongoDB: {response.text}")
    except Exception as e:
        print(f"Kan geen verbinding maken met de server: {e}")

def update_total_score(total_score):
    try:
        response = requests.post(f"{SERVER_URL}/add-score", json={"totalScore": total_score})
        if response.status_code == 200:
            print("Totaalscore succesvol toegevoegd aan de database.")
        else:
            print(f"Fout bij toevoegen van totaalscore: {response.text}")
    except Exception as e:
        print(f"Kan geen verbinding maken met de server: {e}")

# Hoofdloop
running = True
while running:
    screen.fill(LIGHT_BLUE if state == "login" else WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "login":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if submit_button.collidepoint(event.pos):
                    first_name, last_name, email = input_text
                    if first_name and last_name and email:
                        save_user_data(first_name, last_name, email)
                        state = "running"
                    else:
                        print("Vul alle velden in.")

                for i, box in enumerate(input_boxes):
                    if box.collidepoint(event.pos):
                        active_box = i

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    active_box = (active_box + 1) % len(input_boxes)
                elif event.key == pygame.K_RETURN:
                    first_name, last_name, email = input_text
                    if first_name and last_name and email:
                        save_user_data(first_name, last_name, email)
                        state = "running"
                    else:
                        print("Vul alle velden in.")
                elif event.key == pygame.K_BACKSPACE:
                    input_text[active_box] = input_text[active_box][:-1]
                else:
                    input_text[active_box] += event.unicode

        elif state == "running":
            for game in games:
                total_score += run_game(game)
            update_total_score(total_score)
            state = "finished"

    # Login scherm tekenen
    if state == "login":
        title_surface = title_font.render("SUPER GAME", True, BLUE)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 100))

        for i, box in enumerate(input_boxes):
            pygame.draw.rect(screen, WHITE, box)
            pygame.draw.rect(screen, BLUE, box, 2)
            text_surface = font.render(input_text[i], True, BLACK)
            screen.blit(text_surface, (box.x + 10, box.y + 10))

            label_text = ["Voornaam:", "Achternaam:", "Email:"][i]
            label_surface = label_font.render(label_text, True, BLACK)
            screen.blit(label_surface, (box.x - 120, box.y + 5))

        pygame.draw.rect(screen, ORANGE, submit_button)
        submit_text = font.render("Submit", True, WHITE)
        screen.blit(submit_text, (submit_button.x + 50, submit_button.y + 10))

        footer_font = pygame.font.Font(None, 20)
        footer_surface = footer_font.render("Zuyd Hogeschool", True, BLACK)
        screen.blit(footer_surface, (20, HEIGHT - 30))

        zuyd_surface = footer_font.render("ZUYD", True, (255, 0, 0))
        screen.blit(zuyd_surface, (WIDTH - 70, HEIGHT - 30))

    elif state == "finished":
        finish_text = font.render(f"All games finished! Total Score: {total_score}", True, BLACK)
        screen.blit(finish_text, (WIDTH // 2 - finish_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()
