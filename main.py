import pygame
import os

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800


class CreateButton:
    def __init__(self, x, y, width, height, text, image, hover_image=None, sound=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

        self.image = load_image(image)
        self.image = pygame.transform.scale(self.image, (width, height))

        self.hover_image = self.image
        if hover_image:
            self.hover_image = load_image(hover_image)
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        self.is_hovered = False

        self.rect = self.image.get_rect(topleft=(x, y))

        self.sound = None
        if sound:
            self.sound = pygame.mixer.Sound(os.path.join('data', sound))

    def draw_btn(self, screen):
        if self.is_hovered:
            current_image = self.hover_image
        else:
            current_image = self.image

        screen.blit(current_image, self.rect.topleft)

        font = pygame.font.Font(os.path.join('data', 'pixel_font.ttf'), 30)
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


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Wall Jumper')
main_background = load_image('bg_main_menu.png')


def main_menu():
    start_game_btn = CreateButton(SCREEN_WIDTH / 2 - (252 / 2), 350, 252, 74, "Новая игра", 'BUTTON_ON.png',
                                  'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')
    settings_game_btn = CreateButton(SCREEN_WIDTH / 2 - (252 / 2), 450, 252, 74, "Настройки", 'BUTTON_ON.png',
                                     'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')
    exit_game_btn = CreateButton(SCREEN_WIDTH / 2 - (252 / 2), 550, 252, 74, "Выйти", 'BUTTON_ON.png',
                                 'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (-525, 0))

        font = pygame.font.Font(os.path.join('data', 'pixel_font.ttf'), 72)
        text_surface = font.render('Wall Jumper', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, 100))
        screen.blit(text_surface, text_rect)

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT and event.button == settings_game_btn:
                settings_menu()

            if event.type == pygame.USEREVENT and event.button == exit_game_btn:
                running = False

            for btn in [start_game_btn, settings_game_btn, exit_game_btn]:
                btn.processing_event(event)

        for btn in [start_game_btn, settings_game_btn, exit_game_btn]:
            btn.check_hover(mouse_pos)
            btn.draw_btn(screen)

        pygame.display.flip()

    pygame.quit()


def settings_menu():
    audio_game_btn = CreateButton(SCREEN_WIDTH / 2 - (252 / 2), 350, 252, 74, "Звук", 'BUTTON_ON.png',
                                  'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')
    back_btn = CreateButton(SCREEN_WIDTH / 2 - (252 / 2), 450, 252, 74, "Назад", 'BUTTON_ON.png',
                            'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (-525, 0))

        font = pygame.font.Font(os.path.join('data', 'pixel_font.ttf'), 72)
        text_surface = font.render('Настройки', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, 100))
        screen.blit(text_surface, text_rect)

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.USEREVENT and event.button == back_btn:
                return

            for btn in [audio_game_btn, back_btn]:
                btn.processing_event(event)

        for btn in [audio_game_btn, back_btn]:
            btn.check_hover(mouse_pos)
            btn.draw_btn(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main_menu()
