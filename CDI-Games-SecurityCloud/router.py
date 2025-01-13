import pygame
import constante as c

class Router(pygame.sprite.Sprite):
    def __init__(self, score):
        super(Router, self).__init__()
        self.image = pygame.image.load('CDI-Games-SecurityCloud/images/router.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // c.SCHIP_GROOTTE, self.image.get_height() // c.SCHIP_GROOTTE))
        self.rect = self.image.get_rect()
        self.rect.x = c.DISPLAY_WIDTH // 2 - self.rect.width // 2
        self.rect.y = c.DISPLAY_HEIGHT - self.rect.height - 10
        self.hp = 100
        self.max_hp = 100
        self.score = score  # Reference to the score

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.destroy()
        self.reduce_score(amount)

    def reduce_score(self, amount):
        damage_percentage = amount / self.max_hp
        score_reduction = 500 * damage_percentage
        self.score[0] -= score_reduction

    def destroy(self):
        self.kill()

    def draw_hp_bar(self, surface):
        # Draw the HP bar below the router
        bar_width = self.rect.width
        bar_height = 5
        fill = (self.hp / self.max_hp) * bar_width
        outline_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height + 2, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height + 2, fill, bar_height)
        pygame.draw.rect(surface, (255, 0, 0), fill_rect)
        pygame.draw.rect(surface, (255, 255, 255), outline_rect, 1)

    def update(self):
        pass