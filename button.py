import pygame
import os


def load_image(name, colorkey=None):
    base_path = os.path.join('data', 'menu', 'images')
    fullname = os.path.join(base_path, name)
    if not os.path.isfile(fullname):
        raise FileNotFoundError(f"Файл с изображением '{fullname}' не найден")
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class CreateButton:
    def __init__(self, x, y, width, height, text, image, hover_image=None, sound=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

        self.image = load_image(f'buttons/{image}')
        self.image = pygame.transform.scale(self.image, (width, height))

        self.hover_image = self.image
        if hover_image:
            self.hover_image = load_image(f'buttons/{hover_image}')
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        self.is_hovered = False

        self.rect = self.image.get_rect(topleft=(x, y))

        self.sound = None
        if sound:
            self.sound = pygame.mixer.Sound(os.path.join('data', 'menu', 'sounds', 'click_sounds', sound))

    def draw_btn(self, screen):
        current_image = self.hover_image if self.is_hovered else self.image
        screen.blit(current_image, self.rect.topleft)

        font = pygame.font.Font(os.path.join('data', 'menu', 'fonts', 'pixel_font.ttf'), 30)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery - 10))
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def processing_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
