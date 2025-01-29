import pygame
import qrcode
import io
import requests

# =========================
# Configuratie en Initialisatie
# =========================

# Pygame initialisatie
pygame.init()

# Serverconfiguratie
SERVER_URL = "http://localhost:4000"

# Scherminstellingen
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.NOFRAME)
pygame.display.set_caption("QR Code Scorebord")

# Kleuren
BG_COLOR = (20, 20, 40)  # Donkerblauwe achtergrond
TEXT_COLOR = (255, 255, 255)  # Witte tekst
BOX_COLOR = (0, 0, 0, 150)  # Transparante zwarte box
BORDER_COLOR = (255, 255, 255)  # Witte rand

# Lettertype-instellingen
try:
    FONT_PATH = "IBMPlexSans-Medium.ttf"
    FONT_SIZE = int(SCREEN_HEIGHT * 0.05)
    FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)
except Exception as e:
    print(f"Fout bij laden van lettertype: {e}")
    FONT = pygame.font.Font(None, FONT_SIZE)

# Achtergrondafbeelding (optioneel)
try:
    bg_image = pygame.image.load("achtergrond.png").convert()
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except Exception as e:
    print(f"Fout bij laden achtergrond: {e}")
    bg_image = None

# =========================
# Gebruikersgegevens
# =========================

# Gebruikersdata ophalen
try:
    with open("user_data.txt", "r") as user_file:
        user_id = user_file.readline().strip()  # Lees het ObjectId
        user_email = user_file.readline().strip()  # Lees de e-mail
        total_score = user_file.readline().strip()  # Lees de score
    print(f"Gebruiker geladen: ID: {user_id}, E-mail: {user_email}, Score: {total_score}")
except FileNotFoundError:
    user_id = None
    user_email = None
    total_score = "Onbekend"
    print("Fout: user_data.txt niet gevonden.")

# =========================
# QR-code genereren
# =========================

if user_id:
    qr_data = f"http://20.86.37.173/api/scan/{user_id}"  # Link met ObjectId
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")

    qr_buffer = io.BytesIO()
    qr_image.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)
    qr_surface = pygame.image.load(qr_buffer, 'PNG')
    print(f"QR-code succesvol gegenereerd: {qr_data}")
else:
    qr_surface = None
    print("Geen ObjectId beschikbaar. QR-code niet gegenereerd.")

# =========================
# Functies
# =========================

def update_qr_scanned_status(user_id):
    """Update de status van de QR-scan in de server."""
    try:
        response = requests.post(f"{SERVER_URL}/qr-scanned", json={"id": user_id})
        if response.status_code == 200:
            print("QR-scanstatus succesvol bijgewerkt.")
        else:
            print(f"Fout bij bijwerken: {response.text}")
    except Exception as e:
        print(f"Fout: Kan geen verbinding maken met de server: {e}")

def vertical_center_group(elements, spacing=50):
    """Bereken verticale posities voor elementen."""
    total_height = sum(e.get_height() for e in elements) + (len(elements) - 1) * spacing
    y_start = (SCREEN_HEIGHT - total_height) // 2
    positions = []
    current_y = y_start
    for element in elements:
        positions.append(element.get_rect(centerx=SCREEN_WIDTH // 2, y=current_y))
        current_y += element.get_height() + spacing
    return positions

# =========================
# Layout en Posities
# =========================

# =========================
# Layout en Posities
# =========================

if user_id and total_score != "Onbekend":
    text1 = FONT.render(f"Eindscore: {total_score}", True, TEXT_COLOR)
    text2 = FONT.render("Scan de QR-code om het scorebord te volgen!", True, TEXT_COLOR)
    text3 = FONT.render("Ga nu door naar replay voor deel 2!", True, TEXT_COLOR)  # Nieuwe tekst

    elements = [text1, text2]
    if qr_surface:
        elements.append(qr_surface)
    elements.append(text3)  # Voeg de nieuwe tekst toe

    # Posities berekenen
    text1_pos, text2_pos, qr_pos, text3_pos = vertical_center_group(
        elements,
        spacing=int(SCREEN_HEIGHT * 0.03)
    )


# =========================
# Hoofdprogramma
# =========================

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        # Simuleer QR-scan met Enter-toets
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if user_id:
                update_qr_scanned_status(user_id)

    # Achtergrond
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(BG_COLOR)

    # Teken transparante box
    box_width = SCREEN_WIDTH * 0.6
    box_height = SCREEN_HEIGHT * 0.8
    box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
    box_surface.fill(BOX_COLOR)
    box_rect = box_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    pygame.draw.rect(box_surface, BORDER_COLOR, box_surface.get_rect(), 5)
    screen.blit(box_surface, box_rect)

    # Teken elementen
      # Teken elementen
    if user_id and total_score != "Onbekend":
        screen.blit(text1, text1_pos)
        screen.blit(text2, text2_pos)
        if qr_surface:
            screen.blit(qr_surface, qr_pos)
        screen.blit(text3, text3_pos)  # Nieuwe tekst weergeven


    pygame.display.flip()

pygame.quit()
