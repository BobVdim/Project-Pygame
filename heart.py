import pygame


class Heart(pygame.sprite.Sprite):
    def __init__(self, x, speed, image, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0
        self.speed = speed
        self.group = group

    def update(self, *args):
        if self.rect.y < args[0] - 58:
            self.rect.y += self.speed
        else:
            self.kill()

    def collect(self, player, health_bar):
        if player.rect.colliderect(self.rect):
            if health_bar.current_health < health_bar.max_health:
                health_bar.add_health(1)
                self.kill()
