import pygame
import constante as c
from ship import Ship
from bg import BG
from enemy_spawner import EnemySpawner
from kaboem_spawner import KaboemSpawner
from router import Router
from firewall import Firewall
import os


# Initialize Pygame and font module
pygame.init()
pygame.font.init()

pygame.event.set_grab(True)  # Direct all input to this process
pygame.mouse.set_visible(True)  # Optional: Adjust mouse visibility


# display info
display = pygame.display.set_mode((c.DISPLAY_SIZE), pygame.FULLSCREEN)
fps = c.FPS
clock = pygame.time.Clock()
black = (0, 0, 0)

print("SDL_WINDOWID:", os.environ.get("SDL_WINDOWID"))


# Initialize score
score = [2500]  # Use a list to pass by reference

# Initialize timer
timer = 30  # Timer in seconds
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 1000)  # Set timer to decrease every second

# Load title image
title_image = pygame.image.load('CDI-Games-SecurityCloud/images/network_invaders.png').convert_alpha()

# Load custom font
custom_font_path = 'CDI-Games-SecurityCloud/font/Minecraft.ttf'  # Path to your custom font file
font = pygame.font.Font(custom_font_path, 24)  # Load the custom font with size 36

# object info
bg = BG()
bg_group = pygame.sprite.Group()
bg_group.add(bg)

player = Ship()
spritegroup = pygame.sprite.Group()
spritegroup.add(player)

router = Router(score)
router_group = pygame.sprite.Group()
router_group.add(router)

firewall_group = pygame.sprite.Group()
firewall_image = pygame.image.load('CDI-Games-SecurityCloud/images/firewall_concept_sprite.png')
firewall_width = firewall_image.get_width() // c.SCHIP_GROOTTE

def calculate_firewall_positions():
    spacing = (display.get_width() - 4 * firewall_width) // 5
    positions = []
    for i in range(4):
        firewall_x = spacing + i * (firewall_width + spacing)
        positions.append(firewall_x)
    return positions

def calculate_firewall_y_position():
    return (display.get_height() - firewall_image.get_height() // c.SCHIP_GROOTTE) // 1.4

firewall_positions = calculate_firewall_positions()
firewall_y = calculate_firewall_y_position()
for firewall_x in firewall_positions:
    firewall = Firewall(firewall_x, firewall_y, router, score)
    firewall_group.add(firewall)

enemy_lanes = [None] * 4  # Track which lanes have enemies

enemy_spawner = EnemySpawner(firewall_positions, enemy_lanes, score)

kaboem_spawner = KaboemSpawner()

def game_over_screen(final_score):
    print(f"Score: {final_score}")
    font = pygame.font.Font(custom_font_path, 74)  # Use custom font for game over screen
    text = font.render("Game Over", True, ("#b13e53"))
    text_rect = text.get_rect(center=(c.DISPLAY_WIDTH // 2, c.DISPLAY_HEIGHT // 2 - 100))

    # New text
    message_font = pygame.font.Font(custom_font_path, 50)  # Use custom font for message
    message_text = message_font.render("Al je data is gelekt...", True, (255, 255, 255))
    message_rect = message_text.get_rect(center=(c.DISPLAY_WIDTH // 2, c.DISPLAY_HEIGHT // 2 - 50))

    score_font = pygame.font.Font(custom_font_path, 50)  # Use custom font for score
    score_text = score_font.render(f"Score: {final_score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(c.DISPLAY_WIDTH // 2, c.DISPLAY_HEIGHT // 2 + 50))

    button_font = pygame.font.Font(custom_font_path, 50)  # Use custom font for button
    button_text = button_font.render("Exit", True, (255, 255, 255))
    button_rect = button_text.get_rect(center=(c.DISPLAY_WIDTH // 2, c.DISPLAY_HEIGHT // 2 + 100))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()

        display.fill(black)
        display.blit(text, text_rect)
        display.blit(message_text, message_rect)  # Blit the new message text
        display.blit(score_text, score_rect)
        pygame.draw.rect(display, ("#b13e53"), button_rect.inflate(20, 20))
        display.blit(button_text, button_rect)
        pygame.display.update()

def you_survived_screen(final_score):
    print(f"Score: {final_score}")
    font = pygame.font.Font(custom_font_path, 74)  # Use custom font for "You Survived" screen
    text = font.render("Router Beschermd!", True, ("#38b764"))
    text_rect = text.get_rect(center=(c.DISPLAY_WIDTH // 2, c.DISPLAY_HEIGHT // 2 - 100))

    # New text
    message_font = pygame.font.Font(custom_font_path, 50)  # Use custom font for message
    message_text = message_font.render("Hmm, er lijkt toch wat van je data te zijn gelekt...", True, (255, 255, 255))
    message_rect = message_text.get_rect(center=(c.DISPLAY_WIDTH // 2, c.DISPLAY_HEIGHT // 2 - 50))

    score_font = pygame.font.Font(custom_font_path, 50)  # Use custom font for score
    score_text = score_font.render(f"Score: {final_score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(c.DISPLAY_WIDTH // 2, c.DISPLAY_HEIGHT // 2 + 50))

    button_font = pygame.font.Font(custom_font_path, 50)  # Use custom font for button
    button_text = button_font.render("Exit", True, (255, 255, 255))
    button_rect = button_text.get_rect(center=(c.DISPLAY_WIDTH // 2, c.DISPLAY_HEIGHT // 2 + 100))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()

        display.fill(black)
        display.blit(text, text_rect)
        display.blit(message_text, message_rect)  # Blit the new message text
        display.blit(score_text, score_rect)
        pygame.draw.rect(display, (0, 255, 0), button_rect.inflate(20, 20))
        display.blit(button_text, button_rect)
        pygame.display.update()


# Startscherm
Startscherm = True

controls_image_arrows = pygame.image.load('CDI-Games-SecurityCloud/images/controlls_arrows_sprite.png').convert_alpha()
controls_image_arrows = pygame.transform.scale(controls_image_arrows, (400, 300))  # Adjust the size as needed

controls_image_spatie = pygame.image.load('CDI-Games-SecurityCloud/images/controlls_spatie_sprite.png').convert_alpha()
controls_image_spatie = pygame.transform.scale(controls_image_spatie, (400, 300))  # Adjust the size as needed

while Startscherm:
    for event in pygame.event.get():
        print(event)  # Log all events for debugging
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Startscherm = False
                running = True

    display.fill("#1a1c2c")
    font = pygame.font.Font(custom_font_path, 50)
    text = font.render("Welkom bij Network Invaders!", True, ("#41a6f6"))
    text_rect = text.get_rect(center=(c.DISPLAY_WIDTH // 2, 50))

    font = pygame.font.Font(custom_font_path, 26)
    text2 = font.render("In dit spel ga jij ons netwerk verdedigen van het kwaadaardige team scraper!", True, (255, 255, 255))
    text2_rect = text2.get_rect(center=(c.DISPLAY_WIDTH // 2, 100))

    font = pygame.font.Font(custom_font_path, 26)
    text3 = font.render("De bedoeling is dat je de Firewalls aan sterkt met pakketjes om zo de hackers te kunnen verslaan.", True, (255, 255, 255))
    text3_rect = text3.get_rect(center=(c.DISPLAY_WIDTH // 2, 126))    

    font = pygame.font.Font(custom_font_path, 26)
    text4 = font.render("Dit doe je door op de Firewalls te schieten.", True, (255, 255, 255))
    text4_rect = text4.get_rect(center=(c.DISPLAY_WIDTH // 2, 152)) 

    font = pygame.font.Font(custom_font_path, 26)
    text5 = font.render("De Controls zijn: ", True, (255, 255, 255))
    text5_rect = text5.get_rect(center=(c.DISPLAY_WIDTH // 2, 200)) 

    font = pygame.font.Font(custom_font_path, 26)
    text6 = font.render("Gebruik de pijltjes toetsen om te bewegen en de spatiebalk om te schieten.", True, (255, 255, 255))
    text6_rect = text6.get_rect(center=(c.DISPLAY_WIDTH // 2, 226))

    font = pygame.font.Font(custom_font_path, 36)
    text7 = font.render("Druk op SPATIE om te beginnen", True, (255, 255, 255))
    text7_rect = text7.get_rect(center=(c.DISPLAY_WIDTH // 2, c.DISPLAY_HEIGHT // 2 + 100))

    display.blit(text, text_rect)
    display.blit(text2, text2_rect)
    display.blit(text3, text3_rect)
    display.blit(text4, text4_rect)
    display.blit(text5, text5_rect)
    display.blit(text6, text6_rect)
    display.blit(text7, text7_rect)



    # Display the controls image
    controls_image_rect = controls_image_arrows.get_rect(center=(500, 300))
    display.blit(controls_image_arrows, controls_image_rect)

    controls_image2_rect = controls_image_spatie.get_rect(center=(900, 250))
    display.blit(controls_image_spatie, controls_image2_rect)
    pygame.display.update()


# Game loop

while running:
    # Ticke Clock (voor de fps)
    clock.tick(fps)

    # Handle events (input)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.VIDEORESIZE:
            display = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            firewall_positions = calculate_firewall_positions()
            firewall_y = calculate_firewall_y_position()
            for i, firewall in enumerate(firewall_group):
                firewall.rect.x = firewall_positions[i]
                firewall.rect.y = firewall_y
        elif event.type == timer_event:
            timer -= 1
            if timer <= 0:
                you_survived_screen(score[0])

        # Handle input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.vel_x = -player.speed
            elif event.key == pygame.K_RIGHT:
                player.vel_x = player.speed

            if event.key == pygame.K_SPACE:
                player.shiet()

        # Stop moving when key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.vel_x = 0
            elif event.key == pygame.K_RIGHT:
                player.vel_x = 0

    # update all the objects (states of objects)
    bg_group.update()
    spritegroup.update()
    enemy_spawner.update()
    kaboem_spawner.update()
    router_group.update()
    firewall_group.update()

    # Check for collisions between player's bullets and firewalls
    for firewall in firewall_group:
        collided = pygame.sprite.spritecollide(firewall, player.kogels, True)
        for bullet in collided:
            firewall.get_hit()

    # Check for collisions between firewall bullets and enemies
    for firewall in firewall_group:
        collided = pygame.sprite.groupcollide(firewall.bullets, enemy_spawner.enemy_group, True, False)
        for bullet, enemies in collided.items():
            for enemy in enemies:
                enemy.get_hit()

    # Check for collisions between enemies and firewalls
    for firewall in firewall_group:
        for enemy in enemy_spawner.enemy_group:
            if enemy.rect.colliderect(firewall.rect) and enemy.vel_y == 0:
                enemy.deal_damage(firewall)

    # Check for game over condition
    if router.hp <= 0 or all(firewall.hp <= 0 for firewall in firewall_group):
        game_over_screen(score[0])

    # Render objects to the screen
    display.fill(black)
    bg_group.draw(display)
    spritegroup.draw(display)
    player.kogels.draw(display)
    firewall_group.draw(display)
    for firewall in firewall_group:
        firewall.bullets.draw(display)
        firewall.draw_hp_bar(display)
    router_group.draw(display)
    router.draw_hp_bar(display)  # Draw the router's HP bar
    enemy_spawner.enemy_group.draw(display)  # Draw enemies after firewalls
    for enemy in enemy_spawner.enemy_group:
        enemy.draw_hp_bar(display)  # Draw the HP bar for each enemy
    kaboem_spawner.kaboem_group.draw(display)

    # Draw the banner
    banner_color = ("#333C57")  # Hex color #333C57
    banner_height = 150
    pygame.draw.rect(display, banner_color, (0, 0, display.get_width(), banner_height))
    display.blit(title_image, (display.get_width() // 2 - title_image.get_width() // 2, 10))

    # Render the score below the banner
    score_text = font.render(f"Score: {score[0]}", True, (255, 255, 255))
    display.blit(score_text, (10, banner_height + 10))

    # Render the timer below the banner
    timer_text = font.render(f"Time: {timer}", True, (255, 255, 255))
    display.blit(timer_text, (display.get_width() - 150, banner_height + 10))

    pygame.display.update()