import pygame
from settings import DEBUG_ACTIVATION


class DebugWindow:
    def __init__(self, screen_rect):
        self.screen_rect = screen_rect
        self.rect = pygame.Rect((0,0), (1,1))
        # self.rect.topright = screen_rect.topright
        self.font = pygame.font.SysFont("comicsans", 15)
        self.render_height = self.font.get_height()
        self.renders = []
        self.visible = DEBUG_ACTIVATION

    def is_visible(self):
        return self.visible

    def update(self, datas):
        self.renders = []
        max_width = 0
        height = len(datas)*self.render_height
        for data in datas:
            new_render = self.font.render(data, True, (255,255,255))
            max_width = max(max_width, new_render.get_width())
            self.renders.append(new_render)
        self.rect.size = max_width,height
        self.rect.topright = self.screen_rect.topright

    def display(self, screen):
        pygame.draw.rect(screen, (0,0,0), self.rect)
        base_x, y = self.rect.topright
        for render in self.renders:
            screen.blit(render, (base_x-render.get_width(),y))
            y += self.render_height
