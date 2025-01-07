import pygame
import constante as c
import random as r

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.image.load('images/enemy_1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // c.SCHIP_GROOTTE, self.image.get_height() // c.SCHIP_GROOTTE))
        self.rect = self.image.get_rect()
        self.rect.x = r.randrange(0, c.DISPLAY_SIZE[0] - self.rect.width)
        self.rect.y = -self.rect.height
        self.hp = 3
        self.vel_x = 0
        self.vel_y = r.randrange(3, 8)
        self.type = r.choice(['enemy_1', 'enemy_2', 'enemy_3', 'enemy_4'])
        self.image = pygame.image.load(f'images/{self.type}.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))


    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def get_hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.destroy()
        

    def destroy(self):
        self.kill()