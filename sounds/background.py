import pygame


def play_background_music(music_path=None):
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops=-1, start=0.0)

    if pygame.mixer.music.get_busy():
        print("Музыка играет")
    else:
        print("Музыка не играет")
