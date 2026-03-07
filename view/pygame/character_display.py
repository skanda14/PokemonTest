import pygame
from settings import MESSAGE_TILE_WIDTH, MESSAGE_TILE_HEIGHT


class CharDisplay:
    def __init__(self, grid_pos, sprites_dict, char=None):
        self.char = None
        self.rect = pygame.Rect(grid_pos[0]*MESSAGE_TILE_WIDTH, grid_pos[1]*MESSAGE_TILE_HEIGHT, MESSAGE_TILE_WIDTH, MESSAGE_TILE_HEIGHT)
        self.sprites_dict = sprites_dict
        self.update(char)

    def update(self, new_char):
        if new_char:
            if new_char in self.sprites_dict:
                self.char = new_char
            else:
                print(f"error: {new_char} not in sprites_dict")
                self.char = None
        else:
            # print(f"new char: {new_char} is None")
            self.char = None

    def erase(self):
        self.char = None

    def copy(self, other_char_display):
        self.char = other_char_display.get_char()

    def cut(self, other_char_display):
        self.char = other_char_display.get_char()
        other_char_display.erase()

    def get_char(self):
        return self.char

    def display(self, surface):
        if self.char: surface.blit(self.sprites_dict[self.char], self.rect)
        # surface.blit(self.sprites_dict[self.char], self.rect)
