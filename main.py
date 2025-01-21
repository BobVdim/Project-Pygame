import pygame
import os

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
FPS = 60


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, sprite_group, scale=1, animation_speed=10):
        super().__init__(sprite_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows, scale)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.animation_speed = animation_speed
        self.animation_counter = 0

    def cut_sheet(self, sheet, columns, rows, scale):
        frame_width = sheet.get_width() // columns
        frame_height = sheet.get_height() // rows
        for j in range(rows):
            for i in range(columns):
                frame_location = (frame_width * i, frame_height * j)
                frame = sheet.subsurface(pygame.Rect(frame_location, (frame_width, frame_height)))
                if scale != 1:
                    frame = pygame.transform.scale(frame, (int(frame_width * scale), int(frame_height * scale)))
                self.frames.append(frame)

    def update(self):
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.animation_counter = 0


class Player:
    scale = 5
    height = 12 * scale
    width = 5 * scale

    x = SCREEN_WIDTH / 2 - width / 2
    y = SCREEN_HEIGHT - height

    maxSpeed = 5
    maxFallSpeed = 15
    acceleration = 0.5  # и замедление тоже

    def __init__(self):
        pass


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
clock = pygame.time.Clock()
pygame.display.set_caption('Wall Jumper')
main_background = load_image('bg_main_menu.png')


def main_menu():
    start_game_btn = CreateButton(SCREEN_WIDTH / 2 - (252 / 2), 350, 252, 74, "Новая игра", 'BUTTON_ON.png',
                                  'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')
    settings_game_btn = CreateButton(SCREEN_WIDTH / 2 - (252 / 2), 450, 252, 74, "Настройки", 'BUTTON_ON.png',
                                     'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')
    exit_game_btn = CreateButton(SCREEN_WIDTH / 2 - (252 / 2), 550, 252, 74, "Выйти", 'BUTTON_ON.png',
                                 'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')

    is_audio_btn_clicked = False

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

            if event.type == pygame.USEREVENT and event.button == start_game_btn:
                game_screen()

            if event.type == pygame.USEREVENT and event.button == settings_game_btn:
                is_audio_btn_clicked = settings_menu(is_audio_btn_clicked)

            if event.type == pygame.USEREVENT and event.button == exit_game_btn:
                running = False

            for btn in [start_game_btn, settings_game_btn, exit_game_btn]:
                btn.processing_event(event)

        for btn in [start_game_btn, settings_game_btn, exit_game_btn]:
            btn.check_hover(mouse_pos)
            btn.draw_btn(screen)

        pygame.display.flip()

    pygame.quit()


def settings_menu(is_audio_btn_clicked):
    audio_game_btn = CreateButton(SCREEN_WIDTH / 2 - (252 / 2), 350, 252, 74, "Звук", 'BUTTON_ON.png',
                                  'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')
    back_btn = CreateButton(SCREEN_WIDTH / 2 - (252 / 2), 450, 252, 74, "Назад", 'BUTTON_ON.png',
                            'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')

    if is_audio_btn_clicked:
        audio_game_btn.image = load_image('BUTTON_OFF.png')
        audio_game_btn.image = pygame.transform.scale(audio_game_btn.image,
                                                      (audio_game_btn.width, audio_game_btn.height))
        audio_game_btn.hover_image = load_image('BUTTON_OFF_HOVERED.gif')
        audio_game_btn.hover_image = pygame.transform.scale(audio_game_btn.hover_image,
                                                            (audio_game_btn.width, audio_game_btn.height))

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

            if event.type == pygame.USEREVENT and event.button == audio_game_btn:
                if not is_audio_btn_clicked:
                    is_audio_btn_clicked = True
                    audio_game_btn.image = load_image('BUTTON_OFF.png')
                    audio_game_btn.image = pygame.transform.scale(audio_game_btn.image,
                                                                  (audio_game_btn.width, audio_game_btn.height))
                    audio_game_btn.hover_image = load_image('BUTTON_OFF_HOVERED.gif')
                    audio_game_btn.hover_image = pygame.transform.scale(audio_game_btn.hover_image,
                                                                        (audio_game_btn.width, audio_game_btn.height))
                else:
                    is_audio_btn_clicked = False
                    audio_game_btn.image = load_image('BUTTON_ON.png')
                    audio_game_btn.image = pygame.transform.scale(audio_game_btn.image,
                                                                  (audio_game_btn.width, audio_game_btn.height))
                    audio_game_btn.hover_image = load_image('BUTTON_ON_HOVERED.gif')
                    audio_game_btn.hover_image = pygame.transform.scale(audio_game_btn.hover_image,
                                                                        (audio_game_btn.width, audio_game_btn.height))

            if event.type == pygame.USEREVENT and event.button == back_btn:
                return is_audio_btn_clicked

            for btn in [audio_game_btn, back_btn]:
                btn.processing_event(event)

        for btn in [audio_game_btn, back_btn]:
            btn.check_hover(mouse_pos)
            btn.draw_btn(screen)

        pygame.display.flip()


def game_screen():
    left_side = (0, 0, SCREEN_HEIGHT, 'left')
    right_side = (SCREEN_WIDTH, 0, SCREEN_HEIGHT, 'right')

    walls = [left_side, right_side]
    ground = (0, SCREEN_WIDTH, SCREEN_HEIGHT)

    platforms = [ground]

    all_sprite = pygame.sprite.Group()

    player = AnimatedSprite(load_image('hero_cat_run.png'), 10, 1, 50, 50, all_sprite, scale=5, animation_speed=250)

    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        all_sprite.update()

        all_sprite.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main_menu()
