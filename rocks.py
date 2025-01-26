import pygame


class Rock(pygame.sprite.Sprite):
    def __init__(self, x, speed, surf, group, is_big_rock=False):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = speed
        self.is_big_rock = is_big_rock

    def update(self, *args):
        if self.is_big_rock:
            if self.rect.y < args[0] - 120:
                self.rect.y += self.speed
            else:
                self.kill()

        else:
            if self.rect.y < args[0] - 58:
                self.rect.y += self.speed
            else:
                self.kill()
