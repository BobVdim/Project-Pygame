import pygame
import config


class Timer:
    def __init__(self):
        self.start_ticks = pygame.time.get_ticks()
        self.spawn_interval = config.TIMER_SPAWN['spawn_interval']
        self.last_spawn_time = pygame.time.get_ticks()
        self.min_spawn_interval = config.TIMER_SPAWN['min_spawn_interval']

        pygame.time.set_timer(pygame.USEREVENT, self.spawn_interval)

    def get_time(self):
        seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
        return seconds

    def draw(self, screen):
        font = pygame.font.Font(None, 36)
        time_text = f"Time: {int(self.get_time())}s"
        text_surface = font.render(time_text, True, (255, 255, 255))
        screen.blit(text_surface, (800 // 2 - text_surface.get_width() // 2, 20))

    def update_spawn_interval(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time >= 10000:
            if self.spawn_interval > 200:
                self.spawn_interval -= 100
                print(self.spawn_interval)
            elif self.spawn_interval > self.min_spawn_interval:
                self.spawn_interval -= 10
                print(self.spawn_interval)
            self.spawn_interval = max(self.spawn_interval, self.min_spawn_interval)

            pygame.time.set_timer(pygame.USEREVENT, self.spawn_interval)
            self.last_spawn_time = current_time
