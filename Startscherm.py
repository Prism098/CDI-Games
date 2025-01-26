import pygame
import subprocess
import sys
import os
import requests
import time

# Stel de werkmap in
script_dir = os.path.dirname(os.path.abspath(__file__))
user_data_path = os.path.join(script_dir, "user_data.json")

# MongoDB server configuratie
SERVER_URL = "http://localhost:4000"

# Lijst van games met absolute paden
games = [
    {"name": "Website Interface Builder Game", "script": os.path.join(script_dir, "CDI_Games_HCI", "HCIMain.py")},
    {"name": "Data Cleaning Game", "script": os.path.join(script_dir, "CDI_Games_DataEngineering", "main.py")},
    {"name": "Code Racer", "script": os.path.join(script_dir, "CDI_Games_SoftwareDevelopment", "caride.py")},
    {"name": "Network Invaders", "script": os.path.join(script_dir, "CDI_Games_SecurityCloud", "SecurityMain.py")},
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
                return int(float(line.split(":")[1].strip()))
    except Exception as e:
        print(f"Error running {game['name']}: {e}")
    return 0

# Pygame setup
pygame.init()

# Scherminstellingen
WIDTH, HEIGHT = 1920, 1080
DISPLAY_SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode((DISPLAY_SIZE), pygame.FULLSCREEN)
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
    pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 60, 300, 40),  # Voornaam
    pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 40),  # Achternaam
    pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 60, 300, 40),  # E-mail
]
active_box = 0
input_text = ["", "", ""]

# Knoppen
submit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 140, 200, 50)

# Functies voor gebruikersgegevens
def save_user_data(first_name, last_name, email):
    data = {
        "name": f"{first_name} {last_name}",
        "email": email.strip().lower(),  # Normalize de e-mail
        "status": "not started",
        "totalScore": 0
    }
    print(f"Opslaan gebruiker: {data}")  # Debuggen
    try:
        response = requests.post(f"{SERVER_URL}/save", json=data)
        if response.status_code == 201:
            print("Gebruikersgegevens succesvol opgeslagen in MongoDB.")
        else:
            print(f"Fout bij opslaan in MongoDB: {response.text}")
    except Exception as e:
        print(f"Kan geen verbinding maken met de server: {e}")


def update_total_score(email, total_score, first_name, last_name):
    try:
        # Payload voorbereiden
        payload = {"email": email, "name": f"{first_name} {last_name}", "totalScore": total_score}
        print(f"Verzonden payload naar server: {payload}")  # Debugging

        # Score updaten in de database
        response = requests.post(f"{SERVER_URL}/add-score", json=payload)

        if response.status_code == 200:
            print("Totaalscore succesvol toegevoegd aan de database.")

            # Schrijf ook naar user_data.txt
            with open("user_data.txt", "w") as user_file:
                user_file.write(f"{email}\n")  # Schrijf de e-mail van de gebruiker
                user_file.write(f"{total_score}\n")  # Schrijf de totalScore van de gebruiker
            print("Totaalscore ook succesvol naar user_data.txt geschreven.")
        else:
            print(f"Fout bij toevoegen van totaalscore: {response.text}")
    except Exception as e:
        print(f"Kan geen verbinding maken met de server: {e}")



# Hoofdloop
running = True
cursor_visible = True
cursor_timer = pygame.time.get_ticks()

while running:
    screen.fill(("#1a1c2c") if state == "login" else (255, 255, 255))

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
            update_total_score(email, total_score, first_name, last_name)
            state = "finished"

    # Login scherm tekenen
    if state == "login":
        title_surface = title_font.render("Opendag Zuyd 2025 HBO-ICT", True, ("#41a6f6"))
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT // 2 - 200))

        for i, box in enumerate(input_boxes):
            pygame.draw.rect(screen, (255, 255, 255), box)
            pygame.draw.rect(screen, ("#41a6f6"), box, 2)
            text_surface = font.render(input_text[i], True, (0, 0, 0))
            screen.blit(text_surface, (box.x + 10, box.y + 10))

            label_text = ["Voornaam:", "Achternaam:", "Email:"][i]
            label_surface = label_font.render(label_text, True, (255, 255, 255))
            screen.blit(label_surface, (box.x - 170, box.y + 5))


            zuyd_banner1 = pygame.image.load('CDI_Games_SecurityCloud/images/zuyd_banner_sprite.png').convert_alpha()
            zuyd_banner1 = pygame.transform.scale(zuyd_banner1, (300, 300))  # Adjust the size as needed
            screen.blit(zuyd_banner1, (WIDTH // 2 - 750  , HEIGHT // 2 - 200))


            zuyd_banner2 = pygame.image.load('CDI_Games_SecurityCloud/images/zuyd_banner_sprite.png').convert_alpha()
            zuyd_banner2 = pygame.transform.scale(zuyd_banner2, (300, 300))  # Adjust the size as needed
            screen.blit(zuyd_banner2, (WIDTH // 2 + 400  , HEIGHT // 2 - 200))

            # Draw the blinking cursor
            if i == active_box and cursor_visible:
                cursor_pos = box.x + 10 + text_surface.get_width() + 2
                pygame.draw.line(screen, (0, 0, 0), (cursor_pos, box.y + 10), (cursor_pos, box.y + 30), 2)

        pygame.draw.rect(screen, ("#ef7d57"), submit_button)
        submit_text = font.render("Submit", True, (255, 255, 255))
        screen.blit(submit_text, (submit_button.x + 50, submit_button.y + 10))

        footer_font = pygame.font.Font(None, 20)
        footer_surface = footer_font.render("Zuyd Hogeschool", True, (255, 255, 255))
        screen.blit(footer_surface, (20, HEIGHT - 30))

        zuyd_surface = footer_font.render("ZUYD", True, (255, 0, 0))
        screen.blit(zuyd_surface, (WIDTH - 70, HEIGHT - 30))

    elif state == "finished":
        # Schrijf de e-mail naar een bestand
        # Schrijf e-mail en totalScore naar het bestand
        with open("user_data.txt", "w") as user_file:
            user_file.write(f"{email}\n")  # Schrijf de e-mail van de gebruiker
            user_file.write(f"{total_score}\n")  # Schrijf de totalScore van de gebruiker
        


        pygame.quit()  # Sluit huidige Pygame-instantie
        subprocess.run([sys.executable, os.path.join(script_dir, "QR-code.py")])
        state = "login"  # Keer terug naar login voor de volgende gebruiker

    # Toggle cursor visibility
    if pygame.time.get_ticks() - cursor_timer > 500:
        cursor_visible = not cursor_visible
        cursor_timer = pygame.time.get_ticks()

    pygame.display.flip()

pygame.quit()
