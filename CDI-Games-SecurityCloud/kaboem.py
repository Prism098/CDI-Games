import pygame
import constante as c
import random as r

class Kaboem(pygame.sprite.Sprite):
    def __init__(self):
        super(Kaboem, self).__init__()
        self.width = r.randrange(1, 6)
        self.height = self.width
        self.size = (self.width, self.height)
        self.image = pygame.Surface(self.size)
        self.color = (r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.kill_timer = c.FPS
        self.vel_x = r.randrange(-16, 16)
        self.vel_y = r.randrange(-16, 16)

    
    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if self.kill_timer == 0:
            self.kill()
        else:
            self.kill_timer -= 1