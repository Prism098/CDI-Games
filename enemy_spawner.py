import pygame
from enemy import Enemy
import constante as c
import random as r


class EnemySpawner:
    def __init__(self):
        self.enemy_group = pygame.sprite.Group()
        self.spawn_timer = r.randrange(int(c.FPS / 2), int(c.FPS * 2))

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
        new_enemy = Enemy()
        self.enemy_group.add(new_enemy)
