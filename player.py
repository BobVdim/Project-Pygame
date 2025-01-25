import pygame
import os


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width_player = width
        self.height_player = height
        self.rect = pygame.Rect(x, y, width, height)

        self.player_images_peace = {
            'peace1': pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "peace", "СТОЙКА_1.png")),
                (self.width_player, self.height_player)),
            'peace2': pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "peace", "СТОЙКА_3.png")),
                (self.width_player, self.height_player)),
            'peace3': pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "peace", "СТОЙКА_1.png")),
                (self.width_player, self.height_player)),
            'peace4': pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "peace", "СТОЙКА_2.png")),
                (self.width_player, self.height_player)),
        }

        self.player_images_walk = {
            'walk1': pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "walk", "БЕГ_1.png")),
                (self.width_player, self.height_player)),
            'walk2': pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "walk", "БЕГ_2.png")),
                (self.width_player, self.height_player)),
            'walk3': pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "walk", "БЕГ_3.png")),
                (self.width_player, self.height_player)),
            'walk4': pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "walk", "БЕГ_4.png")),
                (self.width_player, self.height_player)),
        }

        self.player_images_damage = {
            'damage1': pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "damage", "ПОЛУЧЕНИЕ_УРОНА1.png")),
                (self.width_player, self.height_player)),
            'damage2': pygame.transform.scale(
                pygame.image.load(os.path.join("data", "player", "player_images", "damage", "ПОЛУЧЕНИЕ_УРОНА2.png")),
                (self.width_player, self.height_player)),
        }

        self.animation_frames = ['peace1', 'peace2', 'peace3', 'peace4']
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 300
        self.direction = "right"

        self.is_taking_damage = False
        self.damage_timer = 0
        self.damage_animation_speed = 100
        self.damage_duration = 500

    def move(self, dx):
        self.x += dx
        self.rect.x = self.x

        if dx > 0:
            self.direction = "right"
        elif dx < 0:
            self.direction = "left"

    def take_damage(self):
        self.is_taking_damage = True
        self.damage_timer = pygame.time.get_ticks()
        self.animation_frames = ['damage1', 'damage2']
        self.current_frame = 0

    def update_animation(self, dt, is_walking):
        if self.is_taking_damage:
            self.animation_timer += dt
            if self.animation_timer >= self.damage_animation_speed:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.animation_frames)

            if pygame.time.get_ticks() - self.damage_timer > self.damage_duration:
                self.is_taking_damage = False
                self.animation_frames = ['peace1', 'peace2', 'peace3', 'peace4']
            return

        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)

        if is_walking and not self.is_taking_damage:
            self.animation_frames = ['walk1', 'walk2', 'walk3', 'walk4']
        elif not self.is_taking_damage:
            self.animation_frames = ['peace1', 'peace2', 'peace3', 'peace4']

    def get_current_image(self):
        image_key = self.animation_frames[self.current_frame]

        if image_key in self.player_images_walk:
            image = self.player_images_walk[image_key]
        elif image_key in self.player_images_damage:
            image = self.player_images_damage[image_key]
        else:
            image = self.player_images_peace[image_key]

        if self.direction == "left":
            image = pygame.transform.flip(image, True, False)

        return image

    def draw(self, screen):
        screen.blit(self.get_current_image(), self.rect)
