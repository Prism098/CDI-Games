import pygame
import qrcode
import io

# Initialiseer Pygame
pygame.init()

# Scherminstellingen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)
FONT = pygame.font.Font(None, 36)

# Maak scherm
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Scan QR-code om het scorebord bij te werken")

# QR-code genereren
qr_data = "https://google.com/"
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(qr_data)
qr.make(fit=True)

# QR-code omzetten naar Pygame image
qr_image = qr.make_image(fill_color="black", back_color="white")
qr_buffer = io.BytesIO()
qr_image.save(qr_buffer, format="PNG")
qr_buffer.seek(0)
qr_surface = pygame.image.load(qr_buffer, 'PNG')
qr_rect = qr_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))

# Tekst renderen
text = FONT.render("Scan de QR-code om live het scorebord te updaten", True, TEXT_COLOR)
text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Scherm vullen
    screen.fill(BG_COLOR)

    # QR-code en tekst tekenen
    screen.blit(qr_surface, qr_rect)
    screen.blit(text, text_rect)

    # Scherm bijwerken
    pygame.display.flip()

pygame.quit()
