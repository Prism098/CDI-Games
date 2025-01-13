import pygame
import constante as c


class Kogel(pygame.sprite.Sprite):
    def __init__(self):
        super(Kogel, self).__init__()
        self.width = 4
        self.height = self.width * 2
        self.size = (self.width, self.height)
        self.image = pygame.Surface(self.size)
        self.color = ("#41a6f6")
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.vel_x = 0
        self.vel_y = -8

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y