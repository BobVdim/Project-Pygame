import os
import pygame
from button import CreateButton
from menus.common import SCREEN_WIDTH, screen
import csv
from score_manager import load_best_times


def get_best_time():
    best_times = load_best_times()
    return best_times


import math


def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes} мин {seconds} сек"


def score_menu(bg, sdvig):
    back_btn = CreateButton(SCREEN_WIDTH / 2 - (252 / 2), 650, 252, 74, "Назад",
                            'BUTTON_ON.png', 'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')

    running = True
    best_time = get_best_time()

    while running:
        screen.fill((0, 0, 0))
        screen.blit(bg, (sdvig, 0))

        font = pygame.font.Font(os.path.join('data', 'menu', 'fonts', 'pixel_font.ttf'), 72)
        text_surface = font.render('Лучшее время', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, 100))
        screen.blit(text_surface, text_rect)

        best_times = get_best_time()
        time_font = pygame.font.Font(os.path.join('data', 'menu', 'fonts', 'pixel_font.ttf'), 50)

        time_easy = time_font.render(f'1)Лёгкий: {format_time(best_times["Лёгкий"])}', True, (255, 255, 255))
        time_medium = time_font.render(f'2)Средний: {format_time(best_times["Средний"])}', True, (255, 255, 255))
        time_hard = time_font.render(f'3)Сложный: {format_time(best_times["Сложный"])}', True, (255, 255, 255))
        time_hardcore = time_font.render(f'4)Хардкор: {format_time(best_times["Хардкор"])}', True, (255, 255, 255))

        screen.blit(time_easy, (SCREEN_WIDTH / 6, 200))
        screen.blit(time_medium, (SCREEN_WIDTH / 6, 300))
        screen.blit(time_hard, (SCREEN_WIDTH / 6, 400))
        screen.blit(time_hardcore, (SCREEN_WIDTH / 6, 500))

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.USEREVENT and hasattr(event, 'button') and event.button == back_btn:
                return

            for btn in [back_btn]:
                btn.processing_event(event)

        for btn in [back_btn]:
            btn.check_hover(mouse_pos)
            btn.draw_btn(screen)

        pygame.display.flip()
