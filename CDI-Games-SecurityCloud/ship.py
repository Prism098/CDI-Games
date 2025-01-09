import pygame
import constante as c
from kogel import Kogel

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('CDI-Games-SecurityCloud/images/laptop.png').convert_alpha() # Laadt de foto van het schip in image, convert is zodat de game niet lagt
        self.image = pygame.transform.scale(self.image, (self.image.get_width()//c.SCHIP_GROOTTE, self.image.get_height()//c.SCHIP_GROOTTE))
        self.rect = self.image.get_rect() # Maakt een rechthoek rond de foto
        self.rect.x = c.DISPLAY_WIDTH//2 - self.rect.width//2 # Zet het schip in het midden van het scherm
        self.rect.y = c.DISPLAY_HEIGHT - self.rect.height * 2 # Zet het schip onderaan het scherm
        self.kogels = pygame.sprite.Group()
        self.vel_x = 0 # Snelheid van het schip in de x richting
        self.vel_y = 0 # Snelheid van het schip in de y richting    
        self.speed = 15 # Snelheid van het schip

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
        new_kogel.rect.x = self.rect.x + self.rect.width//2 - new_kogel.rect.width//2
        new_kogel.rect.y = self.rect.y
        self.kogels.add(new_kogel)