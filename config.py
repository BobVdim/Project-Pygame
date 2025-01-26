import os

# -----Player Config---------------------


PLAYER_SIZE = {
    "width": 50,
    "height": 50,
}

PLAYER_COORDS = {
    'x': 800 // 2,
    'y': 800 - 100,
}

PLAYER_SPEED = 1

PLAYER_IMAGES_PATH = "data/player/player_images"

PLAYER_ANIMATIONS = {
    "peace": [
        os.path.join(PLAYER_IMAGES_PATH, "peace", "СТОЙКА_1.png"),
        os.path.join(PLAYER_IMAGES_PATH, "peace", "СТОЙКА_3.png"),
        os.path.join(PLAYER_IMAGES_PATH, "peace", "СТОЙКА_1.png"),
        os.path.join(PLAYER_IMAGES_PATH, "peace", "СТОЙКА_2.png"),
    ],
    "walk": [
        os.path.join(PLAYER_IMAGES_PATH, "walk", "БЕГ_1.png"),
        os.path.join(PLAYER_IMAGES_PATH, "walk", "БЕГ_2.png"),
        os.path.join(PLAYER_IMAGES_PATH, "walk", "БЕГ_3.png"),
        os.path.join(PLAYER_IMAGES_PATH, "walk", "БЕГ_4.png"),
    ],
    "damage": [
        os.path.join(PLAYER_IMAGES_PATH, "damage", "ПОЛУЧЕНИЕ_УРОНА1.png"),
        os.path.join(PLAYER_IMAGES_PATH, "damage", "ПОЛУЧЕНИЕ_УРОНА2.png"),
    ],
}

ANIMATION_SPEEDS = {
    "peace": 300,
    "damage": 150,
    "walk": 300,
}

ANIMATION_DEFAULTS = {
    "current_frame": 0,
    "animation_timer": 0,
    "direction": 'right',
}

DAMAGE_DEFAULTS = {
    'duration': 2000,
    'is_taking_damage': False,
    'damage_timer': 0,
}

INVINCIBILITY_DEFAULTS = {
    'invincibility_duration': 2000,
    'is_invincible': False,
    'invincible_timer': 0,
}

# -----Health Config---------------------


HEALTH_MAX_HEALTH = 3

HEALTH_COORDS = {
    'x': 800 - 70,
    'y': 10,
}

HEALTH_IMAGES_PATH = 'data/'

HEALTH_IMAGES = {
    "active_heart": os.path.join(HEALTH_IMAGES_PATH, "седрце_полное.png"),
    "empty_heart": os.path.join(HEALTH_IMAGES_PATH, "седрце_неполное.png"),
}

HEALTH_SCALE = 5

HEALTH_TEXT = {
    'font_size': 36,
    'text_offset': (-7, 0),
    'text_color': (255, 255, 255),
}

HEALTH_SPACING = 10

# -----Timer Config---------------------

TIMER_SPAWN = {
    'spawn_interval': 1000,
    'min_spawn_interval': 100,
    'spawn_update_interval': 10000,
    'mid_spawn_interval': 200,
    'large_decrease_step': 100,
    'small_decrease_step': 10,
}