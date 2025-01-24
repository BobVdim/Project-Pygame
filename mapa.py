import pygame
from pytmx.util_pygame import load_pygame

WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)


class Tiles(pygame.sprite.Sprite):
    def __init__(self, position, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TMX Loader Example")
clock = pygame.time.Clock()

tmx_data = load_pygame('data/basic.tmx')

WIDTH = tmx_data.width * tmx_data.tilewidth
HEIGHT = tmx_data.height * tmx_data.tileheight
screen = pygame.display.set_mode((WIDTH, HEIGHT))
print(WIDTH, HEIGHT)

sprite_group = pygame.sprite.Group()

wall_rects = []

for layer in tmx_data.layers:
    if hasattr(layer, 'tiles'):
        for x, y, surf in layer.tiles():
            if layer.name == 'Walls':
                pos = x * tmx_data.tilewidth, y * tmx_data.tileheight
                rect = pygame.Rect(pos, (tmx_data.tilewidth, tmx_data.tileheight))
                wall_rects.append(rect)
                Tiles(position=pos, surface=surf, groups=(sprite_group,))

print("Все стены:")
for rect in wall_rects:
    print(f"Стена на позиции: {rect.topleft}, Размер: {rect.size}")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    sprite_group.draw(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
