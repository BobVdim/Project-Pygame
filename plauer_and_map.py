import pygame
import os
from pytmx.util_pygame import load_pygame

WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)


class Player:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = 800, 800

        self.width_player = 40
        self.height_player = 50

        self.FPS = 60

        self.GRAVITY = 0.5

        self.JUMP_FORCE = -15
        self.WALL_JUMP_UPWARD_FORCE = -15

        self.WALL_SLIDE_SPEED = 0.1

        self.WALL_PUSH_SPEED = 4

        self.FRICTION = 0.95

        self.x, self.y = self.WIDTH // 2, self.HEIGHT - 40

        self.speed_x, self.speed_y = 0, 0

        self.on_ground = False
        self.on_wall = False

        self.wall_push_direction = 0
        self.push_counter = 0
        self.wall_jump_counter = 0

        self.player_images = {
            'peace1': pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "peace", "СТОЙКА_1.png")),
                (self.width_player, self.height_player)),
            'peace1_pere': pygame.transform.scale(pygame.image.load(
                os.path.join("data", "player", "player_images", "peace", "СТОЙКА_1_ПЕРЕ.png")),
                (self.width_player, self.height_player)),
            'peace2': pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "peace", "СТОЙКА_3.png")),
                (self.width_player, self.height_player)),
            'peace2_pere': pygame.transform.scale(pygame.image.load(
                os.path.join("data", "player", "player_images", "peace", "СТОЙКА_3_ПЕРЕ.png")),
                (self.width_player, self.height_player)),
            'peace3': pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "peace", "СТОЙКА_1.png")),
                (self.width_player, self.height_player)),
            'peace3_pere': pygame.transform.scale(pygame.image.load(
                os.path.join("data", "player", "player_images", "peace", "СТОЙКА_1_ПЕРЕ.png")),
                (self.width_player, self.height_player)),
            'peace4': pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "peace", "СТОЙКА_2.png")),
                (self.width_player, self.height_player)),
            'peace4_pere': pygame.transform.scale(pygame.image.load(
                os.path.join("data", "player", "player_images", "peace", "СТОЙКА_2_ПЕРЕ.png")),
                (self.width_player, self.height_player)),

            'on_wall1': pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "on_wall", "НА_СТЕНЕ_1.png")),
                (self.width_player, self.height_player - 20)), 90),
            'on_wall1_pere': pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
                os.path.join("data", "player", "player_images", "on_wall", "НА_СТЕНЕ_1_ПЕРЕ.png")),
                (self.width_player, self.height_player - 20)), -90),
            'on_wall2': pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "on_wall", "НА_СТЕНЕ_2.png")),
                (self.width_player, self.height_player - 20)), 90),
            'on_wall2_pere': pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
                os.path.join("data", "player", "player_images", "on_wall", "НА_СТЕНЕ_2_ПЕРЕ.png")),
                (self.width_player, self.height_player - 20)), -90),
            'on_wall3': pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "on_wall", "НА_СТЕНЕ_3.png")),
                (self.width_player, self.height_player - 20)), 90),
            'on_wall3_pere': pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
                os.path.join("data", "player", "player_images", "on_wall", "НА_СТЕНЕ_3_ПЕРЕ.png")),
                (self.width_player, self.height_player - 20)), -90),

            'push1': pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "push", "ПОЛЁТ_1_ПЕРЕ.png")),
                (self.width_player + 10, self.height_player + 10)),
            'push1_pere': pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "push", "ПОЛЁТ_1.png")),
                (self.width_player + 10, self.height_player + 10)),
            'push2': pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "push", "ПОЛЁТ_2_ПЕРЕ.png")),
                (self.width_player + 10, self.height_player + 10)),
            'push2_pere': pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "push", "ПОЛЁТ_2.png")),
                (self.width_player + 10, self.height_player + 10)),
            'push3': pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "push", "ПОЛЁТ_3_ПЕРЕ.png")),
                (self.width_player + 10, self.height_player + 10)),
            'push3_pere': pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "push", "ПОЛЁТ_3.png")),
                (self.width_player + 10, self.height_player + 10)),
            'push4': pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "push", "ПОЛЁТ_4_ПЕРЕ.png")),
                (self.width_player + 10, self.height_player + 10)),
            'push4_pere': pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "push", "ПОЛЁТ_4.png")),
                (self.width_player + 10, self.height_player + 10)),
        }

        self.current_frame = 'peace1'
        self.frame_counter = 0

    def handle_events(self):
        if self.on_ground:
            self.speed_y = self.JUMP_FORCE
            self.on_ground = False

        elif self.on_wall and self.push_counter == 0:
            print(f"Отталкивание от стены! Текущие координаты X: {self.x}")
            self.push_counter = 1
            self.speed_y = self.WALL_JUMP_UPWARD_FORCE
            self.speed_x = self.WALL_PUSH_SPEED * self.wall_push_direction
            self.on_wall = False
            self.wall_jump_counter = 1

        elif 0 < self.wall_jump_counter <= 15:
            print(f"Отталкивание в сторону стены! Текущие координаты X: {self.x}")
            self.speed_y = self.WALL_JUMP_UPWARD_FORCE
            self.speed_x = -self.WALL_PUSH_SPEED * self.wall_push_direction
            self.wall_jump_counter = 0

    def update(self):
        self.update_physics()
        self.update_animation()

    def gravity_and_verticalmovement(self):
        self.speed_y += self.GRAVITY
        self.y += self.speed_y

    def check_ground_collision(self):
        if self.y + self.height_player >= self.HEIGHT:
            self.y = self.HEIGHT - self.height_player
            self.speed_y = 0
            self.on_ground = True
            self.speed_x = 0

    def check_wall_collision(self):
        self.on_wall = False
        if self.x <= 0 or self.x + self.width_player >= self.WIDTH:
            if self.push_counter == 0:
                self.on_wall = True
                self.speed_y = min(self.speed_y, int(self.WALL_SLIDE_SPEED))

    def handle_wall_push(self):
        if self.push_counter > 0:
            self.x += self.WALL_PUSH_SPEED * self.wall_push_direction
            self.push_counter += 1

            if self.push_counter > 15:
                self.push_counter = 0

    def handle_horizontal_movement(self):
        if self.push_counter == 0 and not self.on_ground:
            self.x += self.speed_x
            self.speed_y *= 0.98

    def check_edge_wall(self):
        if self.push_counter == 0:
            if self.x <= 0:
                self.on_wall = True
                self.wall_push_direction = 1
            elif self.x + 30 >= self.WIDTH:
                self.on_wall = True
                self.wall_push_direction = -1

    def handle_keyboard_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= 5
        if keys[pygame.K_d]:
            self.x += 5

    def check_bounds(self):
        if self.x < 0:
            self.x = 0
        if self.x + 30 > self.WIDTH:
            self.x = self.WIDTH - 30

    def update_physics(self):
        self.gravity_and_verticalmovement()
        self.check_ground_collision()
        self.check_wall_collision()
        self.handle_wall_push()
        self.handle_horizontal_movement()
        self.check_edge_wall()
        self.handle_keyboard_input()
        self.check_bounds()

    def update_frames(self, frames, fps_divisor):
        self.frame_counter += 1
        if self.frame_counter >= self.FPS // fps_divisor:
            if self.current_frame not in frames:
                self.current_frame = frames[0]

            current_index = frames.index(self.current_frame)
            next_index = (current_index + 1) % len(frames)
            self.current_frame = frames[next_index]
            self.frame_counter = 0

    def update_animation(self):
        if self.x < self.WIDTH // 2:
            side = "_pere"
        else:
            side = ""

        if self.on_ground:
            frames = [f'peace1{side}', f'peace2{side}', f'peace3{side}', f'peace4{side}']
            self.update_frames(frames, fps_divisor=4)

        elif self.on_wall:
            frames = [f'on_wall1{side}', f'on_wall2{side}', f'on_wall3{side}']
            self.update_frames(frames, fps_divisor=4)

        elif self.wall_jump_counter > 0:
            if self.wall_push_direction == 1:
                frames = [f'push1_pere', f'push2_pere', f'push3_pere', f'push4_pere']
            else:
                frames = [f'push1', f'push2', f'push3', f'push4']
            self.update_frames(frames, fps_divisor=8)

        elif not self.on_ground and not self.on_wall:
            if self.x < self.WIDTH // 2:
                side = ""
            else:
                side = "_pere"
            frames = [f'push1{side}', f'push2{side}', f'push3{side}', f'push4{side}']
            self.update_frames(frames, fps_divisor=8)


# Класс для Tiles
class Tiles(pygame.sprite.Sprite):
    def __init__(self, position, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)


# Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TMX Loader Example")
clock = pygame.time.Clock()

# Загрузка карты
tmx_data = load_pygame('data/basic.tmx')

WIDTH = tmx_data.width * tmx_data.tilewidth
HEIGHT = tmx_data.height * tmx_data.tileheight
screen = pygame.display.set_mode((WIDTH, HEIGHT))
print(WIDTH, HEIGHT)

sprite_group = pygame.sprite.Group()

for layer in tmx_data.layers:
    if hasattr(layer, 'tiles'):
        for x, y, surf in layer.tiles():
            pos = x * tmx_data.tilewidth, y * tmx_data.tileheight
            Tiles(position=pos, surface=surf, groups=(sprite_group,))

player = Player()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.handle_events()

    player.update()

    screen.fill(WHITE)
    sprite_group.draw(screen)

    player_frame = player.player_images[player.current_frame]
    screen.blit(player_frame, (player.x, player.y))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
