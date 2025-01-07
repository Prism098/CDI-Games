import pygame
from enemy import Enemy
import constante as c
import random as r

class EnemySpawner:
    def __init__(self, firewall_positions, enemy_lanes, score):
        self.enemy_group = pygame.sprite.Group()
        self.spawn_timer = r.randrange(int(c.FPS / 2), int(c.FPS * 2))
        self.firewall_positions = firewall_positions
        self.enemy_lanes = enemy_lanes
        self.score = score  # Reference to the score

    def update(self):
        self.enemy_group.update()
        for enemy in self.enemy_group:
            if enemy.rect.y >= c.DISPLAY_HEIGHT:
                self.enemy_group.remove(enemy)
        if self.spawn_timer == 0:
            self.spawn_enemy()
            self.spawn_timer = r.randrange(int(c.FPS / 2), int(c.FPS * 2))
        else:
            self.spawn_timer -= 1

    def spawn_enemy(self):
        lane_indices = list(range(len(self.enemy_lanes)))
        r.shuffle(lane_indices)
        for i in lane_indices:
            if self.enemy_lanes[i] is None:
                firewall_image = pygame.image.load('images/firewall_concept_sprite.png')
                firewall_height = firewall_image.get_height() // c.SCHIP_GROOTTE
                firewall_y = (c.DISPLAY_SIZE[1] - firewall_height) // 1.4
                
                enemy = Enemy(self.firewall_positions[i], firewall_y, self, self.score)
                self.enemy_group.add(enemy)
                self.enemy_lanes[i] = enemy
                break