import os

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50

PLAYER_INITIAL_X = 800 // 2
PLAYER_INITIAL_Y = 800 - 100

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

DAMAGE_DURATION = 2000
INVINCIBILITY_DURATION = 2000
