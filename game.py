import pygame
import random

from rocks import Rock
from player import Player
from health_bar import HealthBar
from timer import Timer
from menus.main_menu import main_menu
from pytmx.util_pygame import load_pygame
from tile import Tiles
import os
from button import CreateButton


FPS = 60

is_paused = False


TEMP_WIDTH = 800
TEMP_HEIGHT = 800


tmx_data = load_pygame('data/game/map/basic.tmx')

WIDTH = tmx_data.width * tmx_data.tilewidth
HEIGHT = tmx_data.height * tmx_data.tileheight

background_image = pygame.image.load(os.path.join('data/', 'game/', 'images/', 'total_bg.png'))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))


screen = pygame.display.set_mode((TEMP_WIDTH, TEMP_HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))

sprite_group = pygame.sprite.Group()

platform_rects = []

clock = pygame.time.Clock()

pause_button = CreateButton(0, 10, 100, 75, "Стоп", 'BUTTON_ON.png', 'BUTTON_ON_HOVERED.gif',
                            'button_sound_click.mp3')




for layer in tmx_data.layers:
    if hasattr(layer, 'tiles'):
        for x, y, surf in layer.tiles():
            pos = x * tmx_data.tilewidth, y * tmx_data.tileheight
            Tiles(position=pos, surface=surf, groups=(sprite_group,))
    if layer.name == 'Platform':
        for x, y, surf in layer.tiles():
            pos = x * tmx_data.tilewidth, y * tmx_data.tileheight
            platform_rect = pygame.Rect(pos[0], pos[1], tmx_data.tilewidth, tmx_data.tileheight)
            platform_rects.append(platform_rect)

damage_sound = pygame.mixer.Sound(os.path.join('data/', 'player/', 'sounds/', 'damage_sound.wav'))



def blur_surface(surface, radius=5):
    surface = pygame.transform.gaussian_blur(surface, radius)
    return surface


rocks_images = ['data/rocks/rock2.png', 'data/rocks/rock3.png']

big_rocks_images = ['data/rocks/big_rock1.png', 'data/rocks/big_rock2.png']

rocks_surface = []
for path in rocks_images + big_rocks_images:
    try:
        image = pygame.image.load(path).convert_alpha()
        rocks_surface.append(image)
    except pygame.error as e:
        print(f"Ошибка при загрузке {path}: {e}")


class Game:
    def __init__(self):
        self._timer = Timer()
        self._player = Player()
        self._health_bar = HealthBar()
        self._rocks = pygame.sprite.Group()


    def init_new_game(self):
        self._timer = Timer()
        self._player = Player()
        self._health_bar = HealthBar()
        self._rocks = pygame.sprite.Group()

    def pause_game(self):
        global is_paused
        is_paused = True
        self._timer.pause()

        blurred_bg = blur_surface(screen.copy(), radius=10)
        font = pygame.font.Font(os.path.join('data', 'menu', 'fonts', 'pixel_font.ttf'), 50)
        text_surface = font.render("Тайм-аут", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 100))

        resume_button = CreateButton(WIDTH / 2 - (252 / 2), 350, 252, 74, "Вернуться", 'BUTTON_ON.png',
                                     'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')

        menu_button = CreateButton(WIDTH / 2 - (252 / 2), 450, 252, 74, "Выйти в меню", 'BUTTON_ON.png',
                                   'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')

        while is_paused:
            screen.blit(blurred_bg, (0, 0))
            screen.blit(text_surface, text_rect)
            resume_button.draw_btn(screen)
            menu_button.draw_btn(screen)

            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                resume_button.processing_event(event)
                menu_button.processing_event(event)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if resume_button.rect.collidepoint(event.pos):
                        is_paused = False
                        self._timer.resume()
                    elif menu_button.rect.collidepoint(event.pos):
                        is_paused = False
                        main_menu(self)
                        return  # Важно! Прерываем выполнение, чтобы не продолжалась игра.

            resume_button.check_hover(mouse_pos)
            menu_button.check_hover(mouse_pos)
            resume_button.draw_btn(screen)
            menu_button.draw_btn(screen)

            pygame.display.update()
            clock.tick(FPS)

    def run_game(self):
        global is_paused
        running = True

        while running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if pause_button.rect.collidepoint(event.pos):
                        self.pause_game()

                elif event.type == pygame.USEREVENT:
                    self.createRocks(self._rocks)

            if not is_paused:
                self._timer.update_spawn_interval()

            keys = pygame.key.get_pressed()
            is_walking = False

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if self._player.rect.x > 130:
                    self._player.move(-5)
                    is_walking = True

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if self._player.rect.x + self._player.rect.width < WIDTH - 130:
                    self._player.move(5)
                    is_walking = True

            self._player.update_animation(clock.get_time(), is_walking)

            screen.blit(background_image, (0, 0))
            for layer in tmx_data.visible_layers:
                if hasattr(layer, 'tiles'):
                    for x, y, surf in layer.tiles():
                        pos = x * tmx_data.tilewidth, y * tmx_data.tileheight
                        screen.blit(surf, pos)

            self._player.draw(screen)
            self._rocks.draw(screen)
            self._rocks.update(HEIGHT)
            self.check_game_over()
            self._health_bar.draw(screen)
            self._timer.draw(screen)

            if not is_paused:
                pause_button.check_hover(mouse_pos)
                pause_button.draw_btn(screen)

            pygame.display.update()
            clock.tick(FPS)

    def check_game_over(self):
        for rock in self._rocks:
            if self._player.rect.colliderect(rock.rect):
                if not self._player.is_invincible:
                    if rock.rect.bottom > self._player.rect.top and rock.rect.bottom <= self._player.rect.top + 10:
                        if rock.is_big_rock:
                            self._health_bar.reduce_health()
                            self._health_bar.reduce_health()
                        else:
                            self._health_bar.reduce_health()

                        self._rocks.remove(rock)
                        damage_sound.play()
                        self._player.take_damage()
                        if self._health_bar.current_health == 0:
                            print("Game Over")
                            pygame.quit()
                            quit()

    def createRocks(self, group):
        is_big_rock = random.random() < 0.1

        if is_big_rock:
            image = random.choice(big_rocks_images)
            scale_factor = 5
            speed = random.randint(3, 6)
        else:
            image = random.choice(rocks_images)
            scale_factor = random.uniform(1, 1.5)
            speed = random.randint(3, 6)

        original_image = pygame.image.load(image).convert_alpha()
        new_width = int(original_image.get_width() * scale_factor)
        new_height = int(original_image.get_height() * scale_factor)
        image = pygame.transform.scale(original_image, (new_width, new_height))

        x = random.randint(130, WIDTH - 130)
        Rock(x, speed, image, group, is_big_rock)