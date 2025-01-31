import pygame
import constante as c
from firewall_bullet import FirewallBullet

class Firewall(pygame.sprite.Sprite):
    def __init__(self, initial_x, initial_y, router, score):
        super(Firewall, self).__init__()
        self.image = pygame.image.load('CDI_Games_SecurityCloud/images/firewall_concept_sprite.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // c.SCHIP_GROOTTE, self.image.get_height() // c.SCHIP_GROOTTE))
        self.rect = self.image.get_rect()
        self.rect.x = initial_x
        self.rect.y = initial_y  # Position at the bottom of the screen
        self.hp = 30
        self.max_hp = 30
        self.hit_count = 0
        self.vel_x = 0
        self.vel_y = 0
        self.bullets = pygame.sprite.Group()
        self.router = router  # Reference to the router
        self.score = score  # Reference to the score

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.bullets.update()

    def get_hit(self):
        self.hit_count += 1
        if self.hit_count >= 3:
            self.fire_bullet()
            self.hit_count = 0

    def fire_bullet(self):
        bullet = FirewallBullet(self.rect.centerx, self.rect.top)
        self.bullets.add(bullet)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.destroy()

    def destroy(self):
        self.score[0] -= 500  # Decrease the score by 500 points
        self.router.take_damage(25)  # Damage the router by 25 HP when the firewall is destroyed
        self.kill()

    def draw_hp_bar(self, surface):
        # Draw the HP bar below the firewall
        bar_width = self.rect.width
        bar_height = 5
        fill = (self.hp / self.max_hp) * bar_width
        outline_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height + 2, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height + 2, fill, bar_height)
        pygame.draw.rect(surface, ("#a7f070"), fill_rect)
        pygame.draw.rect(surface, (255, 255, 255), outline_rect, 1)