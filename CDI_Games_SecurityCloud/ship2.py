import pygame
import constante as c
from kogel import Kogel

class Ship(pygame.sprite.Sprite):
    def __init__(self, firewall_positions):
        super().__init__()
        self.image = pygame.image.load('CDI_Games_SecurityCloud/images/laptop.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // c.SCHIP_GROOTTE, self.image.get_height() // c.SCHIP_GROOTTE))
        self.rect = self.image.get_rect()
        self.rect.x = c.DISPLAY_WIDTH // 2 - self.rect.width // 2
        self.rect.y = c.DISPLAY_HEIGHT - self.rect.height * 2
        self.kogels = pygame.sprite.Group()
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 12
        self.firewall_positions = firewall_positions
        self.current_lane = 0

    def update(self):
        self.kogels.update()
        for kogel in self.kogels:
            if kogel.rect.y <= 0:
                self.kogels.remove(kogel)
        self.rect.x += self.vel_x
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= c.DISPLAY_WIDTH - self.rect.width:
            self.rect.x = c.DISPLAY_WIDTH - self.rect.width
        self.rect.y += self.vel_y

    def shiet(self):
        new_kogel = Kogel()
        new_kogel.rect.x = self.rect.x + self.rect.width // 2 - new_kogel.rect.width // 2
        new_kogel.rect.y = self.rect.y
        self.kogels.add(new_kogel)

    def snap_to_lane(self, direction):
        if direction == "left" and self.current_lane > 0:
            self.current_lane -= 1
        elif direction == "right" and self.current_lane < len(self.firewall_positions) - 1:
            self.current_lane += 1
        self.rect.x = self.firewall_positions[self.current_lane] + (self.firewall_positions[1] - self.firewall_positions[0]) // 2 - self.rect.width * 1.75