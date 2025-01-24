import random
from datetime import datetime, timedelta

ROWS = 8
COLUMNS = 6

def generate_random_date():
    year = random.randint(1995, 2005)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Simpel om geldige datums te garanderen
    return f"{year}-{month:02d}-{day:02d}"

def generate_random_start_date():
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2024, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_date = start_date + timedelta(days=random_days)
    return random_date.strftime("%Y-%m-%d")

def generate_dataset():
    dataset = []
    for r in range(ROWS):
        row_data = []
        for c in range(COLUMNS):
            rnd = random.random()

            # Bepaal status zonder outliers
            if rnd < 0.10:
                status = "missing"
            elif rnd < 0.40:
                status = "incorrect"
            else:
                status = "correct"

            # Waarde genereren op basis van kolom en status
            if c == 0:  # Distance (km)
                if status == "missing":
                    value_str = ""
                elif status == "incorrect":
                    value_str = random.choice([
                        f"{random.randint(-50, -1)}km",  # Negatieve waarden
                        f"{random.randint(100, 400)}km",
                        "??"  # Foutieve eenheid
                    ])
                else:
                    value_str = f"{random.randint(1, 60)}km"  # Correcte waarden
            elif c == 1:  # Transport
                if status == "missing":
                    value_str = ""
                elif status == "incorrect":
                    value_str = random.choice([
                        "Bezem",
                        "Luchtballon",
                        "Tapijt",
                        "Kangoeroe",
                        "Tijdmachine"
                    ])
                else:
                    value_str = random.choice(["Auto", "Trein", "Fiets", "Te voet"])
            elif c == 2:  # Average Grade
                if status == "missing":
                    value_str = ""
                elif status == "incorrect":
                    value_str = str(random.randint(11, 18))  # Onrealistische hoge cijfers
                else:
                    value_str = str(random.randint(1, 10))  # Redelijke cijfers
            elif c == 3:  # Highest Grade
                if status == "missing":
                    value_str = ""
                elif status == "incorrect":
                    value_str = str(random.randint(11, 18))  # Onrealistisch hoog
                else:
                    value_str = str(random.randint(5, 10))  # Redelijke hoogste score
            elif c == 4:  # Birth Date
                if status == "missing":
                    value_str = ""
                elif status == "incorrect":
                    value_str = "2025-12-31"  # Toekomstige datum
                else:
                    value_str = generate_random_date()
            elif c == 5:  # Start Date
                if status == "missing":
                    value_str = ""
                elif status == "incorrect":
                    value_str = "1945-01-01"
                else:
                    value_str = generate_random_start_date()

            # Voeg cel toe aan rij
            row_data.append({
                "status": status,
                "value": value_str,
                "clicked": False,
                "mark": None
            })
        dataset.append(row_data)
    return dataset
