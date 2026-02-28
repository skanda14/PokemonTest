import pygame

class Debug:
    def __init__(self, screen):
        self.screen_rect = screen.get_rect()
        self.rect = pygame.Rect(0, 0, 640, 480)
        self.font = pygame.font.SysFont(None, 24)
        self.string = None
        self.render = None
        self.update("None")

    def update(self, string):
        self.string = string
        self.render = self.font.render(self.string, True, (248,248,248), (0,0,0))
        self.rect = self.render.get_rect()
        self.rect.topright = self.screen_rect.topright

    def display(self, screen):
        screen.blit(self.render, self.rect)
