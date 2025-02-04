import os

import pygame


def play_background_music():
    pygame.mixer.music.load(os.path.join('data', 'menu', 'sounds', 'background', 'background_music.mp3'))
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops=-1, start=0.0)
