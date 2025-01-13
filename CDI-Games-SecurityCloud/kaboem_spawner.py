import pygame
from kaboem import Kaboem
import constante as c
import random as r

class KaboemSpawner:
    def __init__(self):
        self.kaboem_group = pygame.sprite.Group()

    def update(self):
        self.kaboem_group.update()
        

    def spawn_kaboem(self, pos):
        random_nummer = r.randint(3, 30)
        for num_kaboem in range(random_nummer):
            new_kaboem = Kaboem()
            new_kaboem.rect.x = pos[0]
            new_kaboem.rect.y = pos[1]
            self.kaboem_group.add(new_kaboem)