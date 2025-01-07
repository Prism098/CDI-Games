import pygame
import constante as c
from ship import Ship
from bg import BG
from enemy_spawner import EnemySpawner
from kaboem_spawner import KaboemSpawner

# display info
display = pygame.display.set_mode((c.DISPLAY_SIZE))
fps = c.FPS
clock = pygame.time.Clock()
black = (0, 0, 0)

# object info
bg = BG()
bg_group = pygame.sprite.Group()
bg_group.add(bg)

player = Ship()
spritegroup = pygame.sprite.Group()
spritegroup.add(player)

enemy_spawner = EnemySpawner()

kaboem_spawner = KaboemSpawner()



# Game loop
running = True
while running:
    # Ticke Clock (voor de fps)
    clock.tick(fps)

    # Handle events (input)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


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


    # Check for collisions
    collided = pygame.sprite.groupcollide(player.kogels, enemy_spawner.enemy_group, True, False)
    for bullet, enemy in collided.items():
        enemy[0].get_hit()
        kaboem_spawner.spawn_kaboem((bullet.rect.x, bullet.rect.y))
        


    # Render objects to the screen
    display.fill(black)
    bg_group.draw(display)
    spritegroup.draw(display)
    player.kogels.draw(display)
    enemy_spawner.enemy_group.draw(display)
    kaboem_spawner.kaboem_group.draw(display)
    pygame.display.update()