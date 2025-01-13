import pygame
import constante as c

class Enemy(pygame.sprite.Sprite):
    def __init__(self, initial_x, stop_y, enemy_spawner, score):
        super(Enemy, self).__init__()
        self.image = pygame.image.load('CDI-Games-SecurityCloud/images/hacker_sprite.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // c.SCHIP_GROOTTE, self.image.get_height() // c.SCHIP_GROOTTE))
        self.rect = self.image.get_rect()
        self.rect.x = initial_x
        self.rect.y = -self.rect.height
        self.hp = 3
        self.max_hp = 3  # Store the maximum HP for the HP bar
        self.vel_x = 0
        self.vel_y = 4
        self.stop_y = stop_y
        self.damage_timer = 0  # Timer to control damage rate
        self.enemy_spawner = enemy_spawner  # Reference to the enemy spawner
        self.score = score  # Reference to the score

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if self.rect.y >= self.stop_y:
            self.rect.y = self.stop_y
            self.vel_y = 0

    def get_hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.destroy()

    def destroy(self):
        self.kill()
        # Remove from lane
        for i, lane in enumerate(self.enemy_spawner.enemy_lanes):
            if lane == self:
                self.enemy_spawner.enemy_lanes[i] = None

    def deal_damage(self, firewall):
        if self.damage_timer <= 0:
            firewall.take_damage(2)  # Deal 2 damage per second
            self.damage_timer = c.FPS  # Reset timer to 1 second
        else:
            self.damage_timer -= 1

    def draw_hp_bar(self, surface):
        # Draw the HP bar above the enemy
        bar_width = self.rect.width
        bar_height = 5
        fill = (self.hp / self.max_hp) * bar_width
        outline_rect = pygame.Rect(self.rect.x, self.rect.y - 10, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y - 10, fill, bar_height)
        pygame.draw.rect(surface, ("#b13e53"), fill_rect)
        pygame.draw.rect(surface, (255, 255, 255), outline_rect, 1)