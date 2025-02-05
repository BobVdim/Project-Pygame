import pygame
import os
import config


class HealthBar:
    def __init__(self):
        if config.DIFFICULTY_MOD == 'mega_hard':
            self.current_health = 1
            self.max_health = 1

        else:
            self.current_health = config.HEALTH_MAX_HEALTH
            self.max_health = config.HEALTH_MAX_HEALTH

        self.x = config.HEALTH_COORDS['x']
        self.y = config.HEALTH_COORDS['y']

        self.scale = config.HEALTH_SCALE

        pygame.font.init()
        self.font_size = config.HEALTH_TEXT['font_size']
        self.font = pygame.font.Font(os.path.join('data', 'menu', 'fonts', 'pixel_font.ttf'), self.font_size)
        self.text_color = config.HEALTH_TEXT['text_color']
        self.text_offset = config.HEALTH_TEXT['text_offset']

        active_image = pygame.image.load(config.HEALTH_IMAGES['active_heart']).convert_alpha()
        empty_image = pygame.image.load(config.HEALTH_IMAGES['empty_heart']).convert_alpha()

        self.active_heart_image = pygame.transform.scale(
            active_image,
            (int(active_image.get_width() * self.scale), int(active_image.get_height() * self.scale))
        )
        self.empty_heart_image = pygame.transform.scale(
            empty_image,
            (int(empty_image.get_width() * self.scale), int(empty_image.get_height() * self.scale))
        )

        self.heart_width = self.active_heart_image.get_width()
        self.heart_height = self.active_heart_image.get_height()

        self.spacing = config.HEALTH_SPACING

    def draw(self, surface):
        text = f"{self.current_health}/{self.max_health}"
        text_surface = self.font.render(text, True, self.text_color)

        text_x = self.x + self.text_offset[0]
        text_y = self.y + self.text_offset[1]

        surface.blit(text_surface, (text_x, text_y))

        y_offset = text_y + text_surface.get_height() + self.spacing
        for i in range(self.max_health):
            if i < self.current_health:
                surface.blit(self.active_heart_image, (self.x, y_offset))
            else:
                surface.blit(self.empty_heart_image, (self.x, y_offset))

            y_offset += self.heart_height + self.spacing

    def reduce_health(self):
        if self.current_health > 0:
            self.current_health -= 1

    def add_health(self, amount=1):
        if self.current_health < self.max_health:
            self.current_health += amount
