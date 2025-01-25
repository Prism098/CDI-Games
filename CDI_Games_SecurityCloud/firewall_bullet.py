import pygame
import constante as c

class FirewallBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(FirewallBullet, self).__init__()
        self.image = pygame.image.load('CDI_Games_SecurityCloud/images/kogels_concept.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // c.SCHIP_GROOTTE, self.image.get_height() // c.SCHIP_GROOTTE))
        self.rect = self.image.get_rect()
        self.rect.centerx = x  # Center the bullet horizontally
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = -6

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if self.rect.y <= 0:
            self.kill()