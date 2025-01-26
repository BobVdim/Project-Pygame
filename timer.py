import pygame


class Timer:
    def __init__(self):
        self.start_ticks = pygame.time.get_ticks()

    def get_time(self):
        seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
        return seconds

    def draw(self, screen):
        font = pygame.font.Font(None, 36)
        time_text = f"Time: {int(self.get_time())}s"
        text_surface = font.render(time_text, True, (255, 255, 255))
        screen.blit(text_surface, (800 // 2 - text_surface.get_width() // 2, 20))
