import pygame
from settings import MOVE_DURATION_IN_FRAMES


def get_rect(images):
    w = 0
    h = 0
    for image in images:
        if image.get_width() > w:
            w = image.get_width()
        if image.get_height() > h:
            h = image.get_height()
    return pygame.Rect(0, 0, w, h)


class Animation:
    def __init__(self, name, images, img_dur=20, loop=True):
        self.name = name
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.frame = -1
        self.max_frame = MOVE_DURATION_IN_FRAMES*2  -1 #  self.img_duration * len(self.images) - 1
        self.img_duration = (self.max_frame+1)//len(self.images)

        self.rect = get_rect(self.images)

    def print_data(self):
        a = str(int(self.frame / self.img_duration))
        b = str(len(self.images))
        print(f"Animation: frame:{self.frame}/{self.max_frame} image:{a}/{b}")

    def get_rect(self):
        return self.rect.copy()

    def modify_rect_center_pos(self, pos):
        self.rect.center = pos

    def copy(self):
        return Animation(self.name, self.images, self.img_duration, self.loop)

    def update(self, game_speed=1):
        if self.loop:
            self.frame = (self.frame + game_speed) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + game_speed, self.max_frame)
            if self.frame >= self.max_frame:
                return False
        return True

    def reset(self):
        self.frame = 0

    def next_frame(self):
        self.frame = min(self.frame + 1, self.max_frame)

    def previous_frame(self):
        self.frame = max(self.frame-1, 0)

    def img(self):
        return self.images[int(self.frame / self.img_duration)]

    def display(self, surf, character_rect):
        img = self.img()
        # img.set_colorkey(img.get_at((0,0)))
        surf.blit(img, character_rect.topleft)
