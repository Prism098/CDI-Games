import pygame
import qrcode
import io

# Initialize Pygame
pygame.init()

# Configuration variables
USE_GRADIENT = False  # Set to True for gradient background
BG_IMAGE_OPACITY = 255  # 0-255 (0 = fully transparent, 255 = fully opaque)
BOX_OPACITY = 150  # 0-255 for box transparency

# Get current screen resolution
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Colors
BG_COLOR = (232, 26, 60)
GRADIENT_COLORS = [(130, 15, 28), (232, 26, 50)]  # From top to bottom
BOX_COLOR = (0, 0, 0, BOX_OPACITY)
BORDER_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)

# Create fullscreen borderless window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 
                               pygame.FULLSCREEN | pygame.NOFRAME)
pygame.display.set_caption("QR Code Scorebord")

# Load custom font
try:
    FONT_PATH = "IBMPlexSans-Medium.ttf"  # Ensure this file exists in your directory
    FONT_SIZE = int(SCREEN_HEIGHT * 0.05)
    FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)
except Exception as e:
    print(f"Font loading error: {e}, using system font")
    FONT = pygame.font.Font(None, FONT_SIZE)

# Try to load background image
bg_image = None
try:
    bg_image = pygame.image.load('images/vormen2.png').convert_alpha()
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_image.set_alpha(BG_IMAGE_OPACITY)
except Exception as e:
    print(f"Background image error: {e}")

# Gebruikersgegevens ophalen
try:
    with open("user_data.txt", "r") as user_file:
        user_email = user_file.readline().strip()  # Lees de e-mail
        total_score = user_file.readline().strip()  # Lees de totalScore
    print(f"Gebruikers e-mail geladen: {user_email}")
    print(f"Totaalscore geladen: {total_score}")
except FileNotFoundError:
    user_email = None
    total_score = "Niet beschikbaar"
    print("Fout: Geen user_data.txt bestand gevonden.")


# Create QR code
qr_data = "https://google.com/"  # Replace with actual data if needed.
qr = qrcode.QRCode(version=1, box_size=10, border=0)
qr.add_data(qr_data)
qr.make(fit=True)

# Create QR code image
qr_image = qr.make_image(fill_color="white", back_color=BG_COLOR)
qr_buffer = io.BytesIO()
qr_image.save(qr_buffer, format="PNG")
qr_buffer.seek(0)
qr_surface = pygame.image.load(qr_buffer, 'PNG')

# Create text surfaces
text1 = FONT.render(f"Eindscore: {total_score}", True, TEXT_COLOR)
text2 = FONT.render("Scan QR code voor een live scorebord", True, TEXT_COLOR)

# Calculate positions
def vertical_center_group(elements, spacing=50):
    total_height = sum(e.get_height() for e in elements) + (len(elements)-1)*spacing
    y_start = (SCREEN_HEIGHT - total_height) // 2
    positions = []
    current_y = y_start
    for element in elements:
        positions.append(element.get_rect(centerx=SCREEN_WIDTH//2, y=current_y))
        current_y += element.get_height() + spacing
    return positions

# Position elements
text1_pos, text2_pos, qr_pos = vertical_center_group(
    [text1, text2, qr_surface],
    spacing=int(SCREEN_HEIGHT * 0.03)
)

# Create single box around all elements
def create_box(content_rects, padding=50):
    min_x = min(r.left for r in content_rects)
    max_x = max(r.right for r in content_rects)
    min_y = min(r.top for r in content_rects)
    max_y = max(r.bottom for r in content_rects)
    
    width = max_x - min_x + padding*2
    height = max_y - min_y + padding*2
    
    box_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    box_surface.fill(BOX_COLOR)
    pygame.draw.rect(box_surface, BORDER_COLOR, (0, 0, width, height), 2)
    
    return box_surface, pygame.Rect(
        min_x - padding,
        min_y - padding,
        width,
        height
    )

box_surface, box_rect = create_box([text1_pos, text2_pos, qr_pos])

# Gradient function
def draw_gradient(surface, colors):
    for y in range(surface.get_height()):
        ratio = y / surface.get_height()
        r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * ratio)
        g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * ratio)
        b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Draw background
    if USE_GRADIENT:
        draw_gradient(screen, GRADIENT_COLORS)
    else:
        screen.fill(BG_COLOR)
    
    # Draw background image with opacity
    if bg_image:
        bg_image.set_alpha(BG_IMAGE_OPACITY)
        screen.blit(bg_image, (0, 0))

    # Draw content box
    screen.blit(box_surface, box_rect)
    
    # Draw elements
    screen.blit(text1, text1_pos)
    screen.blit(text2, text2_pos)
    screen.blit(qr_surface, qr_pos)

    # Update display
    pygame.display.flip()

pygame.quit()
