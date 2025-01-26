import pygame


class Rock(pygame.sprite.Sprite):
    def __init__(self, x, speed, surf, group):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = speed

    def update(self, *args):
        if self.rect.y < args[0] - 58:
            self.rect.y += self.speed
        else:
            self.kill()
