import pygame
import constante as c
import random as r

class Ster(pygame.sprite.Sprite):
    def __init__(self):
        super(Ster, self).__init__()
        self.width = r.randrange(1, 4)
        self.height = self.width
        self.size = (self.width, self.height)
        self.image = pygame.Surface(self.size)
        self.color = (r.randrange(0, 255), r.randrange(0, 255), r.randrange(0, 255))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = r.randrange(0, c.DISPLAY_SIZE[0])
        self.vel_x = 0
        self.vel_y = r.randrange(4, 25)

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y