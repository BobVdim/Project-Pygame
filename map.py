import pygame
import random
import os
from tile import Tiles
from pytmx.util_pygame import load_pygame
from rocks import Rock
from player import Player
from health_bar import HealthBar
from timer import Timer

BLACK = (0, 0, 0)
FPS = 60

pygame.init()
pygame.display.set_caption("Cave Game")
clock = pygame.time.Clock()

TEMP_WIDTH = 800
TEMP_HEIGHT = 800
screen = pygame.display.set_mode((TEMP_WIDTH, TEMP_HEIGHT))

tmx_data = load_pygame('data/game/map/basic.tmx')

WIDTH = tmx_data.width * tmx_data.tilewidth
HEIGHT = tmx_data.height * tmx_data.tileheight
screen = pygame.display.set_mode((WIDTH, HEIGHT))

background_image = pygame.image.load(os.path.join('data/', 'game/', 'images/', 'total_bg.png'))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

health_bar = HealthBar()

pygame.mixer.init()
damage_sound = pygame.mixer.Sound(os.path.join('data/', 'player/', 'sounds/', 'damage_sound.wav'))

sprite_group = pygame.sprite.Group()
platform_rects = []

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

rocks_images = ['data/rocks/rock2.png', 'data/rocks/rock3.png']
big_rocks_images = ['data/rocks/big_rock1.png', 'data/rocks/big_rock2.png']

rocks_surface = []
for path in rocks_images + big_rocks_images:
    try:
        image = pygame.image.load(path).convert_alpha()
        rocks_surface.append(image)
    except pygame.error as e:
        print(f"Ошибка при загрузке {path}: {e}")

rocks = pygame.sprite.Group()


def createRocks(group):
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


player = Player()


def check_game_over(player, rocks, health_bar):
    for rock in rocks:
        if player.rect.colliderect(rock.rect):
            if not player.is_invincible:
                if rock.rect.bottom > player.rect.top and rock.rect.bottom <= player.rect.top + 10:
                    if rock.is_big_rock:
                        health_bar.reduce_health()
                        health_bar.reduce_health()
                    else:
                        health_bar.reduce_health()

                    rocks.remove(rock)
                    damage_sound.play()
                    player.take_damage()
                    if health_bar.current_health == 0:
                        print("Game Over")
                        pygame.quit()
                        quit()


timer = Timer()


def run_game():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.USEREVENT:
                createRocks(rocks)

        timer.update_spawn_interval()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if player.rect.x > 130:
                player.move(-5)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if player.rect.x + player.rect.width < WIDTH - 130:
                player.move(5)

        player.update_animation(clock.get_time(), keys[pygame.K_LEFT] or keys[pygame.K_RIGHT])

        screen.blit(background_image, (0, 0))
        for layer in tmx_data.visible_layers:
            if hasattr(layer, 'tiles'):
                for x, y, surf in layer.tiles():
                    pos = x * tmx_data.tilewidth, y * tmx_data.tileheight
                    screen.blit(surf, pos)

        player.draw(screen)
        rocks.draw(screen)
        rocks.update(HEIGHT)
        check_game_over(player, rocks, health_bar)
        health_bar.draw(screen)
        timer.draw(screen)

        pygame.display.update()
        clock.tick(FPS)
