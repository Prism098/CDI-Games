import subprocess
import sys
import os
import requests

# Lijst van games met paden naar de submappen
games = [
    {"name": "Data Cleaning Game", "script": "CDI-Games-DataEngineering/DataMain.py"},
    {"name": "Website Interface Builder Game", "script": "CDI-Games-HCI/HCIMain.py"},
    {"name": "Network Invaders", "script": "CDI-Games-SecurityCloud/SecurityMain.py"},
    {"name": "Boolean Bakery", "script": "CDI-Games-SoftwareDevelopment/SoftwareMain.py"}
]

# Totale score
total_score = 0

# Functie om een game te starten en score op te halen
def run_game(game):
    global total_score
    try:
        print(f"Starting {game['name']}...")

        if not os.path.exists(game["script"]):
            print(f"Error: Script {game['script']} not found!")
            return

        result = subprocess.run(
            [sys.executable, game["script"]],
            capture_output=True,
            text=True,
            timeout=60
        )

        print(f"Output from {game['name']}:")
        print(result.stdout)
        print(result.stderr)

        score_found = False
        final_score = 0
        for line in result.stdout.splitlines():
            if "Score:" in line:
                try:
                    final_score = float(line.split(":")[1].strip())
                    score_found = True
                except ValueError:
                    print(f"Invalid score format in {game['name']} output: {line}")

        if score_found:
            print(f"Score for {game['name']}: {final_score}")
            total_score += final_score
        else:
            print(f"No valid score found in output for {game['name']}.")

    except subprocess.TimeoutExpired:
        print(f"Error: {game['name']} timed out!")
    except Exception as e:
        print(f"Error running {game['name']}: {e}")

# Functie om de totale score naar de backend te sturen
def send_score_to_last_user(total_score):
    url = "http://localhost:4000/add-score"
    data = {"totalScore": total_score}
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Score succesvol toegevoegd aan de laatste gebruiker!")
        else:
            print(f"Fout bij het versturen van de score: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Kan geen verbinding maken met de server: {e}")

# Hoofdprogramma om alle games te spelen
def main():
    global total_score
    print("Welcome to the CDI Game Runner!")

    for game in games:
        run_game(game)

    print(f"All games completed! Total Score: {total_score}")

    # Verstuur de totale score naar de backend
    send_score_to_last_user(total_score)

if __name__ == "__main__":
    main()
