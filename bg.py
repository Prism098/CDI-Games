import pygame
import constante as c
from ster import Ster
import random as r


class BG(pygame.sprite.Sprite):
    def __init__(self):
        super(BG, self).__init__()
        self.image = pygame.Surface(c.DISPLAY_SIZE)
        self.color = (0, 0, 15)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.sterren = pygame.sprite.Group()
        self.timer = r.randrange(1, 10)



    def update(self):
        self.sterren.update()
        for ster in self.sterren:
            if ster.rect.y >= c.DISPLAY_HEIGHT:
                self.sterren.remove(ster)
        if self.timer == 0:
            new_ster = Ster()
            self.sterren.add(new_ster)
            self.timer = r.randrange(1, 10)
        self.image.fill(self.color)
        self.sterren.draw(self.image)
        self.timer -= 1