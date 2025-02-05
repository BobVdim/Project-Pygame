import pygame
import config


class Timer:
    def __init__(self):
        self.start_ticks = pygame.time.get_ticks()
        self.pause_ticks = 0
        self.is_paused = False

        if config.DIFFICULTY_MOD == 'easy':
            self.spawn_interval = 1000
        elif config.DIFFICULTY_MOD == 'medium':
            self.spawn_interval = 700
        elif config.DIFFICULTY_MOD == 'hard' or config.DIFFICULTY_MOD == 'mega_hard':
            self.spawn_interval = 400
        else:
            self.spawn_interval = 1000

        self.last_spawn_time = pygame.time.get_ticks()

        self.min_spawn_interval = config.TIMER_SPAWN['min_spawn_interval']
        self.spawn_update_interval = config.TIMER_SPAWN['spawn_update_interval']
        self.mid_spawn_interval = config.TIMER_SPAWN['mid_spawn_interval']

        self.large_decrease_step = config.TIMER_SPAWN['large_decrease_step']
        self.small_decrease_step = config.TIMER_SPAWN['small_decrease_step']

        pygame.time.set_timer(pygame.USEREVENT, self.spawn_interval)

    def get_time(self):
        if self.is_paused:
            return (self.pause_ticks - self.start_ticks) / 1000
        else:
            return (pygame.time.get_ticks() - self.start_ticks) / 1000

    def draw(self, screen):
        try:
            font = pygame.font.Font('data/menu/fonts/pixel_font.ttf', 36)
        except:
            return
        time_text = f"Time: {int(self.get_time())}s"
        text_surface = font.render(time_text, True, (255, 255, 255))
        screen.blit(text_surface, (800 // 2 - text_surface.get_width() // 2, 20))

    def update_spawn_interval(self):
        if self.is_paused:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time >= self.spawn_update_interval:
            if self.spawn_interval > self.mid_spawn_interval:
                print(self.spawn_interval)
                self.spawn_interval -= self.large_decrease_step
            elif self.spawn_interval > self.min_spawn_interval:
                print(self.spawn_interval)
                self.spawn_interval -= self.small_decrease_step
            self.spawn_interval = max(self.spawn_interval, self.min_spawn_interval)

            pygame.time.set_timer(pygame.USEREVENT, self.spawn_interval)
            self.last_spawn_time = current_time

    def pause(self):
        self.is_paused = True
        self.pause_ticks = pygame.time.get_ticks()

    def resume(self):
        self.is_paused = False
        self.start_ticks += pygame.time.get_ticks() - self.pause_ticks
