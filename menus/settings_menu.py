import os

import pygame

from button import CreateButton, load_image
from menus.common import main_background, SCREEN_WIDTH, screen
from sounds.background import play_background_music


def settings_menu(is_audio_btn_clicked, is_music_playing):
    audio_game_btn = CreateButton(SCREEN_WIDTH / 2 - (252 / 2), 350, 252, 74, "Звук", 'BUTTON_ON.png',
                                  'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')
    back_btn = CreateButton(SCREEN_WIDTH / 2 - (252 / 2), 450, 252, 74, "Назад", 'BUTTON_ON.png',
                            'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')

    if is_audio_btn_clicked:
        audio_game_btn.image = load_image('buttons/BUTTON_OFF.png')
        audio_game_btn.image = pygame.transform.scale(audio_game_btn.image,
                                                      (audio_game_btn.width, audio_game_btn.height))
        audio_game_btn.hover_image = load_image('buttons/BUTTON_OFF_HOVERED.gif')
        audio_game_btn.hover_image = pygame.transform.scale(audio_game_btn.hover_image,
                                                            (audio_game_btn.width, audio_game_btn.height))

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (-525, 0))

        font = pygame.font.Font(os.path.join('data', 'menu', 'fonts', 'pixel_font.ttf'), 72)
        text_surface = font.render('Настройки', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, 100))
        screen.blit(text_surface, text_rect)

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.USEREVENT and hasattr(event, 'button') and event.button == audio_game_btn:
                if not is_audio_btn_clicked:
                    is_audio_btn_clicked = True
                    audio_game_btn.image = load_image('buttons/BUTTON_OFF.png')
                    audio_game_btn.image = pygame.transform.scale(audio_game_btn.image,
                                                                  (audio_game_btn.width, audio_game_btn.height))
                    audio_game_btn.hover_image = load_image('buttons/BUTTON_OFF_HOVERED.gif')
                    audio_game_btn.hover_image = pygame.transform.scale(audio_game_btn.hover_image,
                                                                        (audio_game_btn.width, audio_game_btn.height))
                    if is_music_playing:
                        pygame.mixer.music.stop()
                        is_music_playing = False
                else:
                    is_audio_btn_clicked = False
                    audio_game_btn.image = load_image('buttons/BUTTON_ON.png')
                    audio_game_btn.image = pygame.transform.scale(audio_game_btn.image,
                                                                  (audio_game_btn.width, audio_game_btn.height))
                    audio_game_btn.hover_image = load_image('buttons/BUTTON_ON_HOVERED.gif')
                    audio_game_btn.hover_image = pygame.transform.scale(audio_game_btn.hover_image,
                                                                        (audio_game_btn.width, audio_game_btn.height))
                    if not is_music_playing:
                        play_background_music()
                        is_music_playing = True

            if event.type == pygame.USEREVENT and hasattr(event, 'button') and event.button == back_btn:
                return is_audio_btn_clicked, is_music_playing

            for btn in [audio_game_btn, back_btn]:
                btn.processing_event(event)

        for btn in [audio_game_btn, back_btn]:
            btn.check_hover(mouse_pos)
            btn.draw_btn(screen)

        pygame.display.flip()
