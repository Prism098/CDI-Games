import subprocess
import sys
import os

# Lijst van games met paden naar de submappen
games = [
    {"name": "Data Cleaning Game", "script": "CDI-Games-DataEngineering/DataMain.py"},
   # {"name": "Website Interface Builder Game", "script": "CDI-Games-HCI/HCIMain.py"},
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
        
        # Controleer of het script bestaat
        if not os.path.exists(game["script"]):
            print(f"Error: Script {game['script']} not found!")
            return
        
        # Voer de game uit als subprocess
        result = subprocess.run(
            [sys.executable, game["script"]],
            capture_output=True,
            text=True,
            timeout=60  # Maximaal 60 seconden wachten
        )

        # Debug-uitvoer
        print(f"Output from {game['name']}:")
        print(result.stdout)
        print(result.stderr)

        # Score verwerken vanuit de uitvoer
        for line in result.stdout.splitlines():
            if "Score:" in line:
                try:
                    score = int(line.split(":")[1].strip())
                    print(f"Score for {game['name']}: {score}")
                    total_score += score
                    break
                except ValueError:
                    print(f"Invalid score format in {game['name']} output: {line}")
    except subprocess.TimeoutExpired:
        print(f"Error: {game['name']} timed out!")
    except Exception as e:
        print(f"Error running {game['name']}: {e}")

# Hoofdprogramma om alle games te spelen
def main():
    print("Welcome to the CDI Game Runner!")

    for game in games:
        run_game(game)

    print(f"All games completed! Total Score: {total_score}")

if __name__ == "__main__":
    main()
