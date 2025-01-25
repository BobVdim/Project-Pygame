import pygame
import random
import os
from tile import Tiles
from pytmx.util_pygame import load_pygame
from rocks import Rock
from player import Player
from health_bar import HealthBar

BLACK = (0, 0, 0)
FPS = 60

health_count = 3

pygame.init()
pygame.display.set_caption("Game with Background and TMX Map")
clock = pygame.time.Clock()

TEMP_WIDTH = 800
TEMP_HEIGHT = 800
screen = pygame.display.set_mode((TEMP_WIDTH, TEMP_HEIGHT))

tmx_data = load_pygame('data/basic.tmx')

WIDTH = tmx_data.width * tmx_data.tilewidth
HEIGHT = tmx_data.height * tmx_data.tileheight
screen = pygame.display.set_mode((WIDTH, HEIGHT))

background_image = pygame.image.load(os.path.join('data', 'total_bg.png'))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

health_bar = HealthBar(
    max_health=3,
    x=WIDTH - 70,
    y=10,
    active_heart_image_path='data/седрце_полное.png',
    empty_heart_image_path='data/седрце_неполное.png',
    scale=5,
    font_size=36,
    text_offset=(-7, 0)
)

pygame.mixer.init()
damage_sound = pygame.mixer.Sound(os.path.join('data', 'damage_sound.wav'))

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

rocks_images = ['data/rocks.png']
rocks_surface = [pygame.image.load(path).convert_alpha() for path in rocks_images]
rocks = pygame.sprite.Group()


def createRocks(group):
    indx = random.randint(0, len(rocks_surface) - 1)
    x = random.randint(130, WIDTH - 130)
    speed = random.randint(1, 4)
    Rock(x, speed, rocks_surface[indx], group)


player = Player(x=WIDTH // 2, y=HEIGHT - 100, width=50, height=50)

pygame.time.set_timer(pygame.USEREVENT, 2000)


def check_game_over(player, rocks, health_bar):
    for rock in rocks:
        if player.rect.colliderect(rock.rect):
            if rock.rect.bottom > player.rect.top and rock.rect.bottom <= player.rect.top + 10:
                health_bar.reduce_health()
                rocks.remove(rock)
                damage_sound.play()
                if health_bar.current_health == 0:
                    print("Game Over")
                    pygame.quit()
                    quit()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.USEREVENT:
            createRocks(rocks)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        if player.rect.x > 130:
            player.move(-5)

    elif keys[pygame.K_RIGHT]:
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

    pygame.display.update()
    clock.tick(FPS)
