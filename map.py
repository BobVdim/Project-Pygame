import pygame
import random
import os
from tile import Tiles
from pytmx.util_pygame import load_pygame
from rocks import Rock
from player import Player

BLACK = (0, 0, 0)
FPS = 60

pygame.init()
pygame.display.set_caption("Game with Background and TMX Map")
clock = pygame.time.Clock()

TEMP_WIDTH = 800
TEMP_HEIGHT = 600
screen = pygame.display.set_mode((TEMP_WIDTH, TEMP_HEIGHT))

tmx_data = load_pygame('data/basic.tmx')

WIDTH = tmx_data.width * tmx_data.tilewidth
HEIGHT = tmx_data.height * tmx_data.tileheight
screen = pygame.display.set_mode((WIDTH, HEIGHT))

background_image = pygame.image.load(os.path.join('data', 'total_bg.png'))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

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


player = Player(x=WIDTH//2, y=HEIGHT-100, width=50, height=50)

pygame.time.set_timer(pygame.USEREVENT, 2000)


def check_platform_collision(player_rect, platforms):
    for platform in platforms:
        if player_rect.colliderect(platform):
            return True
    return False


falling_speed = 0
on_ground = False

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
        player.move(-5)
    elif keys[pygame.K_RIGHT]:
        player.move(5)

    player.rect.y += falling_speed

    if not check_platform_collision(player.rect, platform_rects):
        falling_speed += 1  # Если нет коллизии с платформами, увеличиваем скорость падения
        on_ground = False  # Персонаж в воздухе
    else:
        falling_speed = 0  # Останавливаем падение
        on_ground = True  # Персонаж на земле

    # Обновление анимации персонажа
    player.update_animation(clock.get_time(), keys[pygame.K_LEFT] or keys[pygame.K_RIGHT])

    # Отображение фона
    screen.blit(background_image, (0, 0))

    # Отображение тайлов
    for layer in tmx_data.visible_layers:
        if hasattr(layer, 'tiles'):
            for x, y, surf in layer.tiles():
                pos = x * tmx_data.tilewidth, y * tmx_data.tileheight
                screen.blit(surf, pos)

    # Отображение персонажа
    player.draw(screen)

    # Отображение камней
    rocks.draw(screen)
    rocks.update(HEIGHT)

    # Обновление экрана
    pygame.display.update()
    clock.tick(FPS)
