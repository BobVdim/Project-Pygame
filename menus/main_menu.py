import pygame
import os
import config
from button import CreateButton
from menus.common import screen, SCREEN_WIDTH, SCREEN_HEIGHT
from menus.settings_menu import settings_menu
from sounds.background import play_background_music
from menus.common import main_background
from menus.score_menu import score_menu

FPS = 60

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Cave Game')


def show_intro_screen():
    intro_font = pygame.font.Font(os.path.join('data', 'menu', 'fonts', 'pixel_font.ttf'), 72)

    running = True
    start_ticks = pygame.time.get_ticks()
    color_change_time = start_ticks
    current_color = (255, 255, 255)

    while running:
        screen.fill((0, 0, 0))

        if pygame.time.get_ticks() - color_change_time >= 1000:
            current_color = (255, 255, 0) if current_color == (255, 255, 255) else (255, 255, 255)
            color_change_time = pygame.time.get_ticks()

        text_surface = intro_font.render('Cave Game', True, current_color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(text_surface, text_rect)

        pygame.display.flip()

        if pygame.time.get_ticks() - start_ticks >= 1500:
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()


def main_menu(game):
    play_background_music()
    start_game_btn = CreateButton(SCREEN_WIDTH / 2 - (252 / 2), 300, 252, 74, "Новая игра", 'BUTTON_ON.png',
                                  'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')
    settings_game_btn = CreateButton(SCREEN_WIDTH / 2 - (252 / 2), 400, 252, 74, "Настройки", 'BUTTON_ON.png',
                                     'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')
    best_score_btn = CreateButton(SCREEN_WIDTH / 2 - (252 / 2), 500, 252, 74, "Статистика", 'BUTTON_ON.png',
                                  'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')
    exit_game_btn = CreateButton(SCREEN_WIDTH / 2 - (252 / 2), 650, 252, 74, "Выйти", 'BUTTON_ON.png',
                                 'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (-525, 0))

        font = pygame.font.Font(os.path.join('data', 'menu', 'fonts', 'pixel_font.ttf'), 72)
        text_surface = font.render('Cave Game', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, 100))
        screen.blit(text_surface, text_rect)

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT and hasattr(event, 'button') and event.button == start_game_btn:
                game_screen(game)

            if event.type == pygame.USEREVENT and hasattr(event, 'button') and event.button == settings_game_btn:
                settings_menu(main_background, -525)

            if event.type == pygame.USEREVENT and hasattr(event, 'button') and event.button == best_score_btn:
                score_menu(main_background, -525)

            if event.type == pygame.USEREVENT and hasattr(event, 'button') and event.button == exit_game_btn:
                running = False

            for btn in [start_game_btn, settings_game_btn, exit_game_btn, best_score_btn]:
                btn.processing_event(event)

        for btn in [start_game_btn, settings_game_btn, exit_game_btn, best_score_btn]:
            btn.check_hover(mouse_pos)
            btn.draw_btn(screen)

        pygame.display.flip()

    pygame.quit()


def launch_game(game):
    game.init_new_game()
    game.run_game()


def game_screen(game):
    easy_mod_btn = CreateButton(274, 300, 252, 74, "Легкий", 'BUTTON_ON.png',
                                'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')
    mid_mod_btn = CreateButton(274, 400, 252, 74, "Средний", 'BUTTON_ON.png',
                               'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')
    hard_mod_btn = CreateButton(274, 500, 252, 74, "Сложный", 'BUTTON_ON.png',
                                'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')
    back_btn = CreateButton(SCREEN_WIDTH / 2 - (252 / 2), 650, 252, 74, "Назад", 'BUTTON_ON.png',
                            'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (-525, 0))

        font = pygame.font.Font(os.path.join('data', 'menu', 'fonts', 'pixel_font.ttf'), 72)
        text_surface = font.render('Режим', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, 100))
        screen.blit(text_surface, text_rect)

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            for btn in [easy_mod_btn, mid_mod_btn, hard_mod_btn, back_btn]:
                btn.processing_event(event)

            if event.type == pygame.USEREVENT and hasattr(event, 'button'):
                if event.button == easy_mod_btn:
                    config.DIFFICULTY_MOD = 'easy'
                    show_intro_screen()
                    launch_game(game)
                    return
                elif event.button == mid_mod_btn:
                    config.DIFFICULTY_MOD = 'medium'
                    show_intro_screen()
                    launch_game(game)
                    return
                elif event.button == hard_mod_btn:
                    config.DIFFICULTY_MOD = 'hard'
                    show_intro_screen()
                    launch_game(game)
                    return
                elif event.button == back_btn:
                    return

        for btn in [easy_mod_btn, mid_mod_btn, hard_mod_btn, back_btn]:
            btn.check_hover(mouse_pos)
            btn.draw_btn(screen)

        pygame.display.flip()
