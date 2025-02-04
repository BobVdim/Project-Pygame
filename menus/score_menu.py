import os
import pygame
from button import CreateButton
from menus.common import SCREEN_WIDTH, screen
import csv


def get_best_time():
    filename = "score.csv"
    if os.path.exists(filename):
        with open(filename, "r", newline="") as file:
            reader = csv.reader(file)
            times = list(reader)
            if times:
                return float(times[0][0])
    return 0


def score_menu(bg, sdvig):
    back_btn = CreateButton(SCREEN_WIDTH / 2 - (252 / 2), 650, 252, 74, "Назад",
                            'BUTTON_ON.png', 'BUTTON_ON_HOVERED.gif', 'button_sound_click.mp3')

    running = True
    best_time = get_best_time()

    while running:
        screen.fill((0, 0, 0))
        screen.blit(bg, (sdvig, 0))

        font = pygame.font.Font(os.path.join('data', 'menu', 'fonts', 'pixel_font.ttf'), 72)
        text_surface = font.render('Статистика', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, 100))
        screen.blit(text_surface, text_rect)

        time_font = pygame.font.Font(os.path.join('data', 'menu', 'fonts', 'pixel_font.ttf'), 50)
        time_surface = time_font.render(f'Лучшее время: {best_time:.2f} сек', True, (255, 255, 255))
        time_rect = time_surface.get_rect(center=(SCREEN_WIDTH / 2, 400))
        screen.blit(time_surface, time_rect)

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
