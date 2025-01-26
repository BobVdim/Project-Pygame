import pygame
import config


class Player:
    def __init__(self):
        self.x = config.PLAYER_INITIAL_X
        self.y = config.PLAYER_INITIAL_Y

        self.width_player = config.PLAYER_WIDTH
        self.height_player = config.PLAYER_HEIGHT
        self.rect = pygame.Rect(self.x, self.y, self.width_player, self.height_player)

        self.player_images_peace = [
            pygame.transform.scale(pygame.image.load(img), (self.width_player, self.height_player))
            for img in config.PLAYER_ANIMATIONS["peace"]
        ]
        self.player_images_walk = [
            pygame.transform.scale(pygame.image.load(img), (self.width_player, self.height_player))
            for img in config.PLAYER_ANIMATIONS["walk"]
        ]
        self.player_images_damage = [
            pygame.transform.scale(pygame.image.load(img), (self.width_player, self.height_player))
            for img in config.PLAYER_ANIMATIONS["damage"]
        ]

        self.animation_frames = self.player_images_peace
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = config.ANIMATION_SPEEDS["peace"]
        self.direction = "right"

        self.is_taking_damage = False
        self.damage_timer = 0
        self.damage_animation_speed = config.ANIMATION_SPEEDS["damage"]
        self.damage_duration = config.DAMAGE_DURATION

        self.is_invincible = False
        self.invincible_timer = 0
        self.invincible_duration = config.INVINCIBILITY_DURATION

    def move(self, dx):
        self.x += dx * config.PLAYER_SPEED
        self.rect.x = self.x

        if dx > 0:
            self.direction = "right"
        elif dx < 0:
            self.direction = "left"

    def take_damage(self):
        if not self.is_invincible:
            self.is_taking_damage = True
            self.damage_timer = pygame.time.get_ticks()
            self.animation_frames = self.player_images_damage
            self.current_frame = 0
            self.is_invincible = True
            self.invincible_timer = pygame.time.get_ticks()

    def update_invincibility(self):
        if self.is_invincible and pygame.time.get_ticks() - self.invincible_timer >= self.invincible_duration:
            self.is_invincible = False

    def update_animation(self, dt, is_walking):
        self.update_invincibility()
        if self.is_taking_damage:
            self.animation_timer += dt
            if self.animation_timer >= self.damage_animation_speed:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.animation_frames)

            if pygame.time.get_ticks() - self.damage_timer > self.damage_duration:
                self.is_taking_damage = False
                self.animation_frames = self.player_images_peace
            return

        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)

        if is_walking and not self.is_taking_damage:
            self.animation_frames = self.player_images_walk
        elif not self.is_taking_damage:
            self.animation_frames = self.player_images_peace

    def get_current_image(self):
        image = self.animation_frames[self.current_frame]

        if self.direction == "left":
            image = pygame.transform.flip(image, True, False)

        return image

    def draw(self, screen):
        screen.blit(self.get_current_image(), self.rect)
